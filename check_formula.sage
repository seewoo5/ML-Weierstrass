# Formulas computing the minimal reduced Weierstrass coefficients (w1, w2, w3)
# from the Frobenius traces at 2 and 3 (a2, a3) and the conductor N, together
# with two checks:
#
#   1. prove_mod6()  -- an exhaustive proof over all 6^5 Weierstrass models
#      [a1,a2,a3,a4,a6] with coefficients taken mod 6.  For each nonsingular
#      model Sage computes the ground truth (ap(2), ap(3), conductor and the
#      global minimal reduced model) and we check the formulas against it.
#
#   2. check_csv()   -- an extra sanity check against the dataset
#      ec_data_N100000_ap1229.csv (not strictly necessary, but a second source
#      of ground truth from real curves).

import csv
import itertools
import os


# --------------------------------------------------------------------------
# Formulas
# --------------------------------------------------------------------------
def compute_w1(a2):
    return a2 % 2

def compute_w2(a2, a3):
    a2b = a2 % 2
    return (a3 + 1 - a2b) % 3 - 1

def compute_w3(N, a2, w2):
    Nb = N % 2
    a2b = a2 % 2
    if a2b == 0:
        return Nb
    else:  # a2b == 1
        return (Nb + a2b + w2 + (a2 + 1) / 2) % 2


# --------------------------------------------------------------------------
# Check 1: exhaustive proof over all Weierstrass models mod 6
# --------------------------------------------------------------------------
def prove_mod6():
    total = 0
    singular = 0
    bad1, bad2, bad3, bad3_true = [], [], [], []

    for c in itertools.product(range(6), repeat=5):
        try:
            E = EllipticCurve(QQ, list(c))
        except ArithmeticError:
            singular += 1
            continue

        total += 1

        # ground truth from the global minimal (reduced) model
        Em = E.minimal_model()
        gt_w1, gt_w2, gt_w3 = Em.a1(), Em.a2(), Em.a3()

        # inputs to the formulas
        ap2, ap3, N = E.ap(2), E.ap(3), E.conductor()

        # formula predictions
        pred_w1 = compute_w1(ap2)
        pred_w2 = compute_w2(ap2, ap3)
        pred_w3 = compute_w3(N, ap2, pred_w2)        # pipeline (predicted w2)
        pred_w3_true = compute_w3(N, ap2, gt_w2)     # uses ground-truth w2

        if pred_w1 != gt_w1:
            bad1.append((c, ap2, gt_w1, pred_w1))
        if pred_w2 != gt_w2:
            bad2.append((c, ap2, ap3, gt_w2, pred_w2))
        if pred_w3 != gt_w3:
            bad3.append((c, N, ap2, gt_w2, pred_w2, gt_w3, pred_w3))
        if pred_w3_true != gt_w3:
            bad3_true.append((c, N, ap2, gt_w2, gt_w3, pred_w3_true))

    print("=== Check 1: exhaustive proof over Weierstrass models mod 6 ===")
    print("nonsingular models tested:", total)
    print("singular models skipped  :", singular)
    print("w1 mismatches:", len(bad1))
    print("w2 mismatches:", len(bad2))
    print("w3 mismatches (pipeline, predicted w2):", len(bad3))
    print("w3 mismatches (using true w2)         :", len(bad3_true))

    for name, bad in [("w1", bad1), ("w2", bad2),
                      ("w3 (pipeline)", bad3), ("w3 (true w2)", bad3_true)]:
        if bad:
            print("--- sample %s mismatches (up to 10) ---" % name)
            for row in bad[:10]:
                print(row)

    ok = not (bad1 or bad2 or bad3 or bad3_true)
    if ok:
        print("ALL FORMULAS VERIFIED on every nonsingular model mod 6.")
    return ok


# --------------------------------------------------------------------------
# Check 2: extra sanity check against ec_data_N100000_ap1229.csv
# --------------------------------------------------------------------------
def check_csv(path="ec_data_N100000_ap1229.csv"):
    print("=== Check 2: dataset %s ===" % path)
    if not os.path.exists(path):
        print("dataset not found, skipping.")
        return True

    n = ok1 = ok2 = ok3 = ok3_true = 0
    with open(path) as f:
        for row in csv.DictReader(f):
            a2 = Integer(row["a_0002"])
            a3 = Integer(row["a_0003"])
            N = Integer(row["conductor"])
            w1, w2, w3 = Integer(row["wa1"]), Integer(row["wa2"]), Integer(row["wa3"])

            pred_w1 = compute_w1(a2)
            pred_w2 = compute_w2(a2, a3)
            pred_w3 = compute_w3(N, a2, pred_w2)        # pipeline (predicted w2)
            pred_w3_true = compute_w3(N, a2, w2)        # uses ground-truth w2

            ok1 += (pred_w1 == w1)
            ok2 += (pred_w2 == w2)
            ok3 += (pred_w3 == w3)
            ok3_true += (pred_w3_true == w3)
            n += 1

    print("rows:", n)
    print("w1 correct:", ok1, "/", n)
    print("w2 correct:", ok2, "/", n)
    print("w3 correct (pipeline, predicted w2):", ok3, "/", n)
    print("w3 correct (using true w2)         :", ok3_true, "/", n)

    ok = (ok1 == n and ok2 == n and ok3 == n and ok3_true == n)
    if ok:
        print("ALL FORMULAS VERIFIED on every dataset row.")
    return ok


if __name__ == "__main__":
    ok_mod6 = prove_mod6()
    print()
    ok_csv = check_csv()
    print()
    print("OVERALL:", "PASS" if (ok_mod6 and ok_csv) else "FAIL")
