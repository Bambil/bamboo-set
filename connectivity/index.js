'use strict';

const mqtt = require('mqtt');
const config = require('config');
const winston = require('winston');

/**
 * Creates MQTT connection
 */
const mqttClient  = mqtt.connect(`mqtt://${config.get('mqtt.ip')}`);

mqttClient.on('connect',() => {
  winston.log(` * MQTT at ${config.get('mqtt.ip')}`);
  mqttClient.subscribe(
    `I1820/${config.get('cluster.name')}/configuration/chnage`);
});

module.exports = function connectivity() {
  mqttClient.on('error', (err) => {
    winston.error(err);
  });

  mqttClient.on('message', (topic, message) => {
    const splitedTopic = topic.split('/');
    this.act({role: splitedTopic[2], action: splitedTopic[3],
             data: JSON.parse(message)});
  });

  this.add({role: 'connectivity', action: 'send'}, (msg, respond) => {
    mqttClient.publish(msg.channel, msg.data, respond);
  });
};
