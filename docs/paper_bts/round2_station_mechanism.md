# Limiting-station mechanism — R2-BTS-02

Reproduce with `python scripts/run_bts_round2.py --stage stations --output-dir results/<new>/stations`. All 600 original paired-shot minima are reconstructed within 1e-12 m. Full station decomposition is in the new campaign's station_realizations.json; variances, rather than RMS components, add. The exported summary is [round2_stations.json](generated/round2_stations.json).

For any setting K, c_min(K) <= c_entrance, because the entrance is included in the minimum and lies before adjustable quadrupoles. If all downstream c exceed that ceiling, the full minimum is independent of K. This is an observable saturation condition, not a failure of quadrupole optimization or evidence about an unknown continuous chamber.

All406 exact shot ties have the horizontal entrance active in both designs. Reference active counts are449 entrance-x,103 exit-x and48 exit-y; low-beta counts are467,113 and20. Neither internal aperture is limiting in this original ensemble. Of200 machine means,54 improve,53 worsen and93 tie. Difference SD is0.23630 mm; 5th/median/95th percentiles are -0.32237/0/+0.40338 mm and range is -0.92289 to+1.40103 mm. The mean0.014610 mm hides heterogeneity. Downstream-only mean change is+0.056402 mm and is a secondary diagnostic, not a replacement headline metric.

The nominal station records give halfwidth, centroid, betatron/coupled variance, momentum-correlated dispersion variance, RMS and clearance for both settings. New hypothetical internal restrictions will test non-entrance-limited regimes; they do not represent verified hardware. Original tests remain retrospective evidence, not an untouched validation set for new selection.
