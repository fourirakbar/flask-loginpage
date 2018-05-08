import subprocess

getNRP = "5114100115"
getIP = "10.151.36.38"
getPORT = "9001"

name_dir = '/home/fourirakbar/container-data/'+getNRP+'_'+getIP+'_'+getPORT
p = subprocess.Popen('mkdir '+name_dir+'', shell=True)
p.wait()