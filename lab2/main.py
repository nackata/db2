import redis

import worker
import general
import listen

import time
from random import random, sample, randint
from typing import Optional, List




class User:
    conn: redis.Redis
    token: Optional[str]
    username: Optional[str]

    def __init__(self, conn: Optional[redis.Redis] = None, username: Optional[str] = None):
        self.conn = conn or general.connect()
        self.token = None
        self.username = None

        if username is not None:
            self.username = username
            self.token = general.login(self.conn, username)


    def register(self, username: str):
        general.register(self.conn, username)
        self.username = username

    def login(self, username: str):
        self.token = general.login(self.conn, username)
        if self.token:
            self.username = username
        else:
            print('User %s does not exist' % username)
            return

    def logout(self):
        if self.token is not None:
            general.logout(self.conn, self.token)
            self.token = None

    def send(self, username: str, text: str):
        if self.token is None:
            print('You are not logged in')
            return

        user = general.get_user(self.conn, username)
        if user is None:
            print('User %s does not exist' % username)
            return
        general.send_message(self.conn, self.token, user, text)

    def stats(self):
        if self.token is None:
            print('You are not logged in')
            return

        user = self.conn.get(self.token)
        general.get_message_stats(self.conn, user)

    def inbox(self):
        if self.token is None:
            print('You are not logged in')
            return

        general.print_messages(self.conn, self.token)


class Emulate:
    def __init__(self, usernames: List[str]):
        self.conn = general.connect()
        self.usernames = usernames
        for name in usernames:
            if general.get_user(self.conn, name) is None:
                general.register(self.conn, name)

        self.users = [User(self.conn, username=name) for name in usernames]

    def run(self):
        while True:
            time.sleep(random())
            user = sample(self.users, 1)[0]
            target = sample(self.usernames, 1)[0]
            user.send(target, random_text())
            print('%s sent message to %s' % (user.username, target))


class Worker:
    conn: redis.Redis
    msg: Optional[str]

    def __init__(self, conn: Optional[redis.Redis] = None):
        self.conn = conn or general.connect()
        self.msg = None

    def next(self, silent: bool = False):
        self.msg = worker.next_message(self.conn)
        if self.msg is None and not silent:
            print('No messages in queue as of now')

    def spam(self):
        if self.msg is None:
            print('You have not selected a message')
            return

        worker.mark_as_spam(self.conn, self.msg)
        self.msg = None

    def deliver(self):
        if self.msg is None:
            print('You have not selected a message')
            return

        worker.deliver(self.conn, self.msg)
        self.msg = None

    def auto(self):
        while True:
            self.next(silent=True)
            if self.msg is None:
                time.sleep(0.1)
                continue
            print('Checking for spam')
            time.sleep(random())
            if random() < 0.3:
                print('Spam detected')
                self.spam()
            else:
                print('No spam detected')
                self.deliver()


class Admin:
    conn: redis.Redis

    def __init__(self, conn: Optional[redis.Redis] = None):
        self.conn = conn or general.connect()

    def get_usernames(self, users: List[str]):
        p = self.conn.pipeline()
        for user in users:
            p.hget(user, 'username')

        return [str(name) for name in p.execute()]

    def online(self):
        users = self.conn.smembers('logged-in')
        print('Online:')
        for user in self.get_usernames(users):
            print(user)

    def most_active(self, n: int):
        users_scores = list(zip(*self.conn.zrange('user:sent', 0, n-1, desc=True, withscores=True)))
        if len(users_scores) < 2:
            print('No users found')
            return

        print('Most active:')
        users, scores = users_scores
        for user, score in zip(self.get_usernames(users), scores):
            print('%s: %s' % (user, score))

    def spammers(self, n: int):
        users_scores = list(zip(*self.conn.zrange('user:spam', 0, n-1, desc=True, withscores=True)))
        if len(users_scores) < 2:
            print('No users found')
            return

        print('Most active spammers:')
        users, scores = users_scores
        for user, score in zip(self.get_usernames(users), scores):
            print('%s: %s' % (user, score))


class LoginListener:
    conn: redis.Redis

    def __init__(self, conn: Optional[redis.Redis] = None):
        self.conn = conn or general.connect()

    def listen(self):
        listen.listen(self.conn)
