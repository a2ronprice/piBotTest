import time
import paho.mqtt.client as mqtt
import serial

clientName = "PiBot"
serverAddress = "10.194.2.2"
mqttClient = mqtt.Client(clientName)
didPrintSubscribeMessage = False


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
    elif message == "drop":
        print("drop")
        ser.write(b"drop \n")
    else:
        print("message not found")


# Set up calling functions to mqttClient
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder
ser.reset_input_buffer()

# Connect to the MQTT server & loop forever.
# CTRL-C will stop the program from running.
mqttClient.connect(serverAddress)
mqttClient.loop_forever()
