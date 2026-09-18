# Proof and verification notes

Date: 18 September 2026.

## Analytic dependency map

The scalar record theorem (Theorem 2.1) uses the uniform local central limit theorem (Lemma 3.1), the exact conditional density (Lemma 4.1), the centered removed-sum identity (4.8), and the normalized one-sided density identity (Lemma 4.3). The local-limit proof is included and requires only uniform square integrability, a nondegenerate limiting law, and a common maximal lattice.

The rank theorem (Theorem 5.1) chooses a tail with probability tending to zero but expected count much larger than the number of retained ranks. Sorting is applied to one common record map. Support gaps and ties do not require continuity assumptions. The weak-centering proof (Theorem 7.2) instead compares censored samples under nearby exponential tilts, charging upper overflow separately and padding at the boundary atom.

The Poisson theorem (Theorem 8.1) combines the scalar result with the classical binomial–Poisson bound. It compares value counts, not Poisson processes on original sample labels. The binomial and Poisson totals share the same conditional marking law, giving equality of their total-variation distances with those of the corresponding marked counts.

The multiconstraint theorem (Theorem 9.1) observes both a deterministic `o(n)` block and the rare record outside it. It uses an explicitly proved vector local estimate (Lemma 9.2). The hypothesis that support differences generate the whole integer lattice excludes extra Fourier periods. The centered revealed contribution has second moment `o(n)`. The same negative-part argument converts the uniform likelihood ratio into total variation.

For the leaf-count application (Corollaries 9.4–9.5), the observation vector is `(X, 1_{X=0})`. Positivity of `p0,p1,p2` gives a full two-dimensional lattice and a positive-definite covariance matrix. The cycle lemma preserves the degree multiset and the number of leaves. It does not preserve iid coordinate labels as depth-first locations.

The two sharpness examples in Section 10 are analytic: a sparse-positive law lets a positive fraction of ranks recover the whole sum, and a geometric law separates fixed and moving tilts on the `1/log n` scale.

## Checks performed in this release

The supplied programs were executed, not merely inspected. Every rational identity tested passed.

| Program | Exact checked quantities |
|---|---|
| `code/verify.py` | 7,411 product configurations; 38,871 conditional-density equalities; 1,024 tilt equalities; 4,706 degree words; 891 centering identities; 48,710 threshold-padding identities |
| `code/verify_extensions.py` | 2,816 vector configurations; 23,102 vector conditional-density equalities; 5,632 vector centering identities; 192 attainable conditioning totals; 35,888 rotations in 28 leaf-count classes; two common-marking total-variation equalities |

The extension tests include negative vector coordinates, empty rare sets, non-tail rare sets, dimensions two and three, and both empty and nonempty prescribed blocks. Every attainable vector total in each finite model is tested. The centered revealed-sum second moment is checked against its exact independent-summand expression as well as the upper bound used in the proof.

These are finite algebraic and combinatorial checks. They are not a proof of a central limit theorem, a finite-sample asymptotic rate, a proof-assistant certificate, a literature-priority certificate, or independent human review.

## Source and preparation boundary

The scalar manuscript, its censoring argument, and its original verification code were recovered from the author's existing manuscript package. Earlier research records also contain fixed-rank rare-cloud and direct-conditioning proofs. This release includes a new written vector/block proof and the displayed Poisson and leaf-count consequences, together with new exact tests and an expanded literature comparison.

The mathematical review in this preparation was performed by the same AI assistant that made these additions. No independent human mathematical review or end-to-end formal verification has been performed. The manuscript's contribution declaration records this boundary directly.
