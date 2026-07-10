import csv


def weierstrass_stats(path="ec_data_N100000_ap1229.csv"):
    w1_cnt = {0: 0, 1: 0}
    w2_cnt = {-1: 0, 0: 0, 1: 0}
    w3_cnt = {0: 0, 1: 0}
    n = 0
    with open(path) as f:
        for row in csv.DictReader(f):
            w1, w2, w3 = int(row["wa1"]), int(row["wa2"]), int(row["wa3"])
            w1_cnt[w1] += 1
            w2_cnt[w2] += 1
            w3_cnt[w3] += 1
            n += 1

    print("rows:", n)
    print(f"w1 counts: 0: {w1_cnt[0]} ({float(w1_cnt[0]/n*100):.1f}%), 1: {w1_cnt[1]} ({float(w1_cnt[1]/n*100):.1f}%)")
    print(f"w2 counts: -1: {w2_cnt[-1]} ({float(w2_cnt[-1]/n*100):.1f}%), 0: {w2_cnt[0]} ({float(w2_cnt[0]/n*100):.1f}%), 1: {w2_cnt[1]} ({float(w2_cnt[1]/n*100):.1f}%)")
    print(f"w3 counts: 0: {w3_cnt[0]} ({float(w3_cnt[0]/n*100):.1f}%), 1: {w3_cnt[1]} ({float(w3_cnt[1]/n*100):.1f}%)")


if __name__ == "__main__":
    weierstrass_stats()
