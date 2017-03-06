import random

random.seed()
sss = """# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
%d *	* * *	root    cd / && run-parts --report /etc/cron.hourly
%d %d	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
%d %d	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
%d %d	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
""" % (
        random.randint(0, 59),
        random.randint(0, 59), random.randint(0, 23),
        random.randint(0, 59), random.randint(0, 23),
        random.randint(0, 59), random.randint(0, 23),
)
with open('/etc/crontab', 'w') as ouf:
    ouf.write(sss)
