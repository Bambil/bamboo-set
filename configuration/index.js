'use strict';

const winston = require('winston');

module.exports = function configuration() {
  this.add({role: 'configuration', action: 'request'}, (msg, respond) => {
    winston.log(`request configuration ${msg}`);
    this.act({role: 'connectivity', action: 'send', data: msg.data,
             channel: 'configuration/request'}, respond);
  });
};
