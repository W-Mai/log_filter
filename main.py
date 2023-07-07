import re
import argparse

reg_script = re.compile(
    r"\[(?P<DATE>[0-9]+/[0-9]+ [0-9]+:[0-9]+:[0-9]+)] "
    r"\[(?P<TID>[0-9]+?)] "
    r"\[(?P<CORE>.*?)] "
    r"\[(?P<TYPE>.*?)] "
    r".*$\n",
    flags=re.MULTILINE)

with open("test.log", "r") as f:
    script = f.read()

    res = reg_script.findall(script)
    print(len(res))
    exit(0)
    for r in res:
        print(r)
