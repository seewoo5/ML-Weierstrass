r"""
Python translation of the decision trees in trees/*.tex and a checker that
verifies them against ec_data_N100000_ap1229.csv.

Forest convention used in the .tex files:
  [node  [first child = YES branch]  [second child = NO branch]]
so the first listed child is taken when the node's test is TRUE.

Inputs used:
  a2 = a_0002  (trace of Frobenius at 2)
  a3 = a_0003  (trace of Frobenius at 3)
  Nbar = conductor % 2   (the \overline{N} node in w3.tex)
"""
import csv


# --- w1.tex : predict w1 from a2 -------------------------------------------
def predict_w1(a2):
    if a2 <= 0:
        if a2 <= -1:
            if a2 == -2:
                return 0
            else:            # a2 == -1
                return 1
        else:                # a2 == 0
            return 0
    else:                    # a2 >= 1
        if a2 <= 1:          # a2 == 1
            return 1
        else:                # a2 >= 2
            return 0

# --- w2.tex (first tree) : predict w2 from a2 and a3 -----------------------
def predict_w2(a2, a3):
    if a3 <= 0:
        if a3 <= -1:
            if a3 <= -2:
                if a3 <= -3:
                    if a2 <= 0:
                        if a2 <= -1:
                            if a2 <= -2:
                                return 0
                            else:            # a2 == -1
                                return -1
                        else:                # a2 == 0
                            return 0
                    else:                    # a2 >= 1
                        if a2 <= 1:          # a2 == 1
                            return -1
                        else:                # a2 >= 2
                            return 0
                else:                        # a3 == -2
                    if a2 <= 0:
                        if a2 <= -1:
                            if a2 <= -2:
                                return 1
                            else:            # a2 == -1
                                return 0
                        else:                # a2 == 0
                            return 1
                    else:                    # a2 >= 1
                        if a2 <= 1:          # a2 == 1
                            return 0
                        else:                # a2 >= 2
                            return 1
            else:                            # a3 == -1
                if a2 <= -1:
                    if a2 <= -2:
                        return -1
                    else:                    # a2 == -1
                        return 1
                else:                        # a2 >= 0
                    if a2 <= 0:              # a2 == 0
                        return -1
                    else:                    # a2 >= 1
                        if a2 <= 1:          # a2 == 1
                            return 1
                        else:                # a2 >= 2
                            return -1
        else:                                # a3 == 0
            if a2 <= -1:
                if a2 <= -2:
                    return 0
                else:                        # a2 == -1
                    return -1
            else:                            # a2 >= 0
                if a2 <= 0:                  # a2 == 0
                    return 0
                else:                        # a2 >= 1
                    if a2 <= 1:              # a2 == 1
                        return -1
                    else:                    # a2 >= 2
                        return 0
    else:                                    # a3 >= 1
        if a3 <= 1:                          # a3 == 1
            if a2 <= 0:
                if a2 <= -1:
                    if a2 <= -2:
                        return 1
                    else:                    # a2 == -1
                        return 0
                else:                        # a2 == 0
                    return 1
            else:                            # a2 >= 1
                if a2 <= 1:                  # a2 == 1
                    return 0
                else:                        # a2 >= 2
                    return 1
        else:                                # a3 >= 2
            if a3 <= 2:                      # a3 == 2
                if a2 <= -1:
                    if a2 <= -2:
                        return -1
                    else:                    # a2 == -1
                        return 1
                else:                        # a2 >= 0
                    if a2 <= 0:              # a2 == 0
                        return -1
                    else:                    # a2 >= 1
                        if a2 <= 1:          # a2 == 1
                            return 1
                        else:                # a2 >= 2
                            return -1
            else:                            # a3 >= 3
                if a2 <= -1:
                    if a2 <= -2:
                        return 0
                    else:                    # a2 == -1
                        return -1
                else:                        # a2 >= 0
                    if a2 <= 0:              # a2 == 0
                        return 0
                    else:                    # a2 >= 1
                        if a2 <= 1:          # a2 == 1
                            return -1
                        else:                # a2 >= 2
                            return 0


