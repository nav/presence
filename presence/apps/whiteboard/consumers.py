import json
import random
import hashlib
from django.core.cache import cache
from django.http.request import QueryDict
from django.contrib.auth import get_user_model
from django_comments.models import Comment
from channels import Group
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
from .models import Message


@channel_session_user_from_http
def ws_connect(message):
    Group("whiteboard").add(message.reply_channel)


@channel_session_user
def ws_message(message):
    msg = json.loads(message.content.get('text', ''))
    if not msg['comment'].strip():
        return

    comment = Comment.objects.create(user=message.user,
                                     comment=msg['comment'].strip(),
                                     content_type_id=8,
                                     object_pk='1',
                                     site_id=1)
    msg = Message.objects.create(page=msg['page'], comment=comment)
    Group("whiteboard").send({
        "text": json.dumps(dict(id=msg.pk,
                                page=msg.page,
                                comment=comment.comment,
                                submit_date=comment.submit_date.strftime('%Y-%m-%d'),
                                hash=hashlib.md5(comment.user.email).hexdigest())),
    })

@channel_session_user
def ws_disconnect(message):
    Group("whiteboard").discard(message.reply_channel)
