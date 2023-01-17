# control-pibot.py
# If your pi's hostname is something different than "mil-mascaras", see comments
# below the lines labeled *** IMPORTANT *** below.

# *** IMPORTANT ***
# The commands below assume your pi's hostname is mil-mascaras. If you have a
# different name, then use that name in place of mil-mascaras in the mosquitto_pub
# commands, below.
# once running, you can test with the shell commands:
# To play any of the numbered sounds (substitute a diffrent number for "1" for a different sound:
# mosquitto_pub -h mil-mascaras.local -t "pibot/move" -m "1"
# To start the robot:
# mosquitto_pub -h mil-mascaras.local -t "pibot/move" -m "forward"
# To stop the robot:
# mosquitto_pub -h mil-mascaras.local -t "pibot/move" -m "stop"

import time
import paho.mqtt.client as mqtt
# if you're using an Adafruit Crickit hat, uncomment the line below and comment out the statement above:
# from adafruit_crickit import crickit
# NOTE: The line below is needed if you're using the Waveshare Motor Driver Hat
# comment out this line if you're using a Crickit
# Also, only if using the Waveshare Motor Driver Hat, be sure you've installed
# and modified CircuitPython files, in particular the file at:
# /usr/local/lib/python3.5/dist-packages/adafruit_motorkit.py
# as described in the tutorial at:
# https://gallaugher.com/mil-mascaras

# uncomment lines below if you're using a Crickit
# then replace any reference to kit.motor1 with motor_1 and kit.motor2 with motor_2
# motor_1 = crickit.dc_motor_1
# motor_2 = crickit.dc_motor_2

clientName = "PiBot"
# *** IMPORTANT ***
# This is your pi's host name. If your name is something different than
# mil-mascaras, then be sure to change it, here - make it the name of your Pi
serverAddress = "aaronpi"
mqttClient = mqtt.Client(clientName)
# Flag to indicate subscribe confirmation hasn't been printed yet.
didPrintSubscribeMessage = False

# If the robot veers left or right, add a small amount to the left or right trim, below
# until the bot moves roughly straight. The #s below reflect the bot I'm working with.
# It's probably best to start both trim values at 0 and adjust from there.
# out of 1.0 full power.

# This will make turns at 50% of the speed of fwd or backward


def connectionStatus(client, userdata, flags, rc):
    global didPrintSubscribeMessage
    if not didPrintSubscribeMessage:
        didPrintSubscribeMessage = True
        print("subscribing")
        mqttClient.subscribe("pibot/move")
        print("subscribed")


def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')

    if message == "forward":
        print("^^^ moving forward! ^^^")
    elif message == "stop":
        print("!!! stopping!")
    elif message == "backward":
        print("\/ backward \/")
    elif message == "left":
        print("<- left")
    elif message == "right":
        print("-> right")
    else:
        print("message not found")


# Set up calling functions to mqttClient
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

# Connect to the MQTT server & loop forever.
# CTRL-C will stop the program from running.
mqttClient.connect(serverAddress)
mqttClient.loop_forever()
