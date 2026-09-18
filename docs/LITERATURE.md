# Literature comparison and source scope

Checked 18 September 2026. This note distinguishes the paper's claims from the evidence actually inspected. It is not an exhaustive bibliography or a certificate of first priority.

## Exact source question

Svante Janson, *Simply generated trees, conditioned Galton–Watson trees, random allocations and condensation*, Probability Surveys 9 (2012), 103–252, DOI [10.1214/11-PS188](https://doi.org/10.1214/11-PS188).

The fixed-rank total-variation question is **Problem 19.10 in the publication**, **18.10 in arXiv:1112.0510v1**. The preceding paragraph also proposes joint approximation for finitely many upper ranks. The preprint's printed page 89 and the surrounding Theorem 18.7 were inspected, including the actual page image. The weaker fixed-tilt centering and mean-matched moving-law formulations are explicitly part of the source. The published numbering is also corroborated by Stufler's Remark 3.9.

The manuscript's allocation corollary addresses these formulations. Under a bounded central window, and for suitable mean-matched triangular arrays, it allows every `o(n)` ranks. In the weaker fixed-tilt regime it imposes the additional sufficient condition stated in Theorem 7.2. It does not claim every `o(n)` ranks in that regime without an extra condition. Problem 19.9, the sparse endpoint, is not answered.

## Closest comparisons

| Source | Material inspected | Relation and limitation |
|---|---|---|
| Arratia–Tavaré (1994), [arXiv:1308.3279](https://arxiv.org/abs/1308.3279) | Full author version; Sections 2–3, Theorem 3 and residual-sum formula (33), and vector/further-conditioning material in Section 8 | The conditional independent-process framework, likelihood-ratio strategy, sufficiency reductions, and use of vector constraints are established prior work. The paper credits them explicitly. The present asymptotic is specialized to finite-variance iid/row-iid observations selected by a rare value event and jointly observed with a sublinear prescribed block. |
| Diaconis–Freedman (1988), [10.1007/BF01048727](https://doi.org/10.1007/BF01048727) | Publisher abstract and bibliographic metadata; full article not obtained | Gives quantitative conditional approximations for predetermined coordinate blocks in exponential families under stated smoothness/moment hypotheses. It is a direct antecedent for the prescribed-block special case. The full article remains an outstanding theorem-by-theorem priority comparison. |
| Hsing (1995), [10.1016/0304-4149(95)00054-2](https://doi.org/10.1016/0304-4149(95)00054-2) | Publisher/search-indexed abstract and limited indexed text; complete article not obtained | A direct conceptual antecedent on sums and rare observations under weak dependence. The manuscript does not claim that the general phenomenon of asymptotic independence is new. Absence of a local-TV theorem from all of Hsing's results has not been established. |
| Stufler (2024), [arXiv:2204.06982](https://arxiv.org/abs/2204.06982) | Full preprint, dense-regime hypotheses, Lemma 3.5, Corollary 3.6, Remark 3.9 and relevant proof passages; image of the corollary page | A close growing-extremes total-variation theorem for Gibbs partitions with a random component count. The fixed-count setting and the full `o(n)` range here should not be conflated with that statement. The earlier result is prominently cited, not dismissed merely because its model differs. |
| Kortchemski–Vetter (2026), [arXiv:2607.22291v1](https://arxiv.org/abs/2607.22291v1) | Abstract, introduction, main pattern theorem and Lemma 4.2 in the full PDF | Rare fringe-subtree and declumped-pattern counts in conditioned trees, with local bridge-removal estimates and stable-domain cases beyond finite variance. These are multi-vertex patterns, not the entire iid-coordinate rare record. The present theorem is not advertised as subsuming that work. |
| Thévenin (2020), [arXiv:1812.07365](https://arxiv.org/abs/1812.07365), [10.1214/20-EJP465](https://doi.org/10.1214/20-EJP465) | Full preprint, introduction and principal fixed-outdegree count statements | Relevant to conditioned trees and prescribed degree/leaf counts. The new leaf-count corollary concerns the joint law of upper ranked degrees at central targets, not the functional count or tree-shape limits in this paper. |
| Armendáriz–Loulakis (2011), [arXiv:0912.1516](https://arxiv.org/abs/0912.1516), [10.1016/j.spa.2011.01.011](https://doi.org/10.1016/j.spa.2011.01.011) | Abstract, setup and Theorem 1 in the full preprint | Conditional sample laws at a subexponential large-deviation scale, with one large summand. This is an important contrasting regime; the present central-window theorem does not solve the condensation problem. |
| Li–Tan (2023), [arXiv:2312.09499v1](https://arxiv.org/abs/2312.09499v1) | Full preprint's abstract and joint-limit setup | Joint weak/asymptotic limit results for upper order statistics and partial sums. The cited version has two named authors. A later journal record was surfaced but its changed author metadata could not be checked directly, so the bibliography identifies exactly the preprint used rather than silently merging versions. |

## Standard ingredients and additional references

Holst (1979), *Two conditional limit theorems with applications*, DOI [10.1214/aos/1176344676](https://doi.org/10.1214/aos/1176344676), is cited as an earlier conditional-limit contribution. The metadata and scope, rather than a full theorem-level comparison, were checked.

The scalar local limit theorem is proved in the manuscript and compared with Janson's Lemma 14.1 and Remark 14.2 (13.1 and 13.2 in the preprint). The multivariate lemma uses the same classical Fourier method with its full-lattice hypothesis spelled out; it is not claimed as a new local central limit theorem.

The one-sided density step is attributed to Scheffé's convergence argument, *Annals of Mathematical Statistics* 18 (1947), 434–438, DOI [10.1214/aoms/1177730390](https://doi.org/10.1214/aoms/1177730390). Its elementary proof is included.

The Poisson step is classical. Barbour–Hall (1984), *On the rate of Poisson convergence*, *Math. Proc. Cambridge Philos. Soc.* 95(3), 473–480, DOI [10.1017/S0305004100061806](https://doi.org/10.1017/S0305004100061806), was bibliographically checked against the publisher. The exact bound used was checked in Theorem 1 of Arratia–Goldstein–Gordon (1990), *Poisson approximation and the Chen–Stein method*, *Statistical Science* 5(4), 403–434, from an author-hosted PDF, including the image of printed page 406. Their total-variation norm is twice the paper's convention. With independent indicators their theorem gives `(1-exp(-nq))*q` after that conversion. The Poisson approximation is applied after forgetting original sample labels.

The cyclic tree representation is credited to Dwass (1969), *The total progeny in a branching process and a related random walk*, *J. Appl. Probab.* 6(3), 682–686, DOI [10.1017/S0021900200026711](https://doi.org/10.1017/S0021900200026711), and to Janson's allocation/tree treatment. The particular cyclic proof needed here is included, so no unverified external lemma is a hidden dependency.

## Search outcome and what it does not establish

Searches used the exact source question and numbering, conditioned upper order statistics, rare records, sums and extreme values, conditional total variation, and the named closest antecedents. Several broad search responses were irrelevant; they are not evidence of absence. Direct primary-source comparisons, not the number of search hits, support the distinctions above.

No exact earlier theorem subsuming the full package was located in the primary material inspected. This supports presenting the precise theorems and their relationship to Janson's question. It does **not** justify an unconditional claim of first worldwide priority. In particular, the complete Hsing and Diaconis–Freedman articles were not obtained, and the newly written extensions have not received an independent specialist assessment. The manuscript accordingly avoids a claim that its conditioning method, its local limit theorem, or the general independence phenomenon was first discovered here.

The references in the manuscript are relevant to the problem statement, closely related results, standard proof ingredients, or the new applications. Third-party papers and copyrighted full texts are not included in this repository.
