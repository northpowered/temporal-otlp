#!/bin/sh
echo "MimIO entrypoint start"
mkdir -p /data
mkdir -p /data/mimir
mkdir -p /data/loki
echo "Provide cmd to container"
exec "$@"