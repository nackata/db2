import redis


def listen(conn: redis.Redis):
    pubsub = conn.pubsub()
    pubsub.subscribe(['user:event', 'message:spam:event'])

    print('Listening...')

    for item in pubsub.listen():
        if item['type'] != 'message':
            continue
        item = item['data']

        if item.startswith(b'message'):
            print('Spam: ', item)
        elif item.startswith(b'user'):
            user = b':'.join(item.split(b':')[:2])
            if item.endswith(b'login'):
                print('Logged in')
                conn.sadd('logged-in', user)
            elif item.endswith(b'logout'):
                print('Logged out')
                conn.srem('logged-in', user)
