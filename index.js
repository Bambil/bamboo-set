'use strict';

const winston = require('winston');

/**
 * Configure CLI output on the default logger
 */
winston.cli();


/* Seneca application */
const app = require('seneca')();


/**
 * I1820 Initiation
 */
winston.info(' * 18.20 at Sep 07 2016 7:20 IR721');

/**
 * Initiates seneca modules
 */
app.use('connectivity');

/**
 * Seneca is ready
 */
