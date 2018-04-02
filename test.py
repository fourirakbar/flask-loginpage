import redis

POST_USERNAME = "5114100115"
IP_ADDR = "10.151.36.38"
r = redis.StrictRedis(host='localhost', port=6379, db=0)
boi = r.get(POST_USERNAME)

if boi:
    print "NRP sudah digunakan"
    # if boi == "10.151.36.38":
    #     print "aaa"
    # else:
    #     r.set(POST_USERNAME, IP_ADDR)
else:
    r.set(POST_USERNAME, IP_ADDR)   