'use strict';

const schema = require('./request-schema.json');
const winston = require('winston');
const ajv = require('ajv')();

const validate = ajv.compile(schema);

module.exports = function configuration() {
  this.add({role: 'configuration', action: 'request'}, (msg, respond) => {

    if (!validate(msg.data)) {
      return respond(validate.errors);
    }

    this.act({role: 'connectivity', action: 'send', data: msg.data,
             channel: 'configuration/request'}, respond);
  });

  this.add({role: 'configuration', action: 'change'}, (msg, respond) => {
    winston.info(msg.data);
    respond();
  });
};
