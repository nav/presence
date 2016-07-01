import json
import hashlib
from django.core.cache import cache
from django.http.request import QueryDict
from django.contrib.auth import get_user_model
from channels import Group

PRESENCE_CACHE_KEY = 'presence'
PRESENCE_CACHE_TIMEOUT = 60 * 60 * 24


def get_email_hash(username):
    User = get_user_model()
    user = User.objects.only('email').get(username=username)
    return u'{}:{}'.format(user.email, hashlib.md5(user.email).hexdigest())


def ws_connect(message):
    query = QueryDict(message.content['query_string'])
    page = query.get('page')
    email_hash = get_email_hash(query.get('user'))

    Group("presence").add(message.reply_channel)

    presence = cache.get(PRESENCE_CACHE_KEY, dict())
    if page in presence:
        presence[page].append(email_hash)
    else:
        presence[page] = [email_hash]
    cache.set(PRESENCE_CACHE_KEY, presence, PRESENCE_CACHE_TIMEOUT)

    Group("presence").send({
        "text": json.dumps(presence),
    })


# Connected to websocket.receive
def ws_message(message):
    msg = json.loads(message.content['text'])
    action = msg['action']
    if action == 'presence-disconnect':
        page = msg['page']
        email_hash = get_email_hash(msg['user'])

        presence = cache.get(PRESENCE_CACHE_KEY, dict())
        if page in presence:
            presence[page].remove(email_hash)
        if not presence[page]:
            del presence[page]
        cache.set(PRESENCE_CACHE_KEY, presence, PRESENCE_CACHE_TIMEOUT)

        Group("presence").send({
            "text": json.dumps(presence),
        })


# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("presence").discard(message.reply_channel)
