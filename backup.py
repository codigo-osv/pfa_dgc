import datetime
import os
import subprocess

PATH = '/home/observatorio/Dropbox/back/'
FECHA = datetime.datetime.now().strftime('%d-%b-%Y_%H:%M')


ARCHIVO = '{}backup_db_{}.tar'.format(PATH, FECHA)


subprocess.call(['pg_dump', '--format=t', '--dbname=pfa_dgc', '--file=' + ARCHIVO])


#delete files older than 15 days
flist = os.listdir(PATH)
rng = datetime.datetime.now() - datetime.timedelta(days=15)
for file in flist:
    lmod = os.stat(file).st_mtime
    dlmod = datetime.datetime.fromtimestamp(lmod)
    old = dlmod < rng
    if old:
        wp = PATH + file
        os.remove(wp)