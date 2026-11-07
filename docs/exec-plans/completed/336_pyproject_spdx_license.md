# Milestone 336 — SPDX license metadata in pyproject.toml

Completed: 2026-11-07. Removes the setuptools deprecation warning that `project.license` as a TOML table will stop
building after 2027-02-18.

**Change** (`pyproject.toml`).
- `license = {text = "MIT"}` became `license = "MIT"` with `license-files = ["LICENSE"]`. The `LICENSE` file is the
  MIT License.
- The build requirement rose from `setuptools>=61.0` to `setuptools>=77.0.0`, the first version that accepts this
  form.

**Check.** A wheel built in pip's isolated environment from a copy of the tracked sources (setuptools 84.2.1) succeeds
with no deprecation message. Its metadata has `License-Expression: MIT` and `License-File: LICENSE`, and the wheel
contains the license file. The test suite was not rerun, because only packaging metadata changed. Protected files are
unchanged.
