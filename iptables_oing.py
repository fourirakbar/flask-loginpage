# import os
# boi = raw_input("Test: ")
# os.system('iptables -'+boi+'')

from subprocess import *
boi = raw_input("Test: ")
sts = Popen("iptables"+" "+"-"+boi+"", shell=True).wait()
print sts