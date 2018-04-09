readdata = open("data.txt", "r")
boi = readdata.read().split("|")
print len(boi)

if len(boi) == 1 :
    def_port = 9001
    
else:
    print "ga ada"