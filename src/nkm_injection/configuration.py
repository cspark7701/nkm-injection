"""Typed configuration JSON; values retain their documented interface units."""
from dataclasses import fields, is_dataclass
from decimal import Decimal, InvalidOperation
import json
import math
from pathlib import Path
import types
from typing import Any, Dict, Literal, Union, get_args, get_origin, get_type_hints

import numpy as np


def _to_serializable(value: Any, path: str = '$') -> Any:
    """Encode supported values without stringifying objects or nonfinite numbers."""
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, (int, np.integer)):
        return int(value)
    if isinstance(value, (float, np.floating)):
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f'{path}: expected a finite number')
        if number != value:
            raise ValueError(f'{path}: conversion to float would lose precision')
        return number
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.ndarray):
        return _to_serializable(value.tolist(), path)
    if is_dataclass(value) and not isinstance(value, type):
        return {f.name: _to_serializable(getattr(value, f.name), f'{path}.{f.name}')
                for f in fields(value) if f.init}
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            if isinstance(key, (int, np.integer)) and not isinstance(key, (bool, np.bool_)):
                key = str(key)
            elif not isinstance(key, str):
                raise TypeError(f'{path}: JSON mapping keys must be strings or integers')
            if key in result:
                raise ValueError(f'{path}: mapping keys collide after JSON encoding: {key!r}')
            result[key] = _to_serializable(item, f'{path}[{key!r}]')
        return result
    if isinstance(value, (list, tuple)):
        return [_to_serializable(item, f'{path}[{i}]') for i, item in enumerate(value)]
    raise TypeError(f'{path}: unsupported serialized type {type(value).__name__}')


def _coerce(value, hint, path, strict):
    origin, args = get_origin(hint), get_args(hint)
    if hint is Any:
        _to_serializable(value, path)
        return value
    if origin in (Union, getattr(types, 'UnionType', Union)):
        # Prefer an existing exact type so Union[int, str] preserves strings.
        preferred = [a for a in args if isinstance(a, type) and type(value) is a]
        failures = []
        for branch in preferred + [a for a in args if a not in preferred]:
            try:
                return _coerce(value, branch, path, strict)
            except (TypeError, ValueError) as exc:
                failures.append(str(exc))
        raise ValueError(f'{path}: value does not match {hint}; ' + '; '.join(failures))
    if origin is Literal:
        if any(type(value) is type(a) and value == a for a in args):
            return value
        raise ValueError(f'{path}: expected one of {args!r}')
    if hint is type(None):
        if value is None:
            return None
        raise TypeError(f'{path}: expected null')
    if value is None:
        raise TypeError(f'{path}: null is not allowed for {hint}')
    if isinstance(hint, type) and is_dataclass(hint):
        if isinstance(value, hint):
            value = _to_serializable(value, path)
        return _load_dataclass(hint, value, path, strict)
    if origin in (list, tuple, dict) or hint in (list, tuple, dict):
        container = origin or hint
        if container is dict:
            if not isinstance(value, dict):
                raise TypeError(f'{path}: expected a mapping')
            key_hint, item_hint = args or (str, Any)
            if key_hint not in (str, int, Any):
                raise TypeError(f'{path}: JSON mappings require string or integer key annotations')
            result = {}
            for key, item in value.items():
                converted_key = _coerce(key, key_hint, path, strict)
                if converted_key in result:
                    raise ValueError(f'{path}: mapping keys collide after conversion: {key!r}')
                result[converted_key] = _coerce(item, item_hint, f'{path}[{key!r}]', strict)
            return result
        if not isinstance(value, (list, tuple)):
            raise TypeError(f'{path}: expected a sequence')
        if container is tuple and args and not (len(args) == 2 and args[1] is Ellipsis):
            if len(value) != len(args):
                raise ValueError(f'{path}: expected tuple length {len(args)}, got {len(value)}')
            hints = args
        else:
            hints = [args[0] if args else Any] * len(value)
        converted = [_coerce(v, h, f'{path}[{i}]', strict)
                     for i, (v, h) in enumerate(zip(value, hints))]
        return tuple(converted) if container is tuple else converted
    if hint is np.ndarray:
        if not isinstance(value, (list, tuple, np.ndarray)):
            raise TypeError(f'{path}: expected an array')
        _to_serializable(value, path)
        try:
            return np.asarray(value)
        except ValueError as exc:
            raise ValueError(f'{path}: invalid array: {exc}') from exc
    if isinstance(hint, type) and issubclass(hint, Path):
        if not isinstance(value, (str, Path)):
            raise TypeError(f'{path}: expected a path string')
        return hint(value)
    if hint is bool:
        if isinstance(value, (bool, np.bool_)):
            return bool(value)
        if isinstance(value, str) and value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        raise TypeError(f'{path}: expected boolean or true/false string')
    if hint in (int, float):
        if isinstance(value, (bool, np.bool_)) or not isinstance(value, (str, int, float, np.integer, np.floating)):
            raise TypeError(f'{path}: expected {hint.__name__}')
        try:
            if hint is int:
                if isinstance(value, str):
                    number = Decimal(value)
                    if not number.is_finite() or number != number.to_integral_value():
                        raise ValueError('expected a finite integral value')
                    return int(number)
                if isinstance(value, (int, np.integer)):
                    return int(value)
                if not np.isfinite(value) or value != np.floor(value):
                    raise ValueError('expected a finite integral value')
                return int(value)
            result = float(value)
            if not math.isfinite(result):
                raise ValueError('expected a finite number')
            source = int(value) if isinstance(value, (int, np.integer)) else value
            if not isinstance(value, str) and result != source:
                raise ValueError('conversion to float would lose precision')
            return result
        except (ValueError, OverflowError, InvalidOperation) as exc:
            raise ValueError(f'{path}: {exc}') from exc
    if hint is str:
        if isinstance(value, str):
            return value
        raise TypeError(f'{path}: expected a string')
    raise TypeError(f'{path}: unsupported annotation {hint!r}')


