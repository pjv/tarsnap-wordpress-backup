#!/usr/bin/env bash

# run the backup.sh inside of every folder in ~/backups

SCRIPTPATH="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
FILEPATH=`dirname $SCRIPTPATH`

for dir in $FILEPATH/* ; do
  if [ -d "$dir" ]; then
    if [[ -e "$dir/backup.sh" ]]; then
        "$dir/backup.sh"
    fi
  fi
done