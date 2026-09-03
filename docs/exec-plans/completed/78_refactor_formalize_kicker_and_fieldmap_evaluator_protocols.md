# Milestone 78 — Task 14: Formalize Kicker and Field Map Evaluator Protocols

## Executive Summary

Task 14 establishes runtime-checkable Python `Protocol` interfaces (`FieldMap3DProtocol`, `KickerEvaluatorProtocol`) and lightweight evaluator classes across the `nkm_injection` package. This decouples numerical integrators (`SymplecticSplitIntegrator`, `LorentzRK4Integrator`) and multi-turn tracking routines from loose, ad-hoc `Callable` closures, while providing zero-I/O mock field evaluators (`ZeroFieldMap3D`, `UniformFieldMap3D`, `LinearGradientFieldMap3D`) and typed kicker evaluators (`OffKickerEvaluator`, `IdealKickerEvaluator`, `LinearKickerEvaluator`, `NKMKickMap2D`).

---

## Key Achievements

### 1. Created Formal Runtime-Checkable Protocols
- **Location**: [`src/nkm_injection/units.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/units.py)
- **Protocols**:
  - `FieldMap3DProtocol(Protocol)`:
    - Signature: `__call__(self, x: np.ndarray, y: np.ndarray, z: float) -> Tuple[np.ndarray, np.ndarray]`
    - Explicitly defines expected coordinates ($x, y, z$) in meters and returns $(B_y, B_x)$ in Tesla.
  - `KickerEvaluatorProtocol(Protocol)`:
    - Attributes: `model_type: KickerModelType`, `length_m: float`, `energy_eV: float`, `metadata: KickMapMetadata`.
    - Methods:
      - `evaluate_kicks(self, x: Union[float, np.ndarray], y: Optional[Union[float, np.ndarray]] = None) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]` returning $(\Delta x', \Delta y')$ in radians.
      - `__call__(self, x: Union[float, np.ndarray], y: Union[float, np.ndarray]) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]` evaluating raw kicks according to `metadata.value_unit` (e.g. mrad).

### 2. Created Mock Field Evaluators for Unit Testing
- **Location**: [`src/nkm_injection/units.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/units.py)
- **Classes**:
  - `ZeroFieldMap3D`: Conforms to `FieldMap3DProtocol` and returns zero fields without disk I/O.
  - `UniformFieldMap3D(by_T, bx_T)`: Conforms to `FieldMap3DProtocol` and produces constant transverse dipole fields.
  - `LinearGradientFieldMap3D(gradient_T_per_m)`: Conforms to `FieldMap3DProtocol` and evaluates quadrupole gradients.

### 3. Implemented Kicker Evaluators and Updated Integrators
- **Kick Map Class**:
  - Enhanced [`NKMKickMap2D`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/kickmap.py) with `model_type = "fieldmap"`, `energy_eV`, `__call__`, and `evaluate_kicks` to fully conform to `KickerEvaluatorProtocol`.
- **Kicker Evaluator Classes**:
  - Defined [`OffKickerEvaluator`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/storage_ring_injection.py), [`IdealKickerEvaluator`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/storage_ring_injection.py), and [`LinearKickerEvaluator`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/storage_ring_injection.py).
  - Updated [`get_kicker_evaluator`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/storage_ring_injection.py) to return typed evaluator objects.
- **Integrators**:
  - Updated `SymplecticSplitIntegrator` and `LorentzRK4Integrator` in [`src/nkm_injection/integrators.py`](file:///home/cspark/Work/projects/nkm-injection/src/nkm_injection/integrators.py) to type-hint `field_fn: Union[FieldMap3DProtocol, Callable[...]]`.

### 4. Expanded Test Suite
- **Location**: [`tests/test_nkm_integrators.py`](file:///home/cspark/Work/projects/nkm-injection/tests/test_nkm_integrators.py)
- **Tests Added**:
  - `test_field_map_3d_protocol_and_mock_evaluators`: Verified `isinstance(..., FieldMap3DProtocol)` across `ZeroFieldMap3D`, `UniformFieldMap3D`, `LinearGradientFieldMap3D`, and tested direct tracking through `SymplecticSplitIntegrator`.
  - `test_kicker_evaluator_protocols`: Verified `isinstance(..., KickerEvaluatorProtocol)` across `"off"`, `"ideal"`, `"linear"`, and `"fieldmap"` models, verifying kick evaluations and scaling.

---

## Verification & Status

- **Unit Test Suite**: 192/192 passing tests (+2 new tests added).
- **Protected Files Integrity**: Unchanged and verified against SHA-256 baseline.
