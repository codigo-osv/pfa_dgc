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
    wp = PATH + file
    lmod = os.stat(wp).st_mtime
    dlmod = datetime.datetime.fromtimestamp(lmod)
    if dlmod < rng:
       os.remove(wp)

#copy backup files to external drive
subprocess.call(['cp', '-ur', PATH, '/media/observatorio/OSV_Backup'])
