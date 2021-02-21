import json
from json.decoder import JSONDecodeError
import paho.mqtt.client as mqtt

BEEBOTTE_CHANNEL_TOKEN = 'token_jMvmLp00TLF5Kw1t'


def on_connect(client: mqtt.Client, userdata, flags, result_code):
    if not result_code == mqtt.MQTT_ERR_SUCCESS:
        client.reconnect()

    client.subscribe(topic='test/res', qos=1)


def on_messgage(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    #print('dup %s' % msg.dup)
    #print('info %s' % msg.info)
    #print('mid %s' % msg.mid)
    #print('payload %s' % msg.payload)
    #print('qos %s' % msg.qos)
    #print('retain %s' % msg.retain)
    #print('state %s' % msg.state)
    #print('timestamp %s' % msg.timestamp)
    #print('topic %s' % msg.topic)
    try:
        data = json.loads(msg.payload.decode())
        print(json.dumps(data, indent=2))
        pass
    except JSONDecodeError:
        raise


def setup_beebotte():
    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_message = on_messgage
    mqttc.username_pw_set(username='token:%s' % BEEBOTTE_CHANNEL_TOKEN)
    mqttc.tls_set(ca_certs='mqtt.beebotte.com.pem')
    mqttc.connect(host='mqtt.beebotte.com', port=8883)
    mqttc.loop_start()