#!/bin/bash

gnome-terminal -- bash -c "python3 insults/insultServer.py"

gnome-terminal -- bash -c "redis-server"

sudo docker run -it --rm --name rabbitmq -p 5673:5673 -p 15672:15672 rabbitmq:3.13-management