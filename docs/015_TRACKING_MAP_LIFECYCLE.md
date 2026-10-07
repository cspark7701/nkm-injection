# One-turn tracking map lifecycle

`track_multiturn_injection` computes the linear one-turn M66 map once per tracking call, before the turn loop, using `ring.find_m66(dp=0.0)`. It reuses that local map for the turns in that call and retains no map state between calls.

Previously, a function attribute cached the map using only `id(ring)`. Changing quadrupole strengths, geometry, energy, alignment or RF/radiation settings on the same lattice could reuse stale physics. Each subsequent call now recomputes the map from the current lattice. Alternating rings and independent calls do not share Python map state. The lattice must remain unchanged while its tracking call runs.

The public signature and TrackingResult schema are unchanged. Kicker timing, map reference momentum (`dp=0.0`), aperture thresholds, observation points and particle-loss accounting are unchanged. Task 09 now requires positive integer turn counts; zero-turn calls raise before computing a map. Use beam statistics directly for initial-state inspection (see [tracking input contracts](019_TRACKING_INPUT_CONTRACTS.md)). Error ensemble factories already construct perturbed lattices; they require no cache-invalidation protocol.

Particle arrays have shape `(6, N)` in AT coordinate order `(x, px, y, py, delta, ct)`. Positions and ct use m, transverse canonical momenta use the existing rad convention, and delta is dimensionless. Beam energy is in eV at the configuration boundary and is converted to GeV for the existing kicker tracking interface. Aperture losses are checked after each one-turn map; the first turn uses the injection x aperture and subsequent turns use the stored-beam x aperture.

## Validation

`tests/test_tracking_map_lifecycle.py` checks in-place quadrupole, drift-length and roll changes against freshly computed maps, observes energy changes, checks alternating rings, verifies one map computation per call, and tests simultaneous calls with shared/independent immutable map providers. Concurrent tests isolate the function's Python state; the project's existing pyAT process-worker policy is unchanged. Additional checks cover rejection of zero turns, unchanged inputs, ignored legacy cache attributes and aperture loss particle/turn identities.

Fresh-map particle coordinates are compared with zero relative tolerance and absolute tolerance `1e-14`. These small regression lattices are in memory; source lattices and notebooks are not regenerated. Existing injection, field/kick and convergence tests retain their numerical tolerances.

## Repeated-call cost

A small fresh-process benchmark used the original source ring, enabled RF, 20 Gaussian particles, ten turns, seed 42, an off kicker and five timed calls after warm-up. Initial Twiss was beta_x=10 m, beta_y=5 m and alpha=0; emittances were 1e-8/1e-9 m rad, rms relative energy spread 1.1e-3 and rms bunch length 13.4 mm. Energy was 4 GeV. Injection/stored horizontal apertures were 45/30 mm and the vertical aperture was 15 mm. Observation was at the ring entrance after each turn; all 20 particles survived.

| Implementation | Median seconds per warm call |
| --- | ---: |
| Previous function cache, unchanged ring | 0.001436 |
| Current call-local map | 0.167295 |

The extra setup cost was approximately 0.166 s per call in this environment. Final particle coordinates were identical (maximum absolute difference zero). These timings characterize a small repeated ensemble, not full production throughput. The benchmark supports keeping recomputation explicit and reporting its cost; no new cross-call cache or prepared-context API is introduced by Task 05.

The benchmark and fresh-process mutation check wrote only under `/tmp/nkm-task05-map-lifecycle-20261007/`. Protected inputs were read without modification.
