#!/bin/bash

HOMEDIR=$(dirname $0)
PIDIR=$HOMEDIR/run
PID=doonia.pid

usage()
{
    echo "Usage: $0: [OPTIONS]"
    echo "  start dev   : Launch development server"
    echo "  stop dev    : Stop development server"
    echo "  start prod  : Launch production server"
    echo "  stop prod   : Stop production server"
    exit 1
}

if [ ! $# -eq 2 ]; then
  usage
fi

ACTION=$1
PLATFORM=$2

if [ "$ACTION" == "start" ]; then
  # create pid dir
  mkdir -p $PIDIR

  # source the local Python virtualenv
  source $HOMEDIR/py/bin/activate

  if [ "$PLATFORM" == "dev" ]; then
    PORT=9000
  elif [ "$PLATFORM" == "prod" ]; then
    PORT=5000
  else
    echo "Unknown platform '$PLATFORM'"
    usage
    exit 1
  fi

  # write pid file
  echo $$ > $PIDIR/$PLATFORM-$PID

  # launch the flask webserver
  cd $HOMEDIR/website && python doonia.py runserver -p $PORT -t 0.0.0.0

elif [ "$ACTION" == "stop" ]; then
  # get group PID & delete PID file
  GPID=$(cat $PIDIR/$PLATFORM-$PID)
  rm -f $PIDIR/$PLATFORM-$PID
  
  # kill the process group
  kill -- -$GPID
else
    echo "Unknown action '$ACTION'"
    usage
    exit 1
fi
