"""Configuration values round-trip exactly; no physics or unit conversion."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

import numpy as np
import pytest

from nkm_injection.results_schema import SerializableConfigMixin
from nkm_injection.moga import BTSMOGAConfig


@dataclass
class Child:
    count: int = 2


@dataclass
class Config(SerializableConfigMixin):
    enabled: bool = False
    count: int = 2
    strength: float = 1.25  # T m, unchanged by serialization
    child: Child = field(default_factory=Child)
    pairs: Tuple[int, float] = (2, 1.25)
    seeds: Tuple[int, ...] = (3, 5)
    output: Path = Path('results/config.json')
    choice: Union[int, str] = '3'
    mode: Literal['off', 'on'] = 'off'
    optional: Optional[int] = None
    mapping: Dict[str, List[int]] = field(default_factory=lambda: {'seeds': [2, 3]})
    metadata: Dict[str, Any] = field(default_factory=dict)


@pytest.mark.parametrize('value, expected', [(False, False), (True, True), ('false', False),
                                           ('true', True), ('FALSE', False), (np.bool_(False), False)])
def test_boolean_values(value, expected):
    assert Config.from_dict({'enabled': value}).enabled is expected


@pytest.mark.parametrize('data, path', [({'enabled': 'no'}, 'enabled'), ({'enabled': 1}, 'enabled'),
    ({'count': 1.5}, 'count'), ({'count': '1.5'}, 'count'), ({'count': True}, 'count'),
    ({'strength': 2**53 + 1}, 'strength'), ({'strength': np.int64(2**53 + 1)}, 'strength'),
    ({'child': {'count': 1.5}}, 'child.count'), ({'pairs': [2]}, 'pairs'),
    ({'pairs': [2, 'bad']}, r'pairs\[1\]'), ({'count': None}, 'count'),
    ({'mode': 'unknown'}, 'mode'), ({'mapping': {'seeds': [1, 1.5]}}, r'mapping.*\[1\]'),
    ({'output': 23}, 'output'), ({'enabled': []}, 'enabled')])
def test_invalid_values_have_field_paths(data, path):
    with pytest.raises((TypeError, ValueError), match=path):
        Config.from_dict(data)


def test_unknown_keys_and_explicit_compatibility(tmp_path):
    data = {'child': {'count': 3, 'cout': 4}}
    with pytest.raises(ValueError, match=r'\$\.child: unknown fields.*cout'):
        Config.from_dict(data)
    assert Config.from_dict(data, strict=False).child.count == 3
    path = tmp_path / 'config.json'
    path.write_text('{"cout": 2}')
    with pytest.raises(ValueError, match='cout'):
        Config.load(path)
    assert Config.load(path, strict=False) == Config()
    with pytest.raises(ValueError, match='count'):
        Config.from_dict({'count': 1.5}, strict=False)


def test_semantic_roundtrip(tmp_path):
    original = Config(enabled=np.bool_(True), count=np.int64(4), strength=np.float64(1.25),
                      metadata={'array': np.array([1, 2]), 'scalar': np.float32(0.5)})
    restored = Config.from_json(original.to_json())
    assert restored.to_dict() == original.to_dict()
    assert restored.output == original.output
    assert restored.pairs == original.pairs
    assert restored.seeds == original.seeds
    assert restored.choice == '3'
    assert isinstance(restored.child, Child)
    assert Config.from_dict({'count': '2.0', 'strength': '1.25'}).count == 2
    original.save(tmp_path / 'config.json')
    assert Config.load(tmp_path / 'config.json') == restored
    moga = BTSMOGAConfig()
    moga.bts_opt_config.max_iter = 77
    assert BTSMOGAConfig.from_json(moga.to_json()) == moga


@pytest.mark.parametrize('value', [float('nan'), float('inf'), -float('inf'), np.float64('nan')])
def test_nonfinite_rejected_everywhere(value, tmp_path):
    with pytest.raises(ValueError, match='strength'):
        Config.from_dict({'strength': value})
    bad = Config(metadata={'nested': [value]})
    with pytest.raises(ValueError, match=r'metadata.*nested.*\[0\]'):
        bad.to_dict()
    path = tmp_path / 'existing.json'
    path.write_text('preserve me')
    with pytest.raises(ValueError):
        bad.save(path)
    assert path.read_text() == 'preserve me'


@pytest.mark.parametrize('literal', ['NaN', 'Infinity', '-Infinity', '1e999'])
def test_nonfinite_json_including_unknown_keys(literal):
    with pytest.raises(ValueError, match='finite'):
        Config.from_json('{"unknown": ' + literal + '}', strict=False)


def test_unsupported_values_and_duplicate_keys():
    with pytest.raises(TypeError, match='unsupported serialized type object'):
        Config(metadata={'thing': object()}).to_dict()
    with pytest.raises(TypeError, match='keys must be strings'):
        Config(metadata={object(): 'one'}).to_json()
    with pytest.raises(ValueError, match='duplicate JSON key'):
        Config.from_json('{"count": 1, "count": 2}')
    with pytest.raises(TypeError, match='dictionary'):
        Config.from_dict([])


def test_unresolved_annotations_are_not_suppressed():
    @dataclass
    class Broken(SerializableConfigMixin):
        value: 'NonexistentType' = None
    with pytest.raises(TypeError, match='cannot resolve annotations'):
        Broken.from_dict({'value': 1})


def test_union_literal_and_array_types():
    @dataclass
    class Choices(SerializableConfigMixin):
        value: Union[int, Child]
        flag: Literal[True]
        array: np.ndarray
    value = Choices.from_dict({'value': {'count': 3}, 'flag': True, 'array': [[1, 2]]})
    assert value.value == Child(3)
    np.testing.assert_array_equal(Choices.from_json(value.to_json()).array, value.array)
    with pytest.raises(ValueError, match='flag'):
        Choices.from_dict({'value': 2, 'flag': 1, 'array': []})
    with pytest.raises(ValueError, match='value'):
        Choices.from_dict({'value': 1.5, 'flag': True, 'array': []})


def test_integer_mapping_keys_and_collisions():
    @dataclass
    class Histogram(SerializableConfigMixin):
        counts: Dict[int, int]
    original = Histogram({1: 3, 2: 4})
    assert Histogram.from_json(original.to_json()) == original
    with pytest.raises(ValueError, match='collide'):
        Histogram.from_dict({'counts': {'01': 2, '1': 3}})
    with pytest.raises(ValueError, match='collide'):
        Config(metadata={1: 'one', '1': 'another'}).to_json()


def test_integral_float_conversion_preserves_actual_value():
    value = 1e23
    assert Config.from_dict({'count': value}).count == int(value)
