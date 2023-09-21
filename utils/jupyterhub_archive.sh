#!/bin/sh

workdir="$(mktemp -d)"
archive="jupyterhub_$(date +%Y-%m-%dT%H:%M:%S).zip"

compress_directory() {
    cd "/home" || exit 1
    echo "Data export for user $1 from '$archive'" > "$1/jupyterhub_export_info.txt"
    zip -yrX9P "$2" "$workdir/$1.zip" "$1"/**
    rm -f "$1/jupyterhub_export_info.txt"
}

jq -r '.[] | .username + "\t" + .password' < /etc/users.json | \
while read -r user
do
   eval "compress_directory $user"
done

sh -c "cd $workdir && zip -r9 '$archive' . || exit 1"

cp "$workdir/$archive" .
rm -rf "$workdir"

echo "Created archive: '$archive' ($(du -h "$archive" | cut -f1))"
