# 248 — Fix round-four CI tests on clean checkouts

Date: 2026-10-20. Starting commit: fa63e3ddf68e26c37428a4a5b9b1290b8684bff7.

The user explicitly authorized inspection of remote GitHub Actions failures for
this task. Read the failed CI run 39430592540 and its logs; the Python 3.11 job
failed seven round-four tests on absent git-ignored campaign inputs. The Python
3.10 job was cancelled by matrix fail-fast. Paper Regression run 39430592758
passed. No push, workflow dispatch or remote mutation was performed.

Reproduced the same seven failures from a git archive without local results.
Replaced the failing tests' production-result dependencies with temporary,
synthetic beam/error inputs and manifests. The real budget loaders, manifest
builder (including hashes/history), point-identity guard and physics functions
remain exercised. Both field-scale and injection-position mismatches are
rejected. Committed manifest paths are still checked against current overrides.
The error-free post-kick check now constructs/calibrates its input instead of
silently returning when an archived checkpoint is absent. The separate archived
F1-candidate integration check explicitly skips when its optional data is absent.
None of the seven remotely failing tests is skipped.

All fixture outputs stay under pytest temporary directories. No scientific source,
production driver, workflow, manuscript, existing campaign or evidence bundle is
modified. The workflows keep their full test suite and existing Python matrix.

Validation (Python 3.11, project pyAT environment):

- Before the fix, clean export: seven failed and six passed in the affected module,
  reproducing the remote missing-file failures.
- Repaired module in the working checkout: 14 passed.
- Repaired module in the clean export: 13 passed, one explicit archived-data skip.
- Full suite in the clean export: 757 passed, one explicit archived-data skip,
  140.18 seconds. No real campaign outputs were supplied.
- Protected inputs match the pre-change archive; `git diff --check` passes.

Python 3.10 was not available locally; its remote job was cancelled after the
3.11 failure. The fix is to version-independent test input isolation, and both
matrix entries remain enabled. Remote logs identify the failure; local results
do not assert that a new remote run has passed.
Remote success cannot be verified until the local fix is pushed by the author;
this task does not push.
