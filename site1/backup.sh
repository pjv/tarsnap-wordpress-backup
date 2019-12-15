#!/usr/bin/env bash

SCRIPTPATH="$(cd "${0%/*}" 2>/dev/null; echo "$PWD"/"${0##*/}")"
MYDIR=`dirname $SCRIPTPATH`
SITE=`basename $MYDIR`

# SET THE COMMENTED LINES BELOW
DB="" # mysql database name
DBUSER="" # mysql database user
DBPW=""   # mysql database password
KEYFILENAME="tarsnap.key" # tarsnap keyfile filename
BACKUP_PATHS=(
	${MYDIR}/${DB}.sql
	/path/to/htdocs/wp-content/    # path to wp-content for this site
)
# DONE SETTING

cd $MYDIR

# dump the database to site backup directory
mysqldump "$DB" > "$MYDIR/$DB.sql"

# back up to tarsnap
../do-tarsnap-backup.sh -p "$SITE" -k "$MYDIR/$KEYFILENAME" -b ${BACKUP_PATHS[*]}