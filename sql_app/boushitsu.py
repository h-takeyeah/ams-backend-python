import json
import os
from json.decoder import JSONDecodeError
from urllib import request
from urllib.error import HTTPError

import paho.mqtt.client as mqtt

try:
    with open(os.getcwd() + '/env.json') as f:
        data = json.load(f)
        BBT_CH_TOKEN = data['beebotte_channel_token']
        BBT_CH = data['beebotte_channel']
        BBT_RES = data['beebotte_resource']
except FileNotFoundError:
    exit(-1)


def post_ephemeral_message(url, body, footer=None):
    blocks = [{
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': str(body)
        }
    }]

    if not footer == None:
        blocks.append({
            'type': 'context',
            'elements': [
                {
                    'type': 'mrkdwn',
                    'text': str(footer)
                }
            ]
        })

    payload = {
        'text': 'from boushitsu',
        'response_type': 'ephemeral',
        'blocks': blocks
    }
    headers = {'Content-type': 'application/json'}
    req = request.Request(url, json.dumps(payload).encode('utf-8'), headers)
    try:
        with request.urlopen(req):
            pass
    except HTTPError as e:
        pass


def respond_to_count_inroomusers():
    res = request.urlopen('http://localhost:8000/room')
    inroomusers_list = json.loads(res.read())
    count = len(inroomusers_list)
    if count == 0:
        return 'No one is currently in the room.'
    else:
        body = 'Currently in the room '
        for i in range(count):
            body += ':bust_in_silhouette:'
        return body


def respond_to_help():
    return '''
`count`: return number of people in the room
`help`: show this message
`(empty)`: check if the room is open'''


def respond_to_its_is_open():
    res = request.urlopen('http://localhost:8000/room')
    inrroomusers_list = json.loads(res.read())
    if len(inrroomusers_list) == 0:
        body = 'boushitsu status: *closed* :zzz:'
    else:
        body = 'boushitsu status: *open* :heavy_check_mark:'
    return body


def handle_slashcommand(data):
    text = data['text']
    url = data['response_url']
    msg = ''
    if len(text) == 0:
        msg = respond_to_its_is_open()
    else:
        '''split text to command & arguments(if exists)'''
        def parse_req(s): return (None if not s else s[0], s[1:])
        cmd = parse_req(text.split(' '))
        if 'help' == cmd[0]:
            msg = respond_to_help()
        elif 'count' == cmd[0]:
            msg = respond_to_count_inroomusers()
        else:
            msg = 'Could not understand. See `/boushitsu help`.'
    post_ephemeral_message(url, msg)


def on_connect(client: mqtt.Client, userdata, flags, result_code):
    if not result_code == mqtt.MQTT_ERR_SUCCESS:
        client.reconnect()

    client.subscribe(topic=f'{BBT_CH}/{BBT_RES}', qos=1)


def on_messgage(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    try:
        data = json.loads(msg.payload.decode('utf-8'))['data']
    except JSONDecodeError:
        raise
    else:
        handle_slashcommand(data)


def setup_beebotte():
    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_message = on_messgage
    mqttc.username_pw_set(username=f'token:{BBT_CH_TOKEN}')
    mqttc.tls_set(ca_certs='mqtt.beebotte.com.pem')
    mqttc.connect(host='mqtt.beebotte.com', port=8883)
    mqttc.loop_start()
