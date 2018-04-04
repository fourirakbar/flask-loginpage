import docker

file = open("data.txt", "r")
result = file.read()
print "Isi file data.txt: "+result

name_container = result.split("|")[1]
print "Name container: "+name_container

client = docker.from_env()
client.containers.run()