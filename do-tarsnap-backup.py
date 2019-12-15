#!/usr/bin/env python

# originally found here: https://jclement.ca/2014/04/01/tarsnap-pushover.html
# modified by pjv


import subprocess
import time
import argparse

# Arguments #########################################################

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--prefix')
parser.add_argument('-k', '--keyfile')
parser.add_argument('-b', '--backup_paths', nargs='*')

args = parser.parse_args()

##########################################################################

# Configuration #########################################################

MAX_BACKUPS = 20
BACKUP_PREFIX = args.prefix + "_"
BACKUP_ITEMS = args.backup_paths
KEYFILE = args.keyfile
CACHEDIR = "/usr/local/tarsnap-cache" # standard location for deb pkg binary tarsnap install - yours may be different

PUSHOVER_TOKEN = "set_me"
PUSHOVER_USER = "set_me"
NOTIFY_ON_SUCCESS = False

# print KEYFILE
# print BACKUP_PREFIX
# print CACHEDIR
# print BACKUP_ITEMS
# exit(0)

##########################################################################

def notify(title, message, priority):
  subprocess.call([
    "./pushover.sh",
    "-T",
    PUSHOVER_TOKEN,
    "-U",
    PUSHOVER_USER,
    "-p",
    priority,
    "-t",
    title,
    message])

# Perform Backup #########################################################

try:
  result = subprocess.check_output([
    "tarsnap",
    "-c",
    "--keyfile",
    KEYFILE,
    "--cachedir",
    CACHEDIR,
    "--exclude",
    "*cache*",
    "--exclude",
    "wp-less",
    "--quiet",
    "-f", BACKUP_PREFIX + time.strftime('%Y-%m-%d-%H%M%S'),
    ] + BACKUP_ITEMS, stderr=subprocess.STDOUT)
  if NOTIFY_ON_SUCCESS:
    notify(BACKUP_PREFIX + "Backup Complete", ".", "0")
except subprocess.CalledProcessError as e:
  notify(BACKUP_PREFIX + "Backup FAILED", "Error {0} - {1}".format(e.returncode, e.output), "1")


# Perform Pruning ########################################################

archives = subprocess.check_output([
  "tarsnap",
  "--list-archives",
  "--keyfile",
  KEYFILE]).split()
archives = [s for s in archives if s.startswith(BACKUP_PREFIX)]
archives.sort()
archives.reverse()
archives_to_prune = archives[MAX_BACKUPS:]
for archive in archives[MAX_BACKUPS:]:
  try:
    result = subprocess.check_output([
      "tarsnap",
      "-d",
      "--keyfile",
      KEYFILE,
      "--cachedir",
      CACHEDIR,
      "--quiet",
      "-f", archive
      ], stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as e:
    notify(BACKUP_PREFIX + "Pruning FAILED", "Error {0} - {1}".format(e.returncode, e.output), "1")
