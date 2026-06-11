import polars as pl
from tqdm import tqdm

from lmf import db


ec_db = db.ec_curvedata

def query_data(N1, N2, r=None):
    # Elliptic curves over Q of conductor N1 <= N <= N2
    if r is None:
        return ec_db.search({"conductor": {"$gte": N1, "$lte": N2}})
    return ec_db.search({"conductor": {"$gte": N1, "$lte": N2}, "rank": r})

def get_df(max_N=10^5, num_ap=1229, save_csv=False):
    """
    Get a polars dataframe of elliptic curves over Q of conductor up to max_N,
    including the first num_ap coefficients a_p of the L-series.
    If save_csv is True, save the dataframe to a CSV file.
    """
    data = list(query_data(1, max_N))
    pmax = Primes()[num_ap - 1]
    isog_labels = set()

    # Use `wa1`, `wa2`, `wa3` for a1, a2, a3 of Weierstrass form
    # to avoid confusion with ap coefficients
    columns = ["isog_label", "wa1", "wa2", "wa3", "conductor", "rank"]
    for p in Primes()[:num_ap]:
        columns.append(f"a_{p:04d}")
    df = None

    for ec in tqdm(data):
        if ec['lmfdb_iso'] in isog_labels:  # one per isogeny class
            continue
        isog_labels.add(ec['lmfdb_iso'])
        ec_sage = EllipticCurve(QQ, ec['ainvs'])
        aps = list(ec_sage.aplist(pmax))
        wa1 = ec['ainvs'][0]
        wa2 = ec['ainvs'][1]
        wa3 = ec['ainvs'][2]
        conductor = ec['conductor']
        rank = ec['rank']
        row = [ec['lmfdb_iso'], wa1, wa2, wa3, conductor, rank] + aps
        if df is None:
            df = pl.DataFrame([row], schema=columns)
        else:
            df.extend(pl.DataFrame([row], schema=columns))

    if save_csv:
        df.write_csv(f"ec_data_N{max_N}_ap{num_ap}.csv")
    return df

df = get_df(max_N=10^5, num_ap=1229, save_csv=True)
print(df.head())
print(len(df))
