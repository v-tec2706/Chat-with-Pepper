#!/usr/bin/env bash

export PYTHONPATH="$PWD"
trap "exit" SIGINT

response_from_console_enabled=false
should_start_rest_service=false
should_start_bot=false
should_initilize_db=false

rest_controller_port=$(python src/common_utils/parameter_provider.py "REST_API_PORT" 2>&1)
robot_socket_port=$(python src/common_utils/parameter_provider.py "ROBOT_SOCKET_PORT" 2>&1)

initialize_database(){
  ./initialize_db.sh
}

start_rest_service(){
   echo "Initializing REST service..."
   python src/connectivity/rest/rest_controller.py &
   echo "REST service initilized successfuly!"
}

start_bot(){
  if [ $response_from_console_enabled == true ]
  then
    python src/connectivity/socket/socket_conn_bot.py -c
  else
    python src/connectivity/socket/socket_conn_bot.py
  fi
}

help(){
    echo "
      --------------------------------------------------
                Welcome in Chat-with-Pepper
      --------------------------------------------------
      You can run this script with following options:

        [-c | --console]                   enables providing responses to user questions from command line
        [-db | --initialize_database]      initilizes database with required data
        [-r | --rest]                      starts REST service
        [-b | --bot]                       starts bot

        ctrl + C                           exit
     "
}

exit(){
  echo "
  Closing Chat-with-Pepper..."
  kill -9 $(lsof -t -i tcp:"$robot_socket_port","$rest_controller_port")
}


if [ "$1" == "" ]
then
  help
fi

while [ "$1" != "" ]; do
    case $1 in
        -c | --console )
            response_from_console_enabled=true
            ;;
        -db | --initialize_database )
            should_initilize_db=true
            ;;
        -h | --help )
            help
            ;;
        -r | --rest )
            should_start_rest_service=true
            ;;
        -b | --bot )
          should_start_bot=true
          ;;
    esac
    shift
done

if [ $should_start_rest_service == true ]
then
  start_rest_service
fi

if [ $should_initilize_db == true ]
then
  initialize_database
fi

if [ $should_start_bot == true ]
then
  start_bot
fi

wait