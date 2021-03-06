# coding:utf-8
import sys

if __name__ == "__main__":
    filename = sys.argv[1]

    head = "instance_id,prob"
    fout = "ans.csv"
    print fout

    fout = open(fout, "w")
    print >> fout, head

    ans = []
    for i, l in enumerate(open(filename)):
        l = l.strip()
        items = l.split()
        assert len(items) == 3
        # if float(items[1]) <= 0.01:
        # items[1] = "0.01"
        ans += [[items[2], items[1]]]

    ans = sorted(ans, key=lambda x: x[0])
    for key, score in ans:
        print >> fout, key + ',' + score
