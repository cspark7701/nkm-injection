# Bibliography audit (Task 010)

Performed 2026-10-09. Journal DOIs were resolved through the Crossref API, JACoW proceedings DOIs through
DataCite and doi.org, and the IPAC'11 paper from the first page of the proceedings PDF. Author lists
in `paper.bib` match the publisher records exactly.

## Removed from the previous bibliography

| Key | Reason |
| :--- | :--- |
| `NKM_Injection_2021` (Takaki et al., PRAB 24, 040701, 2021) | No such record found; title and DOI unverifiable. Replaced by the verified Takaki et al. 2010 PRST-AB paper. |
| `MAXIV_NKM_2018` (Olsson et al., NIM A 880, 2018) | No matching record found. MAX IV/SOLEIL multipole injection kicker results are cited through Ollier et al. 2023. |
| `SLS_NKM_2016` (Aiba et al., NIM A 830, 2016) | No matching record found. |
| `PyAT_2019` (White et al., IPAC'19 TUPGW077) | Unverified authorship and DOI; replaced by Rogers et al., IPAC'17 THPAB060 (verified). |
| `NSGA2_2002`, `Pymoo_2020` | Real publications, but MOGA is removed from the article (moga_decision.md), so they are no longer cited. |

## Retained and added (all verified)

| Key | Record | Supports |
| :--- | :--- | :--- |
| Takaki2010 | PRST-AB 13, 020705 (2010), doi:10.1103/PhysRevSTAB.13.020705 | Pulsed multipole (sextupole) injection demonstrated at KEK-PF |
| Atkinson2011 | IPAC'11 THPO024, pp. 3394–3396 | Single non-linear kicker with zero central field and an off-axis peak (BESSY II) |
| Liu2016 | IPAC'16 THPMR011, pp. 3406–3408, doi:10.18429/JACoW-IPAC2016-THPMR011 | Kick nonlinearity at the injected beam and beam size limit NLK efficiency |
| Ollier2023 | PRAB 26, 020101 (2023), doi:10.1103/PhysRevAccelBeams.26.020101 | MIK at MAX IV/SOLEIL; perturbation < 2 % of stored rms size |
| Gora2023 | IPAC'23 MOPM075, pp. 1156–1158, doi:10.18429/JACoW-IPAC2023-MOPM075 | BESSY II NLK beam-based characterization; up to 97 % efficiency with optimised sextupoles |
| Chubar1998 | J. Synchrotron Rad. 5, 481–484 (1998), doi:10.1107/S0909049597013502 | RADIA |
| Terebilo2001 | PAC'01 RPAH314, pp. 3203–3205 | Accelerator Toolbox |
| Rogers2017 | IPAC'17 THPAB060, pp. 3855–3857, doi:10.18429/JACoW-IPAC2017-THPAB060 | pyAT |
| Wilson1927 | JASA 22, 209–212, doi:10.1080/01621459.1927.10502953 | Wilson score interval |
| Clopper1934 | Biometrika 26, 404–413, doi:10.1093/biomet/26.4.404 | Exact binomial interval |

Each cited statement in `paper.tex` is limited to what the abstract or first page of the source supports.
Full texts of the PRAB/PRST-AB articles were not read; quantitative statements from them are limited to
the abstracts (e.g. the < 2 % perturbation in Ollier et al.). The style follows JINST numbered
references in order of citation (`JHEP.bst` is requested by JINST; `unsrt` is used locally because
`JHEP.bst` is not installed — to be replaced at submission, Task 012).

Data and software availability: the repository is public on GitHub, but no permanent archive (DOI) has
been created; the availability statement therefore cites the repository and commit and says that a
Zenodo DOI will be created at acceptance. No archive is described as existing before it is created.
