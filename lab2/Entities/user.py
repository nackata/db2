import atexit
from Entities.MainController import MainController

from ui import UiMenu
import colorama
from colorama import Fore
from RedisServer.RedisServer import Redis


class UsrController(object):
    def __init__(self):
        self.redisServ = Redis()
        self.uiMenu = 'Main ui'
        self.curUser = -1
        self.looping = True
        atexit.register(self.make_sign_out)
        self.launch()

    def launch(self):
        from configuration import menu_listing
        try:
            while self.looping:
                choosing = MainController.makeChoosing(menu_listing[self.uiMenu].keys(), self.uiMenu)
                MainController.consider_chosing(self, choosing, list(menu_listing[self.uiMenu].values()))

        except Exception as e:
            UiMenu.show_err(str(e))

    def make_register(self):
        uname=self.redisServ.make_register(*MainController.get_func_arguments(self.redisServ.make_register))
        colorama.init()
        print(Fore.GREEN + "\n Registration proceeded) " + Fore.RESET)

    def make_signin(self):
        user_id = self.redisServ.make_signin(*MainController.get_func_arguments(self.redisServ.make_signin))
        self.curUser = user_id
        self.uiMenu = 'User ui'
        print(Fore.GREEN + f"\n Logged in " + Fore.RESET)
    def inbox_messeges(self):
        msgs = self.redisServ.recieve_msg(self.curUser)
        UiMenu.show_lst("-" * 130 + "\n Messages list ", msgs)

    def recieve_stats(self):
        stats = self.redisServ.recieve_stats(self.curUser)
        UiMenu.show_itm(stats)

    def make_sign_out(self):
        if self.curUser != -1:
            self.redisServ.make_sign_out(self.curUser)
            self.uiMenu = 'Main ui'
            self.curUser = -1

    def send_a_message(self):
        self.redisServ.create_mess(*MainController.get_func_arguments(self.redisServ.create_mess, 1),
                                   self.curUser)


