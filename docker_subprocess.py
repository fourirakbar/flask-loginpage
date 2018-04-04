'''
This script brings up the entire stack of Docker containers, removing the current ones.

Docker compose was tried for this task and it wasn't customisable enough.
Docker cloud was tried (with stack files) and was buggy (failed to launch, no logs returned).
Docker machine was tried, but it can't connect to existing servers only ones it created.
Rancher was too heavy weight for the task, as the containers are lightweight in DigitalOcean.
Kubernetes would've been too heavy weight for DigitalOcean.
It was written in Powershell and worked. But then converting it to Bash was too much effort.
Powershell for Linux is too much effort to install without a debian package (and none standard)
'''

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

        popen = self.run_command(command)

        error = popen.stderr.readline().decode("utf-8")

        if error != "":
            error = error.replace("\n", "")
            self.niceLogger.log("An error occurred:" + error)
        else:
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
        popen.wait(500) # wait a little for docker to complete

        return popen


# Some questions
containerNameSuffix = ""
gethost = input("Local mode [Y/n]?")
if gethost == "":
    containerNameSuffix = "-local"

registry = ""

# Config
config = {
    "NetworkName": "NginxNetwork",
    "PapertrailUrl": "top-secret-url",
    "DataDogApiKey": "TOPSECRET-KEY"
}

containerImages = {
    "Datadog": "datadog/docker-dd-agent:latest",
    "Papertrail": "gliderlabs/logspout",
    "SecretProject1": registry + "SecretProject1:latest",
    "Nginx": registry + "nginx-custom:latest",
    "SecretProject2": registry + "SecretProject2:latest",
}

containerNames = {
    "Datadog": "datadog" + containerNameSuffix,
    "Papertrail": "papertrail" + containerNameSuffix,
    "SecretProject1": "SecretProject1" + containerNameSuffix,
    "Nginx": "nginx" + containerNameSuffix,
    "SecretProject2": "SecretProject2" + containerNameSuffix,
}

niceLogger = NiceLogger()
niceLogger.log("Variables:")
niceLogger.log("Container name suffix: " + containerNameSuffix)
niceLogger.log("Registry prefix: " + registry)
niceLogger.log("")

niceLogger.log("Cleaning images with <none> tags.")

dockerHelper = DockerHelper()
dockerHelper.clean_old_images()

niceLogger.log("Removing containers.")
dockerHelper.remove_container(containerNames["Datadog"])
dockerHelper.remove_container(containerNames["Papertrail"])
dockerHelper.remove_container(containerNames["SecretProject1"])
dockerHelper.remove_container(containerNames["Nginx"])
dockerHelper.remove_container(containerNames["SecretProject2"])

niceLogger.log("Pulling new images.")
dockerHelper.pull_container_image(containerImages["Datadog"])
dockerHelper.pull_container_image(containerImages["Papertrail"])
dockerHelper.pull_container_image(containerImages["SecretProject1"])
dockerHelper.pull_container_image(containerImages["Nginx"])
dockerHelper.pull_container_image(containerImages["SecretProject2"])

niceLogger.log("Creating {0} network.".format(config["NetworkName"]))
dockerHelper.create_network()

niceLogger.log("Adding SecretProject2.")
dockerHelper.run_container(containerNames["SecretProject2"], containerImages["SecretProject2"],
                           ["--env-file", "SecretProject2-env.list"])

# Add papertrail/datadog logging to DigitalOcean only
if containerNameSuffix == "":
    niceLogger.log("Adding datadog.")
    dataDogArgs = ["-v", "/var/run/docker.sock:/var/run/docker.sock:ro",
                   "-v", "/proc/:/host/proc/:ro",
                   "-v", "/sys/fs/cgroup/:/host/sys/fs/cgroup:ro",
                   "-e", "API_KEY=" + config["DataDogApiKey"]
                   ]
    dockerHelper.run_container(containerNames["Datadog"], containerImages["Datadog"], dataDogArgs)

    niceLogger.log("Adding papertrail.")
    paperTrailArgs = ["-e", 'SYSLOG_HOSTNAME="{{.ContainerName}}"',
                      "--restart=always",
                      "-v", "/var/run/docker.sock:/var/run/docker.sock"
                      ]
    papertTrailExec = "syslog://" + config["PapertrailUrl"]
    dockerHelper.run_container_with_exec(containerNames["Papertrail"], containerImages["Papertrail"], papertTrailExec,
                                         paperTrailArgs)
else:
    niceLogger.log("Skipping datadog and papertrail for local mode.")

niceLogger.log("Adding SecretProject1.")
dockerHelper.run_container(containerNames["SecretProject1"], containerImages["SecretProject1"],
                           ["--expose", "5000", "--env-file", "SecretProject1-env.list"])

niceLogger.log("Adding Nginx.")
nginxArgs = ["-p", "80:80",
             "-p", "443:443",
             "--link", containerNames["SecretProject1"] + ":SecretProject1"
             ]
dockerHelper.run_container(containerNames["Nginx"], containerImages["Nginx"], nginxArgs)