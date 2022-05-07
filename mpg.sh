#!/bin/sh
export LOGIN=
export PASSWORD=
TOKEN=$(curl --silent --request POST --header "Content-Type: application/json" --data '{"login":"'"$LOGIN"'","password":"'"$PASSWORD"'","language":"fr-FR"}' https://api.mpg.football/user/sign-in | jq --raw-output '.token')
echo -e "Content-Type: application/json\nAuthorization: $TOKEN" > /tmp/mpg.headers
curl --silent --request GET --header @/tmp/mpg.headers https://api.mpg.football/division/mpg_division_NKAJ9FUM_2_1/coach > data.json | jq .
