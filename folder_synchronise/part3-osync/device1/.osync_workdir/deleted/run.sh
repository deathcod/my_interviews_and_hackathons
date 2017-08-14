#!/bin/sh
CONFLICT_BACKUP=yes
CONFLICT_BACKUP_MULTIPLE=yes
CONFLICT_BACKUP_DAYS=30
LOGFILE="/home/device3/D/log.txt"
IGNORE_OS_TYPE=yes
REMOTE_HOST_PING=yes
SOFT_DELETE=yes
RESUME_TRY=2
CREATE_DIRS=yes
./osync/osync.sh --initiator=/home/device3/ --target=ssh://device1@127.0.1.1:22//home/device1/

