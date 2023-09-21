#!/bin/sh

workdir="$(mktemp -d)"
archive="jupyterhub_$(date +%Y-%m-%dT%H:%M:%S).zip"

compress_directory() {
    cd "/home" || exit 1
    zip -r9P "$2" "$workdir/$1.zip"  "$1"/**
    ls -la "$workdir/$1.zip"
}

jq -r '.[] | .username + "\t" + .password' < /etc/users.json | \
while read -r user
do
   eval "compress_directory $user"
done

sh -c "cd $workdir && zip -r9 '$archive' . || exit 1"

cp "$workdir/$archive" .
rm -rf "$workdir"

echo "Created archive: '$archive'"
