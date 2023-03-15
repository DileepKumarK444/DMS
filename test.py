import paho.mqtt.client as mqtt
import time
import json

print("here")


def on_message(client, userdata, message):
    m_decode = str(message.payload.decode("utf-8", "ignore"))
    print("Received message: ")
    sample = json.loads(m_decode)
    print(sample)
    filename = "C:/Users/Actionfi/Documents/Projects/dms/attachments/" + sample.get('mac_id').replace(':', '_')
    with open(filename, 'w') as filetowrite:
        filetowrite.write(m_decode)


mqttBroker = "mongodb.actionfi.com"
client = mqtt.Client("TestMQTT")
# client.username_pw_set("axl_user", "$6$5FjyEc7TcgwtlHBD$cmZSy3sFq5HLiQAMKbEElQO/0feFaCVl4hMkvFJ9eA6CEoU4KpC4GhVmcBuj5+PNkHPIOBExax8yV1elCtoPJg==")
client.connect(mqttBroker)

client.loop_start()
client.subscribe("SampleMQTT")
client.on_message = on_message
while True:
    time.sleep(1)
client.loop_forever()
