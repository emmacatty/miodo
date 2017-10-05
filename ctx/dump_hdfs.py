# coding:utf-8
from common import *


def dump():
    # dirname = "/user/h_miui_ad/dev/wwxu/exp/tf/rfrecord/base/date=%2d"
    # dirname = "/user/h_miui_ad/dev/wwxu/exp/tf/rfrecord/opt5_1/date=%2d"
    # dirname = "/user/h_miui_ad/dev/wwxu/exp/tf/rfrecord/opt8_100/date=%2d"
    # dirname = "/user/h_miui_ad/dev/wwxu/exp/tf/rfrecord/opt9_0"
    dirname = "/user/h_miui_ad/dev/wwxu/exp/tf/rfrecord/dw/opt3_merged_30_100"
    dirname += '/date=%2d'
    date = range(11, 31) + range(32, 34)
    # date = range(11, 24)

    print date
    prefix = "hadoop --cluster c3prc-hadoop fs -get "
    top_dir = dirname.split("/")[-2]
    print top_dir
    if not os.path.exists(top_dir):
        os.mkdir(top_dir)
    os.chdir(top_dir)
    for d in date:
        cmd = prefix + dirname % d
        print time.ctime(), cmd
        ret = os.system(cmd)
        print ret


if __name__ == "__main__":
    dump()
    pass
