from faker import Faker
from Entities.administrator import Administrator
from ui import UiMenu

import random
from threading import Thread
from RedisServer.RedisServer import Redis


faker = Faker()

def emulator():
    faker = Faker()
    usersNum = 5
    usrs = [faker.profile(fields=['user_name'], sex=None)['user_name'] for u in range(usersNum)]
    thrds = []
    try:
        for i in range(usersNum):
            thrds.append(EmulatorController(usrs[i], usrs, usersNum, random.randint(100, 5000)))
        for tread in thrds:
            tread.launch()
        Administrator()
        for tread in thrds:
            if tread.is_alive():
                tread.stopping()
    except Exception as e:
        UiMenu.show_err(str(e))


class EmulatorController(Thread):
    def __init__(self, userName, listing_users, users_num, loop_num):
        Thread.__init__(self)
        self.quantLp = loop_num
        self.serv = Redis()
        self.usrsListing = listing_users
        self.usersQnt = users_num
        self.serv.make_register(userName)
        self.usr_id = self.serv.make_signin(userName)

    def launch(self):
        while self.quantLp > 0:
            msgText = faker.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None)
            receivr = self.usrsListing[random.randint(0, self.usersQnt - 1)]
            self.serv.create_mess(msgText, receivr, self.usr_id)
            self.quantLp -= 1

        self.stopping()

    def stopping(self):
        self.serv.make_sign_out(self.usr_id)
        self.quantLp = 0
