""" Set component of an IOT Platform

 Creation Date : 7/25/17
 Created By : maryam ebrahimzadeh(maryam.ebrahimzadeh1997@yahoo.com)
              monireh safari(monirehsafari18@gmail.com)

"""
import threading
import time
import json
import paho.mqtt.client as mqtt
from flask import Flask, request
from pymongo import MongoClient
import  random
import yaml_1 as yaml

#with open("example.yaml", 'r') as stream:
#    try:
#        print(yaml.load(stream))
#    except yaml.YAMLError as exc:
#        print(exc)

answerJson = []
""" list: list of answers to diffrent requests."""
client = mqtt.Client("C1")
""" mqtt client."""
broker_address = "127.0.0.1:9994"
""" address of broker . """
client.connect(broker_address)

mongoclient = MongoClient()
""" mongo client ."""
db = mongoclient.mayDatabase
""" database of the module ."""


def on_message(client, userdata, message):
    """ this method is for get the json which is sent by agent layer in MQTT.

    :param client: mqtt client.
    :param userdata: default argument.
    :param message: the message which is received.

    """

    print ("message received " + str(message.payload))
    print("topic " + str(message.topic))

    receivedMessage = json.dumps(message.payload)
    finalReceivedMessage = json.loads(receivedMessage)
    global answerJson
    answerJson.append(finalReceivedMessage)  # answer of next layer


def on_log(client, userdata, level, buf):
    """ this method is for print our log.

    :param client: client mqtt client.
    :param userdata: default argument.
    :param level: default argument.
    :param buf: system log.

    """
    print("log: ", buf)


client.on_message = on_message   # attach function to callback
client.on_log = on_log  # attach function to callback
client.loop_start()   # start the loop when we should finish it ?
client.subscribe("set")  #subscribe on channel

app = Flask(__name__)

@app.route('/', methods=['PUT'])
def getMessageChange():
    """
    this method is used for getting a http PUT  request from UI layer
    and publish it to set channel and sleep for 10ms then
    response to the request.

    :return: if it gets the answer send proper text answer
                else return no response.
    """
    if request.headers['content-type'] == 'application/json':
        jsonfile = request.get_json()
        newjson = json.dumps(jsonfile)
        finaljson = json.loads(newjson)
        requestId = random.random()
        finaljson['id'] = requestId
        client.publish("set", finaljson)

        time.sleep(0.01)  # wait 10 ms
        global answerJson

        lock = threading.Lock
        with lock :
            for i in range(0, len(answerJson) - 1):

                if requestId == answerJson[i]['id']:
                    db.agent.update_one(
                        {"agent_id": answerJson[i]['agent_id'],
                         "device_id": answerJson[i]['device_id']},
                        {
                            "$set": answerJson[i]
                        }
                    )
                    if answerJson[i]['is_done'] == True:
                        del answerJson[i]
                        return "is done"
                    else:
                        del answerJson[i]
                        return "no response"

            return "no response"


@app.route('/', methods=['POST'])
def getMessageRead():
    """
    this method is used for getting a http POST request from UI layer
    to read from database.

    :return: special objects from database.
    """
    return  db.agent.find(request.json())
if __name__ == "__main__":
    app.run(threaded = True , host='0.0.0.0')