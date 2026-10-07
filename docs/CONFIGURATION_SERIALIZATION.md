# Configuration serialization

`SerializableConfigMixin` remains available from `nkm_injection.results_schema`
and the package root. Its implementation lives in `nkm_injection.configuration`,
separate from publication provenance. Configuration classes must be dataclasses.

## Loading and migration

`from_dict(data)`, `from_json(text)` and `load(path)` are strict by default.
Unknown fields, unresolved annotations, missing required fields, invalid types,
nonfinite numbers and lossy numeric conversions raise errors. Errors identify
fields and sequence indices, such as `$.bts_opt_config.max_iter`.
Omitted fields with defaults still use those defaults. Domain `validate()` hooks
run for nested and outer dataclasses.

```python
from nkm_injection import BTSConfig

config = BTSConfig.load('bts_config.json')
# Explicit migration compatibility: ignore unknown fields, including nested ones.
legacy = BTSConfig.load('legacy_bts_config.json', strict=False)
legacy.save('results/migrated_bts_config.json')
```

Compatibility mode only ignores unknown fields. It does not restore truncation,
truthiness-based boolean conversion or nonfinite numbers. Review discarded fields
before using a migrated configuration. Existing well-typed saved objects retain
their JSON structure; no schema version or physical unit conversions are added.
No historical configuration files are rewritten automatically.

Booleans accept actual Python/NumPy booleans and case-insensitive `true`/`false`
strings. Numeric booleans and other strings are rejected. Integer fields accept
integral finite numeric values and numeric strings (including `"2.0"`), but reject
fractional values. Floating fields accept finite numbers and decimal strings;
numeric inputs that lose precision when converted to Python float are rejected.
Decimal float strings use ordinary binary floating-point parsing. Conversion
checks use exact equality, with no tolerance; physics validation retains each
configuration's existing units and tolerances (m, rad, eV, T and T m where used).

## Supported values and round trips

Supported annotations include primitive types, `Any`, optional/general unions,
`Literal`, nested dataclasses, typed lists, fixed/variable tuples, dictionaries,
`Path` and NumPy arrays. General unions prefer an exact existing type before
trying conversions in annotation order. Literals match both type and value;
`True` does not match the integer `1`. Tuples enforce their declared lengths.

Paths encode as strings, tuples and NumPy arrays as lists, and finite NumPy
scalars as Python scalars. Typed loading restores paths, tuples, dataclasses and
arrays; array dtype is inferred from JSON values, rather than preserved as extra
metadata. `Any` metadata preserves JSON types rather than recovering paths,
tuples or array objects. Integer mapping keys encode as strings, as required by
JSON; `Dict[int, ...]` restores integers, whereas untyped/`Any` metadata retains
string keys. Collisions between keys such as `1` and `"1"` are rejected.
Constructor fields are serialized; derived `init=False` fields are recomputed.

Unsupported objects/annotations and mapping keys are rejected instead of being
stringified. NaN/Infinity and overflowing JSON numbers are rejected recursively,
even in JSON fields ignored by compatibility mode. Duplicate JSON keys are
rejected. `save()` validates encoding before opening its destination, so an
encoding failure does not truncate an existing file. Use new result directories
for study outputs; source scientific files remain protected.

The shared result mixin also enforces finite JSON. No-loss distributions now
report `mean_first_loss_turn` and `fraction_lost_on_turn_1` as `None`/JSON `null`
instead of NaN. Consumers must handle these undefined statistics explicitly.
Other incomplete study results containing NaN/Inf must be resolved or represented
explicitly by their producer before serialization; they are not silently cleaned.
