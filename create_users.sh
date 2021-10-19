#!/bin/sh
jq -r '.|keys_unsorted[]' users.json | while read username
do
    password=$(jq -r --arg user "$username" '.[$user]' users.json)
    useradd --system -s /sbin/nologin --create-home "$username"
    yes "$password" | passwd "$username" > /dev/null
done
