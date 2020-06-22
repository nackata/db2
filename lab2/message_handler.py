import redis


def next(conn: redis.Redis):
    msg = conn.srandmember('message:created')
    if msg is None:
        return msg
    print('from: %s' % conn.hget(msg, 'author'))
    print('to: %s' % conn.hget(msg, 'target'))
    print('')
    print(conn.hget(msg, 'text'), flush=True)
    return msg


def mark(conn: redis.Redis, msg: str):
    author = conn.hget(msg, 'author')
    p = conn.pipeline()
    p.hset(msg, 'status', 'spam')
    p.smove('message:created', 'message:spam', msg)
    p.zincrby('user:spam', 1, author)
    p.publish('message:spam:event', msg)
    p.execute()


def message(conn: redis.Redis, msg: str):
    p = conn.pipeline()
    p.hset(msg, 'status', 'delivered')
    p.smove('message:created', 'message:delivered', msg)
    p.execute()
