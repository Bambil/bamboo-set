##
# Documentation for this module
#
# Set component of an IOT Platform

# In The Name Of God
# Creation Date : 7/25/17
# Created By : maryam ebrahimzadeh(maryam.ebrahimzadeh1997@yahoo.com)
#              monireh safari(monirehsafari18@gmail.com)
import time
import json
import paho.mqtt.client as mqtt
from flask import Flask, request
from pymongo import MongoClient
import yaml_1 as yaml

#with open("example.yaml", 'r') as stream:
#    try:
#        print(yaml.load(stream))
#    except yaml.YAMLError as exc:
#        print(exc)


#Global variables
requestId = -1
answered = False
answerJson = ""

#Determine MQTT client
client = mqtt.Client("C1")  # create a client
broker_address = "127.0.0.1:9994"  # use external broker
client.connect(broker_address)  # connect to broker

#Determine mongoclient
mongoclient = MongoClient()
db = mongoclient.mayDatabase

##documentation for a method
#
# @Param client mqtt client
# @Param userdata default argument
# @Param message the message which is received
#
#this method is for get the json which is sent by agent layer in MQTT
def on_message(client, userdata, message):
    answered = True  # if agent  layer answer to us
    print ("message received " + str(message.payload))
    print("topic " + str(message.topic))

    receivedMessage = json.dumps(message.payload)
    finalReceivedMessage = json.loads(receivedMessage)

    answerJson = finalReceivedMessage  # answer of next layer

##documentation for a method
#
# @Param client mqtt client
# @Param userdata default argument
# @Param level default argument
# @Param buf is our systems log
#
#this method is for print our log
def on_log(client, userdata, level, buf):
    print("log: ", buf)


client.on_message = on_message  # attach function to callback
client.on_log = on_log # attach function to callback
client.loop_start()  # start the loop when we should finish it ?
client.subscribe("set") #subscribe on channel

app = Flask(__name__)

##documentation for a method
#
#this method is used for getting a http PUT  request from UI layer
#and publish it to set channel
#and sleep for 10ms
#then if we get the answer send proper text answer
#else return no response
@app.route('/', methods=['PUT'])
def getMessageChange():
    if request.headers['content-type'] == 'application/json':
        jsonfile = request.get_json()
        newjson = json.dumps(jsonfile)
        finaljson = json.loads(newjson)
        global requestId
        requestId = requestId + 1
        finaljson['id'] = requestId
        client.publish("set", finaljson)

        time.sleep(0.01)  # wait 10 ms
        global answered
        global answerJson
        if answered == True and requestId == answerJson['id']:
            db.agent.update_one(
                {"agent_id": answerJson['agent_id'],
                 "device_id": answerJson['device_id']},
                {
                    "$set": answerJson
                }
            )
            if answerJson['is_done'] == True:
                answered = False
                return "is done"
            else:
                answered = False
                return "no response"
        else:#more than ten ms

            answered = False
            return "no response"
##documentation for a method
#
#this method is used for getting a http POST request from UI layer
#  for reading from our database


@app.route('/', methods=['POST'])
def getMessageRead():
    return  db.agent.find(request.json())

if __name__ == "__main__":
    app.run(host='0.0.0.0')