def _load_dataclass(cls, data, path, strict):
    if not isinstance(data, dict):
        raise TypeError(f'{path}: expected a dictionary for {cls.__name__}')
    if not is_dataclass(cls):
        raise TypeError(f'{path}: {cls.__name__} must be a dataclass')
    try:
        hints = get_type_hints(cls)
    except (NameError, TypeError) as exc:
        raise TypeError(f'{path}: cannot resolve annotations for {cls.__name__}: {exc}') from exc
    allowed = {f.name for f in fields(cls) if f.init}
    unknown = set(data) - allowed
    if strict and unknown:
        raise ValueError(f'{path}: unknown fields {sorted(unknown, key=str)!r}')
    kwargs = {name: _coerce(value, hints[name], f'{path}.{name}', strict)
              for name, value in data.items() if name in allowed}
    try:
        instance = cls(**kwargs)
        validate = getattr(instance, 'validate', None)
        if callable(validate):
            validate()
    except (TypeError, ValueError) as exc:
        raise type(exc)(f'{path}: {exc}') from exc
    return instance


class SerializableConfigMixin:
    """Dataclass JSON I/O with strict typed loading and domain validation.

    ``strict=False`` only ignores unknown fields, recursively. Unsafe scalar
    coercions and nonfinite values remain errors in both modes.
    """
    def to_dict(self) -> Dict[str, Any]:
        return _to_serializable(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, allow_nan=False)

    def save(self, filepath: Union[str, Path], indent: int = 2) -> None:
        # Validate before opening a destination, preserving files on encoding errors.
        content = self.to_json(indent=indent)
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')

    @classmethod
    def _coerce_field_value(cls, val: Any, hint: Any) -> Any:
        return _coerce(val, hint, '$', True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], *, strict: bool = True) -> Any:
        return _load_dataclass(cls, data, '$', strict)

    @classmethod
    def from_json(cls, json_str: str, *, strict: bool = True) -> Any:
        def pairs(items):
            result = {}
            for key, value in items:
                if key in result:
                    raise ValueError(f'$: duplicate JSON key {key!r}')
                result[key] = value
            return result
        data = json.loads(json_str, object_pairs_hook=pairs)
        # Also catches overflow literals such as 1e999, even in ignored fields.
        _to_serializable(data)
        return cls.from_dict(data, strict=strict)

    @classmethod
    def load(cls, filepath: Union[str, Path], *, strict: bool = True) -> Any:
        return cls.from_json(Path(filepath).read_text(encoding='utf-8'), strict=strict)

    def validate(self) -> None:
        """Override to validate physical assumptions and interface units."""
