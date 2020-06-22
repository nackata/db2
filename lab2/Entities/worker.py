import time
import redis

from menu import UiMenu
import random
from threading import Thread
class Worker(Thread):

    def __init__(self, delay):
        Thread.__init__(self)
        self.looping = True
        self.rds = redis.Redis(charset="utf-8", decode_responses=True)
        self.timeDelay = delay

    def launch(self):
        while self.looping:
            msg = self.rds.brpop("queue:")
            if msg:
                msg_id = int(msg[1])

                self.rds.hmset(f"msg:{msg_id}", {
                    'status': 'check'
                })
                msg = self.rds.hmget(f"msg:{msg_id}", ["writerId", "receiverId"])
                writerId = int(msg[0])
                receiverId = int(msg[1])
                self.rds.hincrby(f"user:{writerId}", "queue", -1)
                self.rds.hincrby(f"user:{writerId}", "check", 1)
                time.sleep(self.timeDelay)
                isSpam = random.random() > 0.6
                pipeln = self.rds.pipeline(True)
                pipeln.hincrby(f"user:{writerId}", "check", -1)
                if isSpam:
                    sender_username = self.rds.hmget(f"user:{writerId}", 'login')[0]
                    pipeln.zincrby("spam:", 1, f"user:{sender_username}")
                    pipeln.hmset(f"msg:{msg_id}", {
                        'status': 'bloked'
                    })
                    pipeln.hincrby(f"user:{writerId}", "bloked", 1)
                    pipeln.publish('spam', f"{sender_username} sended next spam \"%s\"" %
                                  self.rds.hmget("msg%s" % msg_id, ["text"])[0])
                    print(f"{sender_username} sended next spam \"%s\"" % self.rds.hmget("msg%s" % msg_id, ["text"])[0])
                else:
                    pipeln.hmset(f"msg{msg_id}", {
                        'status': 'sended'
                    })
                    pipeln.hincrby(f"user:{writerId}", "sended", 1)
                    pipeln.sadd(f"sended to:{receiverId}", msg_id)
                pipeln.execute()

    def stopping(self):
        self.looping = False


if __name__ == '__main__':
    try:
        looping = True
        workersCount = 5
        workrs = []
        for i in range(workersCount):
            thisWorker = Worker(random.randint(0, 3))
            thisWorker.setDaemon(True)
            workrs.append(thisWorker)
            thisWorker.launch()
        while True:
            pass
    except Exception as e:
        UiMenu.show_err(str(e))
