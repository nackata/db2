from ui import UiMenu

from inspect import signature


class MainController(object):
    @staticmethod
    def makeChoosing(menu_list: list, name_menu: str):
        try:
            UiMenu.display_ui(menu_list, name_menu)
            return MainController.get_men_value(": ", len(menu_list))
        except Exception as e:
            UiMenu.show_err(str(e))

    @staticmethod
    def consider_chosing(controller, choosing: int, listing_func: list):
        try:
            if choosing > len(listing_func) - 1:
                raise Exception("func does not existing")

            desiredFunc = listing_func[choosing]
            desiredFunc(controller)
        except Exception as e:
            UiMenu.show_err(str(e))

    @staticmethod
    def get_func_arguments(function, amount_miss_arguments=0) -> list:
        from configuration import params
        params = signature(function).parameters

        args = []
        paramLength = len(params)
        for i in range(paramLength - amount_miss_arguments):
            args.append(MainController.get_vale(
                f" Please, enter {list(params)[i]}{params[list(params)[i]] if list(params)[i] in params else ''}: ",
                str))

        return args

    @staticmethod
    def get_men_value(msg: str, top_line: int = None):
        while True:
            numb = input(msg)

            if numb.isdigit():
                numb = int(numb)
                if top_line is None or 0 <= numb < top_line:
                    return numb

    @staticmethod
    def get_vale(msg: str, variant):
        while True:
            try:
                userInput = input(msg)
                if variant == str:
                    if len(userInput) != 0:
                        return variant(userInput)
                else:
                    return variant(userInput)
            except Exception as e:
                UiMenu.show_err(str(e))

    @staticmethod
    def looping(controller):
        controller.looping = False
