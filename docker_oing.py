import subprocess
from subprocess import PIPE
from datetime import datetime

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
        command = ["docker", "run", "-d", "--net", config["NetworkName"], "--name", containerName]
        command.extend(args)
        command.append(containerImage)

        print "Kelar download bosku"

        popen = self.run_command(command)

        error = popen.stderr.readline().decode("utf-8")

        print "===="
        print error
        print "===="

        if error != "":
            print "Masuk if"
            error = error.replace("\n", "")
            self.niceLogger.log("An error occurred:" + error)
        else:
            print "Masuk else"
            id = popen.stdout.readline().decode("utf-8")
            id = id.replace("\n", "")
            self.niceLogger.log(" - New container ID " + id)

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


getIP = "10.151.36.21"

config = {
    "NetworkName": "None",
}

containerImages = {
    "Squid": "sameersbn/squid:latest"
}

containerNames = {
    "Squid": "IP_" + getIP,
}

niceLogger = NiceLogger()
niceLogger.log("Variables:")
niceLogger.log("")

dockerHelper = DockerHelper()

niceLogger.log("Creating {0} network.".format(config["NetworkName"]))
dockerHelper.create_network()

niceLogger.log("Adding SecretProject2.")
dockerHelper.run_container(containerNames["Squid"], containerImages['Squid'], ["-p", "9002:3128"])