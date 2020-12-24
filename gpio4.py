import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import threading
import logging

FORMAT = "%(asctime)s.%(msecs)03d %(levelname)s [%(process)d] [%(filename)s::%(funcName)s@%(lineno)s] %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

BROKER_ADDRESS = "192.168.0.109"
BROKER_PORT = 1883
CHANNEL = 4

GPIO.setmode(GPIO.BCM)

GPIO.setup(CHANNEL, GPIO.OUT)

class Motor:
    
    def __init__(self):
        self.job_active = False

    def switch_on_motor(self):
        if GPIO.input(CHANNEL) == 0:
            GPIO.output(CHANNEL, GPIO.HIGH)
            logging.info("Switched On")

    def sleeper(self,minutes):
        time.sleep(60*minutes)

    def switch_off_motor(self):
        if GPIO.input(CHANNEL) == 1:
            GPIO.output(CHANNEL, GPIO.LOW)
            logging.info("Switched Off")
    
    def get_motor_status(self):
        return GPIO.input(CHANNEL)
    
    def validate_message(self, message):
        elements = message.split('/')
        try :
            if elements[0] == "ushamotor" and isinstance(int(elements[1]), int) == True :
                return True
            else:
                return False
        except Exception as error :
            logging.error(error)
            return False
    
    def get_run_minutes(self, message):
        elements = message.split('/')
        return int(elements[1])

    def run_job(self,message):

        if self.get_motor_status() == 0 and self.job_active == False:
            #start job
            minutes = self.get_run_minutes(message)
            self.job_active = True
            self.switch_on_motor()
            self.sleeper(minutes)
            self.switch_off_motor()
            self.job_active = False
            return True
        else:
            return False


#GPIO.cleanup()

motor_instance = Motor()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ushamotor/#")
    client.subscribe("getstatus")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message_topic = msg.topic
    logging.info(message_topic+" "+str(msg.payload))
    if message_topic == "getstatus":
        current_state = motor_instance.get_motor_status()
        client.publish("currentstatus", payload=str(current_state), qos=0, retain=False)
        logging.info("Status sent")
    elif motor_instance.validate_message(message_topic):
        motor_job_th = threading.Thread(target=motor_instance.run_job, args=(message_topic))
        motor_job_th.start()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

while True:
    time.sleep(1)
