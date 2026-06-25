# Predicting Weierstrass coefficients of elliptic curves

## Install dependencies

You need to install [Sage](https://www.sagemath.org/) first.

```
sage --python -m pip install polars-lts-cpu tqdm scikit-learn matplotlib
sage --python -m pip install -U "lmfdb-lite[pgbinary] @ git+https://github.com/roed314/lmfdb-lite.git"
```


## Download data

This will download elliptic curve data from LMFDB, 437226 isogeny classes up to conductor $\le 10^5$, including label, Weierstrass coefficients, conductor, rank, and the Frobenius traces $a_p$ for $p \le 10^4$ (total 1229 primes).
It may take about an hour.

```
sage download_data.sage
```


## Run experiments

Run `predict_weierstrass.ipynb` with Sage kernel.


## Verifying the predictors

The minimal reduced Weierstrass coefficients $w_1, w_2, w_3$ (i.e. $a_1, a_2, a_3$, with $a_1, a_3 \in \{0, 1\}$ and $a_2 \in \{-1, 0, 1\}$) can be recovered from the Frobenius traces $a_2, a_3$ and the conductor $N$. Two scripts check this.

### `check_tree.py`

Python translation of the decision trees in `trees/*.tex` (`predict_w1`, `predict_w2`, a `mod`-based variant `predict_w2_mod`, and `predict_w3`), checked row-by-row against the downloaded dataset.

```
python3 check_tree.py
```

Expected output: every coefficient matches on all 437226 rows (100% accuracy for `wa1`, both `wa2` variants, and `wa3`).

### `check_formula.sage`

Closed-form formulas (`compute_w1`, `compute_w2`, `compute_w3`) plus two checks:

- `prove_mod6()`: exhaustive proof over all $6^5$ Weierstrass models $[a_1, a_2, a_3, a_4, a_6]$ taken mod 6. For each nonsingular model Sage computes the ground truth ($a_2$, $a_3$, $N$, and the global minimal model) and compares it to the formulas.
- `check_csv()`: extra sanity check against the dataset (skipped if absent).

```
sage check_formula.sage
```

Expected output: `0` mismatches over the 7691 nonsingular models mod 6, all 437226 dataset rows correct, and `OVERALL: PASS`.