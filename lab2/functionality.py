import redis


def connect():
    return redis.Redis(host='localhost', port=6379, db=0)


def send(conn: redis.Redis, token: str, target: str, text: str):
    author = conn.get(token)
    if author is None:
        raise Exception('You are not logged in')

    id = conn.incr('message:id')
    id = 'message:%s' % id
    p = conn.pipeline()
    p.hset(id, 'author', author)
    p.hset(id, 'target', target)
    p.hset(id, 'text', text)
    p.sadd('message:created', id)
    p.sadd('message:from:%s' % author, id)
    p.sadd('message:to:%s' % target, id)
    p.zincrby('user:sent', 1, author)
    p.execute()


def print(conn: redis.Redis, token: str):
    user = conn.get(token)
    if user is None:
        raise Exception('You are not logged in')

    for msg in conn.sinter('message:to:%s' % user, 'message:delivered'):
        print('from: ', str(conn.hget(conn.hget(msg, 'author'), 'username')))
        print(conn.hget(msg, 'text'))
        print('--------------')
        print()


def print_message(conn: redis.Redis, msg: str):
    print('from: %s' % str(conn.hget(conn.hget(msg, 'author'), 'username')))
    print('to: %s' % str(conn.hget(conn.hget(msg, 'target'), 'username')))
    print('')
    print(str(conn.hget(msg, 'text')), flush=True)


def get_user(conn: redis.Redis, username: str):
    return conn.hget('user:username', username)


def get_message_stats(conn: redis.Redis, user: str):
    created = len(conn.sinter('message:from:%s' % user, 'message:created'))
    spam = len(conn.sinter('message:from:%s' % user, 'message:spam'))
    delivered = len(conn.sinter('message:from:%s' % user, 'message:delivered'))

    print('created:   ', created)
    print('delivered: ', delivered)
    print('spam:      ', spam)


def register(conn: redis.Redis, username: str):
    if conn.hexists('user:username', username):
        raise Exception('User with name %s already exists' % username)
    id = conn.incr('user:id')
    if conn.hexists('user:username', username):
        raise Exception('User with name %s already exists' % username)
    p = conn.pipeline()
    p.hset('user:username', username, 'user:%s' % id)
    p.hset('user:%s' % id, 'username', username)
    p.sadd('user:logged-out', 'user:%s' % id)
    p.execute()
    return 'user:%s' % id


def login(conn: redis.Redis, username: str):
    user = conn.hget('user:username', username)
    if user is None:
        raise Exception('User with name %s does not exist' % username)
    token = 'token:%s' % conn.incr('token:id')
    p = conn.pipeline()
    p.set(token, user)
    p.expire(token, 600)
    p.publish('user:event', b'%s:login' % user)
    p.execute()
    return token


def logout(conn: redis.Redis, token: str):
    user = conn.get(token)
    if user is None:
        raise Exception('You are not logged in')
    p = conn.pipeline()
    p.delete(token)
    p.publish('user:event', b'%s:logout' % user)
    p.execute()
