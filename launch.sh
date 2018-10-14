#!/usr/bin/env bash
scriptdir=$(dirname $(readlink -f $0))
cd ${scriptdir}
screen -dmS notaselfbot ${scriptdir}/venv/bin/python main.py

