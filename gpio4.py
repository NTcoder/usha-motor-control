import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)

def switch_on_motor():
    GPIO.output(4, GPIO.HIGH)

def sleeper(minutes):
    time.sleep(60*minutes)

def switch_off_motor():
    GPIO.output(4, GPIO.LOW)
#GPIO.cleanup()



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ushamotor/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()