import os
from src.controller.main_ctrl import Controller

DATAS_PATH = "datas/tournaments"


def main():

    if not os.path.exists(DATAS_PATH):
        os.makedirs(DATAS_PATH)

    Controller().main_menu()


if __name__ == "__main__":
    main()
