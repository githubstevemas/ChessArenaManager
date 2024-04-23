from tabulate import tabulate


def print_table(datas):
    table = tabulate(datas, headers="keys", tablefmt="rounded_grid", numalign="center", stralign="center")
    print(table)


def print_rounds(tournament):

    for i in range(len(tournament["tournament list"])):
        print(f"\nRound {i + 1} :\n")
        round_table = tabulate(tournament["tournament list"][i], headers="keys", tablefmt="rounded_grid", numalign="center", stralign="center")
        print(round_table)


def print_players(players_list):
    headers = ["Fist name", "Last name", "id", "score"]
    table = tabulate(players_list, headers=headers, tablefmt="rounded_grid", numalign="center", stralign="center")
    print(table)
