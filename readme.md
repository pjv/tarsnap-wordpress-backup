### Why you shouldn't use this

This backup scripting code is being released by [request](https://github.com/WordOps/WordOps/issues/15#issuecomment-565737000) and not as a product. This code is a _modified version_ of my own crappy, highly idiosyncratic, and super-not-refactored code for doing backups of wordpress sites I host to tarsnap. The modifications HAVE NOT BEEN TESTED and there are almost certainly bugs in this initial release version (if anyone does decide to use it and finds and fixes bugs in a generally useful way, send me pull requests).

This code is being released with **zero support** and little explanation. If you are an _actual_ sys admin and know enough bash and python scripting to get by, it should be reasonably easy to follow and modify to suit your purposes. If you can't make sense of the bash scripts, then you REALLY shouldn't use this. Really.

#### Dependencies

1. [tarsnap](https://www.tarsnap.com/download.html). If you are on a debian or ubuntu system, just install the [binary package](https://www.tarsnap.com/pkg-deb.html).
2. python
3. [pushover](https://pushover.net/). This is for push notifications on failed backups. You can get an account for free and create the necessary api key. This is an artifact of this code being kind of old and working as-is. I've since replaced all my own push alerts in most places in my infrastructure with [pushbullet](https://www.pushbullet.com/) instead, but apparently have never gotten to it in my backup scripts. If I ever do, I'll replace this dependency (and `pushover.sh`) with pushbullet instead. Pull requests welcome.

#### Usage

First you would clone this repo somewhere. On my box it's in `/home/backups`.

Then for each wordpress site you host, make a copy of the `site1` directory and rename it in a meaningful way (with no spaces). On my box, I name them with just some initials like BTB, MMS, etc. The name of the directory becomes the "machine" name for tarsnap purposes, so you have a separate tarsnap backup for each wp site. Customize the `backup.sh` script for the site. (This is not [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) and there could just be one backup.sh script used for all sites. The reason I have a separate one for each site is because I sometimes add site specific stuff).

Generate a tarsnap key for each site and put it in the site directory, replacing the dummy file in there called `tarsnap.key`. Whatever you name that file, needs to be configured in the site's `backup.sh` script as `KEYFILENAME`. You can use the same keyfile for all your sites, but I like to generate a separate keyfile for each site and my customer (the site's owner) gets a read-only key for the same so they have independent access to the backups (AKA pjv got hit by a bus insurance).

Set up a crontab entry to run `daily_backups.sh` in the middle of the night (or whenever the traffic is lowest on your box). To minimize permissions issues, I use root's crontab for this (`sudo crontab -e`). My entry looks like this:

`0 2 * * * /home/backups/daily_backups.sh >/dev/null 2>&1`

NOTE: tarsnap is kind of arcane and pretty expensive compared to other online backup solutions. I use it because I am paranoid and I think @cperciva is cool.