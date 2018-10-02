#!/bin/bash
# --------- User Settings ---------
PROCESS2RUN="Stanchions.py"
MONITOR_SCRIPT="/home/pi/Python/monitor_process.py"
# ---------------------------------
VAR=`pgrep -f "$PROCESS2RUN"`
echo $VAR
nohup python $MONITOR_SCRIPT $VAR &