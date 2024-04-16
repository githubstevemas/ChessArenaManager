from tabulate import tabulate


def print_table(datas):
    table = tabulate(datas, headers="keys", tablefmt="rounded_grid", numalign="center", stralign="center")
    print(table)
