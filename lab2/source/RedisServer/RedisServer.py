import redis
import datetime
import logging
import colorama
colorama.init()

logging.basicConfig(filename="./events.log", level=logging.INFO)


class Redis(object):
    def __init__(self):
        self.__r = redis.Redis(charset="utf-8", decode_responses=True)

    def make_register(self, user_name):
        if self.__r.hget('usrs:', user_name):
            raise Exception(f"\n Choose other username)")
        usr_id = self.__r.incr('user:id:')
        pipeln = self.__r.pipeline(True)
        pipeln.hset('usrs:', user_name, usr_id)
        pipeln.hmset(f"user:{usr_id}", {
            'login': user_name,
            'id': usr_id,
            'queue': 0,
            'check': 0,
            'bloked': 0,
            'sended': 0,
            'delivered': 0
        })
        pipeln.execute()
        logging.info(f"User {user_name} created at {datetime.datetime.now()} \n")
        return usr_id

    def make_signin(self, usr_name):
        usr_id = self.__r.hget("users:", usr_name)

        if not usr_id:
            raise Exception(f"{usr_name} does not exist ")

        self.__r.sadd("online now", usr_name)
        logging.info(f"{usr_name} logged in at {datetime.datetime.now()} \n")
        self.__r.publish('users', "User %s signed" % self.__r.hmget(f"user:{usr_id}", 'login')[0])
        return int(usr_id)

    def make_sign_out(self, usr_id) -> int:
        logging.info(f" '{usr_id}' signed out at {datetime.datetime.now()} \n")
        self.__r.publish('users', " '%s' signed out" % self.__r.hmget(f"user:{usr_id}", 'login')[0])
        return self.__r.srem("online now:", self.__r.hmget(f"user:{usr_id}", 'login')[0])

    def create_mess(self, msg_text, getter, sender) -> int:

        msgId = int(self.__r.incr('message:id:'))
        receiver = self.__r.hget("users:", getter)

        if not receiver:
            raise Exception(f"\n  '{getter}' does not exist\n")

        pipeln = self.__r.pipeline(True)

        pipeln.hmset('message:%s' % msgId, {
            'text': msg_text,
            'id': msgId,
            'sender_id': sender,
            'receiver': receiver,
            'status': "created"
        })
        pipeln.lpush("queue:", msgId)
        pipeln.hmset('message:%s' % msgId, {
            'status': 'queue'
        })
        pipeln.zincrby("sended:", 1, "user:%s" % self.__r.hmget(f"user:{sender}", 'login')[0])
        pipeln.hincrby(f"user:{sender}", "queue", 1)
        pipeln.execute()

        return msgId

    def recieve_msg(self, user_id):
        msg = self.__r.smembers(f"sended to:{user_id}")
        msgList = []
        for msgId in msg:
            msg = self.__r.hmget(f"msg:{msgId}", ["senderId", "text", "status"])
            senderId = msg[0]
            msgList.append("From '%s' - '%s'" % (self.__r.hmget("user:%s" % senderId, 'login')[0], msg[1]))
            if msg[2] != "delivered":
                pipeln = self.__r.pipeline(True)
                pipeln.hset(f"msg:{msgId}", "status", "delivered")
                pipeln.hincrby(f"user:{senderId}", "sended", -1)
                pipeln.hincrby(f"user:{senderId}", "delivered", 1)
                pipeln.execute()
        return msgList

    def recieve_senders(self, senders_quantity) -> list:
        return self.__r.zrange("sended:", 0, int(senders_quantity) - 1, desc=True, withscores=True)

    def recieve_spamers(self, receivers_quantity) -> list:
        return self.__r.zrange("spam:", 0, int(receivers_quantity) - 1, desc=True, withscores=True)

    def recieve_stats(self, userId):
        curUser = self.__r.hmget(f"user:{userId}", ['queue', 'check', 'bloked', 'sended', 'delivered'])
        return " Queuing - %s\n Check -" \
               " %s\n Banned - %s\n Sended - %s\n Delivered - %s" % \
               tuple(curUser)

    def recieve_active_users(self) -> list:
        return self.__r.smembers("online:")

