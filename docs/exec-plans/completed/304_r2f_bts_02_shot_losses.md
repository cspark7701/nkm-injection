# Milestone 304: R2F-BTS-02 model bounds and shot losses

Completed: 2026-10-31. Qualified the max/sum bracket as a bound on linearized
Gaussian probabilities, not on finite tracked counts. Added a reproducible
saved-output audit and generated macros. Of 600 shots, 16 carry the 942 observed
losses; the review's count of 20 is corrected from the raw records. Machine 116,
shot 2 contributes 454 losses against 410.8915 expected, about 70% of the total
61.5467-particle excess. The stored total conditional expectation is reproduced.

Applied the Humanizer skill to the manuscript passage. No nonlinear-moment
calculation or new tracking was performed; the excess remains unresolved and
Poisson/binomial deviations remain diagnostic. The audit executes in the project
environment and writes a new results directory, preserving old outputs. Final
claim identities and PDFs will be reconciled in R2F-BTS-06.
