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