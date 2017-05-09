#!/bin/bash

read -r -d '' config << EOF
{
  "mqtt": {
    "ip": "$MQTT_IP",
    "port": "$MQTT_PORT"
  },
  "cluster": {
    "name": "$CLUSTER_NAME",
    "consul": {
      "host": "$CLUSTER_CONSUL_HOST"
    }
  }
}
EOF

echo $config > config/default.json
