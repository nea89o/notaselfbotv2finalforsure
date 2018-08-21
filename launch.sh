#!/usr/bin/env bash
scriptdir=$(dirname $(readlink -f $0))
cd ${scriptdir}
while true
do
  `pwd`/venv/bin/python main.py &>$HOME/logs/discordbot
done

