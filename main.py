import os
from src.controller.main_ctrl import Controller

DATAS_PATH = "datas/tournaments"

if __name__ == "__main__":

    if not os.path.exists(DATAS_PATH):
        os.makedirs(DATAS_PATH)

    main = Controller()
    main.main_menu()
