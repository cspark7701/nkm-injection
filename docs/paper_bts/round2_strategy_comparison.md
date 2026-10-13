# Frozen design strategies and new test — R2-BTS-05

[Designs and sweep](generated/round2_designs.json), [new-test results](generated/round2_comparison.json). Reproduce `python scripts/run_bts_round2.py --stage designs --output-dir results/<new>/designs`; `--stage comparison` uses the selected frozen campaign designs unless another design file is explicitly supplied by the driver.200 new independent static machines, three shots and2000 common Gaussian particle draws per shot use seeds82002/82003/82004; bootstrap82005. All nine regime/design combinations are evaluated, totalling10.8 million particle transports. The original test is not used for design selection.

All settings preserve the same six configured exit optics and family bounds. Low-beta uses the spatially refined setting. Nominal direct-clearance optimization uses a millimetre-scaled epigraph, the same matching equalities and horizontal-beta ceiling, two declared starts,200-iteration budgets and1e-8 termination tolerance. All candidate success/failure/iteration/termination records and64-subdivision feasibility are retained. Baseline clearance is degenerate at the fixed entrance; its tiny numerical change is not a physical gain. Finite starts do not establish global optimality.

Hypothetical cases narrow only horizontal m2(s=6.833 m) to3 mm halfwidth, or only vertical m3(s=11.761 m) to1.5 mm; every other aperture and entrance/exit remains unchanged. These are illustrative restrictions, not inferred chamber dimensions. The predeclared nominal halfwidth sweep(1.5,2,3,5,30 mm) exposes transitions; it does not select designs using held-out outcomes.

New paired mean changes versus reference, with pointwise95% machine-cluster intervals [mm]:

| Regime | Refined low beta | Direct nominal clearance |
| :--- | :--- | :--- |
| Baseline | +0.0103 [-0.0156,+0.0377] | numerically zero |
| Horizontal m2 restriction | -0.1522 [-0.1574,-0.1471] | +0.8806 [+0.8472,+0.9135] |
| Vertical m3 restriction | +0.0733 [+0.0478,+0.0980] | +0.2123 [+0.1738,+0.2502] |

Beta reduction helps or hurts according to the limiting plane/location and transport response. Direct nominal clearance performs better in these selected restricted cases, but no robust/global optimizer or universal superiority is claimed. Illustrative useful change is0.1 mm: low-beta vertical gain is resolved but remains below that scale; direct gains exceed it. Common errors and particles ensure paired comparisons. New representative quadrature checks cover every regime/design and bound local moment approximation relative to these effects.

## Invalid preliminary run retained

The legacy lattice shares the same aperture element at both internal stations. A lattice deepcopy preserves that alias. Initial hypothetical limit assignment therefore affected two stations, invalidating the declared cases. Those complete designs/results and exact generating source are retained under invalid_* directories, with invalid_shared_aperture_record.json; none contributes to the paper. The selected aperture is now independently copied before limit assignment. A regression checks the other station is unchanged. The corrected campaign repeats the unchanged declared seeds/protocol; no observed-test optimization or changed restriction was used.
