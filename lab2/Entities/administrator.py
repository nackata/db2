from RedisServer.RedisServer import Redis
from ui import UiMenu
from source.Entities.MainController import MainController
from RedisServer.EventListener import EventListener


class Administrator(object):
    def __init__(self):
        self.redisServer = Redis()

        self.eventListener = EventListener()

        self.eventListener.launch()
        self.launch()
        self.looping = True


    def launch(self):
        from configuration import menu_listing
        try:
            menu = "Admin ui"
            while self.looping:
                choose = MainController.makeChoosing(menu_listing[menu].keys(), menu)
                MainController.consider_chosing(self, choose, list(menu_listing[menu].values()))
        except Exception as e:
            UiMenu.show_err(str(e))


    def recieve_events(self):
        recievedEvents = self.eventListener.recieve_events()
        UiMenu.show_lst("Events: ", recievedEvents)

    def recieve_active_users(self):
        active_users = self.redisServer.recieve_active_users()
        UiMenu.show_lst("Online users: ", active_users)

    def recieve_senders(self):
        senders = self.redisServer.recieve_senders(
            *MainController.get_func_arguments(self.redisServer.recieve_senders))
        UiMenu.show_lst("Most senders: ", senders)

    def recieve_spamers(self):
        spamers = self.redisServer.recieve_spamers(
            *MainController.get_func_arguments(self.redisServer.recieve_spamers))
        UiMenu.show_lst("Most spamrs: ", spamers)