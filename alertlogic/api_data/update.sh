#! /bin/bash

# space separted list of services
APIS="sources scan_scheduler launcher"
URL="https://console.cloudinsight.alertlogic.com/api"

for api in $APIS; do
    echo -ne "fetching api_data: ${api} ... "
    dest="$(dirname $0)/${api}.json"
    curl -s ${URL}/${api}/api_data.json -o ${dest}.tmp
    if [ "$?" == "0" ]; then
        validation=$(jq ".[0].type" ${dest}.tmp 2>/dev/null)
        if [[ "$?" == "0" && ${validation} != "null" ]]; then
            mv ${dest}.tmp ${dest}
            echo "ok"
        else
            echo "invalid format"
            rm -f ${dest}.tmp
        fi
    else
        echo "invalid server response"
        rm -f ${dest}.tmp
    fi
done