# --- w2.tex (second tree) : predict w2 from (a2 mod 2) and (a3 mod 3) -------
def predict_w2_mod(a2, a3):
    a2b = a2 % 2        # in {0, 1}
    a3b = a3 % 3        # in {0, 1, 2}
    if a3b == 0:
        if a2b == 0:
            return 0
        else:                   # a2b != 0
            return -1
    else:                       # a3b != 0
        if a3b <= 1:            # a3b == 1
            if a2b == 0:
                return 1
            else:               # a2b != 0
                return 0
        else:                   # a3b == 2
            if a2b == 0:
                return -1
            else:               # a2b != 0
                return 1

# --- w3.tex : predict w3 from Nbar(=conductor%2), a2 and w2 ----------------
def predict_w3(Nbar, a2, w2):
    if Nbar == 0:
        if a2 <= 0:
            if a2 <= -1:
                if w2 == -1:
                    return 0
                else:
                    if w2 <= 0:             # w2 == 0
                        return 1
                    else:                   # w2 >= 1
                        return 0
            else:                           # a2 == 0
                return 0
        else:                               # a2 >= 1
            if w2 == -1:
                return 1
            else:
                if w2 <= 0:                 # w2 == 0
                    return 0
                else:                       # w2 >= 1
                    return 1
    else:                                   # Nbar == 1
        if a2 <= 0:
            if a2 <= -1:
                if w2 == -1:
                    return 1
                else:
                    if w2 <= 0:             # w2 == 0
                        if a2 == -2:
                            return 1
                        else:
                            return 0
                    else:                   # w2 >= 1
                        return 1
            else:                           # a2 == 0
                return 1
        else:                               # a2 >= 1
            if a2 <= 1:                     # a2 == 1
                if w2 == -1:
                    return 0
                else:
                    if w2 <= 0:             # w2 == 0
                        return 1
                    else:                   # w2 >= 1
                        return 0
            else:                           # a2 >= 2
                return 1


def main():
    path = "ec_data_N100000_ap1229.csv"
    n = 0
    ok1 = ok2 = ok2m = ok3 = 0
    # w3 using the *true* wa2 vs the *predicted* w2
    ok3_truew2 = 0
    with open(path) as f:
        for row in csv.DictReader(f):
            a2 = int(row["a_0002"])
            a3 = int(row["a_0003"])
            Nbar = int(row["conductor"]) % 2
            w1, w2, w3 = int(row["wa1"]), int(row["wa2"]), int(row["wa3"])

            p1 = predict_w1(a2)
            p2 = predict_w2(a2, a3)
            p2m = predict_w2_mod(a2, a3)
            p3 = predict_w3(Nbar, a2, p2)        # full pipeline (uses predicted w2)
            p3t = predict_w3(Nbar, a2, w2)       # uses ground-truth w2

            ok1 += (p1 == w1)
            ok2 += (p2 == w2)
            ok2m += (p2m == w2)
            ok3 += (p3 == w3)
            ok3_truew2 += (p3t == w3)
            n += 1

    print(f"rows: {n}")
    print(f"wa1 accuracy: {ok1}/{n} = {ok1/n:.4%}")
    print(f"wa2 accuracy (tree 1, a2 & a3)       : {ok2}/{n} = {ok2/n:.4%}")
    print(f"wa2 accuracy (tree 2, a2%2 & a3%3)   : {ok2m}/{n} = {ok2m/n:.4%}")
    print(f"wa3 accuracy (pipeline, predicted w2): {ok3}/{n} = {ok3/n:.4%}")
    print(f"wa3 accuracy (using true w2)         : {ok3_truew2}/{n} = {ok3_truew2/n:.4%}")


if __name__ == "__main__":
    main()
