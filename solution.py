import time 
import redis 

def unlist_item(conn, user_id, item_id):
    inventory = f'inventory:{user_id}'
    item = f'{item_id}.{user_id}'
    end = time.time() + 5
    pipe = conn.pipeline()

    while time.time() < end:
        try:
            pipe.watch(inventory)
            if not pipe.zscore('market:', item):
                pipe.unwatch()
                return None
            pipe.multi()
            pipe.zrem("market:", item)
            pipe.sadd(inventory, item_id)
            pipe.execute()
            return True
        except redis.exceptions.WatchError:
            print("watch failed")
    return False
