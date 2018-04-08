readfile = open("data.txt", "r")
split = readfile.read().split("|")
nrp = split[0]
ip = split[1]
print nrp
print ip