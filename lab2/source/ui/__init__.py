from colorama import Fore, Style


class UiMenu(object):
    @staticmethod
    def display_ui(menu_listing, name_menu: str):
        print("\n" + "-" * 130)
        print(Fore.BLUE + f"      {name_menu}  ")
        print(Fore.BLACK + "|" * 130)
        numb = 0
        for itm in menu_listing:
            print(Fore.BLACK + f" Type {numb} to choose {itm}")
            numb += 1
        print(Fore.BLACK + "|" * 130)

    @staticmethod
    def show_itm(itm):
        print(f"\n{itm}")

    @staticmethod
    def show_itms(itms: list):
        counter = 1
        for itm in itms:
            print(f"  {counter} - {itm}")
            counter += 1

    @staticmethod
    def show_err(err: str):
        print(Fore.RED + f" Error occurred {err}")
        print(Style.RESET_ALL)

    @staticmethod
    def show_txt(txt: str):
        print(txt)

    @staticmethod
    def show_line():
        print(' ~' * 130)

    @staticmethod
    def show_lst(listName, lst):
        print(listName)
        counter = 1
        for item in lst:
            print(f" №{counter}.  {item}")
            counter += 1
        print('-' * 130)
