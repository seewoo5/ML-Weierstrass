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

The minimal reduced Weierstrass coefficients $w_1, w_2, w_3$ can be recovered from the Frobenius traces $a_2, a_3$ and the parity of conductor $N$. The following two checks verify this.

### `check_tree.py`

Python translation of the decision trees in `trees/*.tex` (`predict_w1`, `predict_w2`, a `mod`-based variant `predict_w2_mod`, and `predict_w3`), checked row-by-row against the downloaded dataset.

```
python3 check_tree.py
```

Expected output: every coefficient matches on all 437226 rows (100% accuracy for `wa1`, both `wa2` variants, and `wa3`).

### `check_formula.ipynb`

An executable Sage notebook containing the closed-form formulas (`compute_w1`, `compute_w2`, `compute_w3`) and three checks:

- Every stored Frobenius trace is independently validated. Each equation mod 2 or mod 3 is lifted to an elliptic curve over $\mathbb{Q}$; if the original integer coefficients are singular, the notebook adjusts $w_6$ by $\pm 2$ or $\pm 3$ without changing the reduction, then computes `E.ap(2)` or `E.ap(3)`.
- The formulas are checked exhaustively on all 32 equations mod 2 and all 108 reduced equations mod 3 used in the proof.
- `check_csv()` performs an extra row-by-row sanity check against `ec_data_N100000_ap1229.csv` when the dataset is present.

```
sage -n jupyter check_formula.ipynb
```

Select the SageMath 10.9 kernel and run all cells. Expected output: all 32 stored $a_2$ values and all 108 stored $a_3$ values pass the lift checks, every finite formula check passes, and all 437226 dataset rows pass the optional CSV check.


### `weierstrass_dist.py`

Compute distribution of Weierstrass coefficients $w_1, w_2, w_3$ in the downloaded dataset. 

```
python3 weierstrass_dist.py
```

Expected output:
```
w1 counts: 0: 219952 (50.3%), 1: 217274 (49.7%)
w2 counts: -1: 154308 (35.3%), 0: 154994 (35.4%), 1: 127924 (29.3%)
w3 counts: 0: 283609 (64.9%), 1: 153617 (35.1%)
```