# Milestone 101 — Local workflow checks without historical results

Completed: 2026-10-09

## Cause and outcome

`scripts/check_github_actions.sh` called `reproduce_paper.py --no-pdf` without
an explicit complete manifest. That selected the bundled legacy manifest and
failed on missing ignored stage directories in a clean checkout. Creating those
directories would still leave missing scientific results and metadata.

Replaced that check with existing isolated end-to-end publication tests. They
execute the real pipeline in a fresh process and the real reproduction CLI with
complete temporary fixtures, verify hashes and generate seven tables/four figures.
These synthetic software fixtures are clearly identified and are not production
scientific evidence. Actual publication validation remains strict and unchanged.
Updated the local paper/release workflow definitions to use the same tests;
no remote workflows or GitHub APIs were queried or executed.

The checker uses `NKM_PYTHON` (default python3) for every Python/pytest command.
Inventories, logs, pytest cache and test outputs use a fresh temporary workspace.
Successful runs remove it; failures retain logs and show diagnostics even in
quiet mode. Invalid workflow/options fail before writes; dry runs only print
commands. The misleading invitation to push was removed.

Baseline tests now generate reference metrics in temporary directories and
verify the versioned scientific hashes. They no longer read/rewrite historical
baseline metrics or depend on the former fixed inventory destination. The CI
workflow performs these isolated baseline checks. Stored-beam physics regression
uses a temporary generated lattice with an explicit original MAT source.

## Validation

- Local fast checks completed, including isolated baseline checks, real paper
  integration/CLI tests, physics regressions and before/after input verification.
- Nine checker regressions passed, including a copied checkout with no results,
  source/output immutability, all four dry-run targets, invalid options and retained
  quiet-mode error diagnostics. The clean-copy check created no results, generated
  lattice or pytest cache in that checkout and removed its temporary workspace.
- The final unchanged full checker returned status 0: all seven checks passed,
  including the **624-test** full regression suite and post-check immutability.
- The final paper-only checker also returned status 0; successful temporary
  workspaces were removed.
- Shell syntax and `git diff --check` passed.
- Nine protected files matched HEAD by SHA-256, and all 130 pre-existing result
  files retained their hashes. Validation generated no production study outputs.

## Conventions and scope

No integrators, optimizer physics, particle-loss definitions, units or numerical
tolerances changed. Baseline physics tests retain their fixed seed and established
tolerances. Scientific interfaces remain m, rad, eV, T and T m. The local checker
validates workflow commands and software contracts; scientific paper reproduction
requires a complete production-run manifest. PDF compilation is separately covered
by isolated lifecycle regressions and is not requested by these fixture checks.
