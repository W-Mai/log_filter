import re
import argparse


class LogParser(object):
    def __init__(self, path):
        self.path = path
        # self.log_reg = log_reg

        self.reg_compiled = re.compile(
            r"("
            r"\[(?P<DATE>[0-9]+/[0-9]+ [0-9]+:[0-9]+:[0-9]+)] "
            r"\[(?P<TID>[0-9]+?)] "
            r"\[(?P<CORE>.*?)] "
            r"(\[(?P<EXTRA>.*?)])?"
            r"\[(?P<TYPE>.*?)]"
            r"(?P<CONTENT>.*$)\n"
            r")?")

        self._log_parsed = []

    def parse(self):
        with open(self.path, "r") as f:
            for line in f.readlines():
                res = self.reg_compiled.match(line)
                self._log_parsed.append(res.groupdict())

    def get_all_categories(self):
        # categories = {
        #     "core": {
        #         "name": "core",
        #         "tid": {
        #             "id": 1,
        #             "type": {
        #                 "type": "widget",
        #             }
        #         }
        #     },
        # }

        categories = {}

        for log in self._log_parsed:
            core = log["CORE"]
            tid = log["TID"]
            typ = log["TYPE"]

            if core is None or tid is None or typ is None:
                continue

            if core not in categories:
                categories[core] = {
                    "tid": {}
                }

            if tid not in categories[core]["tid"]:
                categories[core]["tid"][tid] = {
                    "type": []
                }

            if typ not in categories[core]["tid"][tid]["type"]:
                categories[core]["tid"][tid]["type"].append(typ)

        return categories

    def get(self, date=None, tid=None, core=None, extra=None, type=None, content=None):
        def filter_cb(x):
            can_keep = True
            if date is not None:
                can_keep = can_keep and x["DATE"] == date
            if tid is not None:
                can_keep = can_keep and x["TID"] == tid
            if core is not None:
                can_keep = can_keep and x["CORE"] == core
            if extra is not None:
                can_keep = can_keep and x["EXTRA"] == extra
            if type is not None:
                can_keep = can_keep and x["TYPE"] == type
            return can_keep

        return filter(filter_cb, self._log_parsed)

    def save(self):
        pass

    def print(self):
        pass

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path


l = LogParser("test.log")
l.parse()

res = l.get(core="ap", type="WIDGETLOG")
for r in res:
    print(r["CONTENT"])
