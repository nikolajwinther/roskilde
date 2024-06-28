#!/usr/bin/env bash

# Script that scrapes the roskilde festival homepage and creates a json file for each musician
function toline {
    sed 's/></>\n</g'
}
function xmltostring {
    cut -d ">" -f2 | cut -d "<" -f1
}


year=$(date +%Y)
dato=$(date +%Y%m%d)
lang="da"
curl -s https://www.roskilde-festival.dk/program/musik > "${lang}-program-$dato.html"
bands=$(cat ${lang}-program-$dato.html | toline | grep props | xmltostring | jq .props.pageProps.modules[0].data.items | grep url | grep program | grep musik | cut -d '"' -f4 | cut -d "/" -f4)
for band in $bands
do
    echo $band
    curl -s https://www.roskilde-festival.dk/program/musik/${band} | toline | grep props | xmltostring | jq .props.pageProps.modules >${lang}-band-$dato-${band}.json

done
