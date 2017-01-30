#! /bin/bash

APIS="sources cloud_explorer"
URL="https://console.cloudinsight.alertlogic.com/api"

for api in $APIS; do 
    echo "fetching api_data: ${api}"
    curl -s ${URL}/${api}/api_data.json -o $(dirname $0)/${api}.json
done
