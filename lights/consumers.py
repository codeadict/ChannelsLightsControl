import json

from channels import Channel, Group


def ws_connect(message):
    message.reply_channel.send({'accept': True})
    Group('lights').add(message.reply_channel)


def ws_receive(message):
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel('lights.receive').send(payload)


def ws_disconnect(message):
    Group('lights').discard(message.reply_channel)
