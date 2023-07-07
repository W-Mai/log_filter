import re
import argparse


class LogParser(object):
    def __init__(self, path):
        self.path = path

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

    def find(self, date=None, tid=None, core=None, extra=None, type=None, content=None):
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

    def print(self):
        pass

    def __str__(self):
        return str({
            "path": self.path,
            "reg": self.reg_compiled
        })

    def __repr__(self):
        return str(self)


def parse_arg() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Log Parser')
    parser.add_argument('path', type=str, help='Path to log file')
    parser.add_argument('-d', '--date', type=str, help='Date')
    parser.add_argument('-i', '--tid', type=str, help='Thread ID')
    parser.add_argument("-c", '--core', type=str, help='Core')
    parser.add_argument('-e', '--extra', type=str, help='Extra')
    parser.add_argument('-t', '--type', type=str, help='Type')
    parser.add_argument('-x', '--content', type=str, help='Content')

    parser.add_argument('-a', '--all-categories', action='store_true', help='Get all categories')
    return parser.parse_args()


def main():
    args = parse_arg()
    print(args)
    log_parser = LogParser(args.path)
    log_parser.parse()


if __name__ == "__main__":
    main()
