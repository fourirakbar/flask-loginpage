import os
import time
import subprocess
import mysql.connector
from subprocess import PIPE
from datetime import datetime

db = mysql.connector.connect(user='taoing', password='fourir96akbar', host='192.168.0.15', database='ta_container')
cursor = db.cursor(buffered=True)

class NiceLogger:
    def log(self, message):
        datenow = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
        print("{0} |  {1}".format(datenow, message))


class DockerHelper:
    niceLogger = NiceLogger()

    def clean_old_images(self):
        command = ["docker", "images", "-q", "-f", "dangling=true"]
        image_ids = self.run_command(command)

        for id in image_ids.stdout.readlines():
            id = id.decode("utf-8")
            id = id.replace("\n", "")

            self.niceLogger.log("Removing container image id " + id)
            command = ["docker", "rmi", "-f", str(id)]
            self.run_command(command)

    def remove_container(self, containerName):
        command = ["docker", "rm", "-f", containerName]
        self.run_command(command)
        self.niceLogger.log(" - Removed " + containerName)

    def create_network(self):
        command = ["docker", "network", "create", config["NetworkName"]]
        self.run_command(command)

    def pull_container_image(self, containerImage):
        command = ["docker", "pull", containerImage]
        self.run_command(command)
        self.niceLogger.log(" - Pulled " + containerImage)

    def run_container(self, containerName, containerImage, args):
        command = ["docker", "run", "-dit", "--workdir", "/root", "--net", config["NetworkName"], "--name", containerName]
        command.extend(args)
        command.append(containerImage)

        popen = self.run_command(command)

        error = popen.stderr.readline().decode("utf-8")

        if error != "":
            error = error.replace("\n", "")
            self.niceLogger.log("An error occurred:" + error)
        else:
            id = popen.stdout.readline().decode("utf-8")
            id = id.replace("\n", "")
            command_mkdir = 'docker exec -d -it '+getIP+' sh -c "mkdir .mitmproxy"'
            os.system(command_mkdir)
            time.sleep(1)

            command_cp = 'docker cp /home/fourirakbar/.mitmproxy/. '+getIP+':/root/.mitmproxy'
            command_cp_2 = 'docker cp /home/fourirakbar/container-data/read_file.sh '+getIP+':/root'
            os.system(command_cp)
            time.sleep(1)
            os.system(command_cp_2)

            command_to_exec = 'docker exec -d -it '+getIP+' sh -c "mitmdump --anticache --anticomp -v --mode transparent --showhost --set client_certs=~/.mitmproxy -w output_file -p '+getPORT+'"'
            print command_to_exec
            os.system(command_to_exec)
            time.sleep(1)
            self.niceLogger.log(" - New container ID " + id)

    # def run_exec_only(execCommand):
    #     command = ["docker", "exec", "-it", containerNames, "-c", "env LA"]

    def run_container_with_exec(self, containerName, containerImage, execCommand, args):
        command = ["docker", "run", "-d", "--net", config["NetworkName"], "--name", containerName]
        command.extend(args)
        command.append(containerImage)
        command.append(execCommand)

        self.run_command(command)

    def run_command(self, command):
        debugcommand = " - {0}".format(" ".join(command))
        self.niceLogger.log(debugcommand)

        popen = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        popen.wait() # wait a little for docker to complete

        return popen

# flag_container=1
print "jancok matek o cok"

readdata = open("data.txt", "r")
boi = readdata.read().split("|")
getNRP = boi[0]
getIP = boi[1]
getPORT = boi[2]

# sql_insert = """INSERT INTO container(name_container, flag) VALUES ('%s', '%s')""" % (getIP, flag_container)
# cursor.execute(sql_insert)
# db.commit()

config = {
    "NetworkName": "host",
}

containerImages = {
    "mitmproxy": "fourirakbar/mitmproxy-oing:version3"
}

containerNames = {
    "mitmproxy": getIP,
}

niceLogger = NiceLogger()
niceLogger.log("Variables:")
niceLogger.log("")

dockerHelper = DockerHelper()

niceLogger.log("Creating {0} network.".format(config["NetworkName"]))
dockerHelper.create_network()

niceLogger.log("Adding SecretProject2.")

name_dir = '/home/fourirakbar/container-data/'+getIP+'_'+getNRP+'_'+getPORT
p = subprocess.Popen('mkdir '+name_dir+'', shell=True)
p.wait()
q = subprocess.call('cp -r /home/fourirakbar/TA/mitmproxy/.mitmproxy/ '+name_dir+'', shell=True)
# q.wait()

dockerHelper.run_container(containerNames["mitmproxy"], containerImages['mitmproxy'], ["-v", name_dir+":/root", "--privileged"])