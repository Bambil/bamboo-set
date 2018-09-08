"use strict";

const winston = require("winston");

/**
 * Configure CLI output on the default logger
 */
winston.cli();

/* Seneca application */
const app = require("seneca")();

/**
 * I1820 Initiation
 */
winston.info(" * 18.20 at Sep 07 2016 7:20 IR721");

/**
 * Initiates seneca modules
 */
app.use("connectivity");
app.use("configuration");

/**
 * Seneca is ready
 */
app.act(
  {
    role: "configuration",
    action: "request",
    data: {
      type: "lamp",
      device: "1",
      settings: [{ name: "on", value: true }],
      agent: "42f6a151-92bb-552d-ba69-bf1d25def01f",
    },
  },
  winston.info
);
