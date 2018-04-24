import subprocess
import netifaces

gw_device = netifaces.gateways()['default'][netifaces.AF_INET][1]

p = subprocess.Popen(('sudo', 'tcpdump', '-i', gw_device, '|', 'awk', `'{ print gensub(/(.*)\..*/,"\\1","g",$3), $4, gensub(/(.*)\..*/,"\\1","g",$5) }'`), stdout=subprocess.PIPE)
for row in iter(p.stdout.readline, b''):
    print row()   # process here