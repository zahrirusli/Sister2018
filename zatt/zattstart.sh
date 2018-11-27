#!/bin/sh

# Start the processes as daemon
zattd -c zatt.conf -s zatt.0.persist -a 172.17.0.2 -p 5254 >/dev/null 2>&1 < /dev/null &
zattd -c zatt.conf -s zatt.1.persist -a 172.17.0.2 -p 5255 >/dev/null 2>&1 < /dev/null &
zattd -c zatt.conf -s zatt.2.persist -a 172.17.0.2 -p 5256
