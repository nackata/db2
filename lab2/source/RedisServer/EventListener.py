import logging
import redis

from threading import Thread
import datetime


class EventListener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.rds = redis.Redis(charset="utf-8", decode_responses=True)
        self.Events = []

    def launch(self):
        pubSubs = self.rds.pubsub()
        pubSubs.subscribe(['users', 'spam'])
        for itm in pubSubs.listen():
            if itm['type'] == 'msg':
                msg = " %s at '%s'" % (itm['data'], datetime.datetime.now())
                self.Events.append(msg)
                logging.info(msg)

    def recieve_events(self):
        return self.Events
