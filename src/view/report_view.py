from tabulate import tabulate


class Table:
    def __init__(self):
        pass

    def print_table(self, datas):

        table = tabulate(datas, headers="keys", tablefmt="rounded_grid", numalign="center", stralign="center")
        print(table)
