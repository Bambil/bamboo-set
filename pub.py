import  paho.mqtt.client as mqtt

client = mqtt.Client("C1")  # create a client
broker_address = "iot.eclipse.org"  # use external broker
client.connect(broker_address)  # connect to broker

client.publish("set", "{'isdone' : True}")