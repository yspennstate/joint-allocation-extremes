# Rare observations under lattice-sum conditioning and joint allocation extremes

**Yitzchak Shmalo** — Einstein Institute of Mathematics, The Hebrew University of Jerusalem.

[Read the paper](paper/main.pdf) · [LaTeX source](paper/main.tex) · [Literature comparison](docs/LITERATURE.md) · [Proof and verification notes](docs/VERIFICATION.md)

## Results

For a finite-variance lattice sample, conditioning its sum at an attainable point in a bounded central-limit window asymptotically preserves the complete indexed record of any deterministic rare event, in total variation. The expected number of rare observations need not stay bounded.

The paper proves a triangular-array version, joint approximation with a prescribed `o(n)`-coordinate block under finitely many lattice constraints, and the following consequences:

- Joint approximation of any `o(n)` upper order statistics, with counterexamples at a positive fraction of ranks.
- Independent-Poisson approximation of the entire vector of rare-value counts, including diverging total intensity. This Poisson approximation forgets original sample labels.
- Weighted-allocation and conditioned-tree applications, including an additional central leaf-count constraint.

The allocation theorem answers the assertion posed in Janson's published **Problem 19.10** (Problem 18.10 in the 2011 preprint) and its proposed finite-dimensional joint extension. All source centering variants are separated. The paper does not address the adjacent sparse-allocation question, infinite-variance limits, or arbitrary noncentral conditioning.

The precise contribution is distinguished from established conditional-process methods, fixed-coordinate approximations, and Gibbs-partition results. The comparison in `docs/LITERATURE.md` records the sources actually inspected and remaining access limitations; no exhaustive worldwide priority certificate or independent human peer review is claimed.

## Reproduce

From the repository root:

```sh
python3 code/verify.py --output code/checks.json
python3 code/verify_extensions.py --output code/extension_checks.json
make paper
```

Python 3.10 or later and a standard pdfLaTeX distribution are sufficient. Both verification programs use only the Python standard library. The article uses `amsart`, Latin Modern, `microtype`, `mathtools`, `booktabs`, `geometry`, `hyperref`, and `enumitem`.

`make paper` compiles `paper/main.tex` twice. The accompanying section files and `references.tex` must remain beside it. The exact checks verify finite identities, not the limiting theorems.

## Files

`paper/` contains the manuscript PDF and its complete LaTeX source. `code/` contains executable checks and recorded results. `docs/` records the source comparison and verification boundary. `CITATION.cff` supplies citation metadata. The source archive is a convenience snapshot; the readable files are the working source.

The acknowledgements, funding, competing-interest declaration, and AI contribution statement are in the manuscript. No empirical data or third-party article PDFs are distributed here.
