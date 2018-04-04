import subprocess
from subprocess import PIPE
from datetime import datetime

class NiceLogger:
    def log(self, message):
        datenow = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
        print("{0} |  {1}".format(datenow, message))

class DockerHelper:
    def run_command(self, command):
        debugcommand = " - {0}".format(" ".join(command))
        self.niceLogger.log(debugcommand)

        popen = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        popen.wait(500) # wait a little for docker to complete

        return popen
        
    def create_network(self):
        command = ["docker", "network", "create", config["NetworkName"]]
        self.run_command(command)

    def run_container(self, containerName, containerImage, args):
        command = ["docker", "run", "-d", "--net", config["NetworkName"], "--name", containerName]
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
            self.niceLogger.log(" - New container ID " + id)


getIP = "10.151.36.20"

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
dockerHelper.run_container(containerNames["Squid"], containerImages['Squid'], )