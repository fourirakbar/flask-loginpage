from flask import Flask, render_template, request, url_for, jsonify
import docker
import subprocess
from subprocess import PIPE
from datetime import datetime
app = Flask(__name__)

@app.route('/tests/endpoint', methods=['POST'])
class NiceLogger:
    def log(self, message):
        datenow = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
        print("{0} |  {1}".format(datenow, message))


class DockerHelper:
    index_port = 9001
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

    def my_test_endpoint(self):
        index_port = index_port + 1
        print "masuk: "+index_port
        input_json = request.get_json(force=True) 
        print request
        print "==="
        # force=True, above, is necessary if another developer 
        # forgot to set the MIME type to 'application/json'
        print 'NRP:', input_json.split("|")[0]
        print 'YOUR IP:', input_json.split("|")[1]

        with open("data.txt", "wb") as fo:
            fo.write(str(input_json))

        getNRP = input_json.split("|")[0] 
        getIP = input_json.split("|")[1]

        config = {
            "NetworkName": "None",
        }

        containerImages = {
            "Squid": "sameersbn/squid:latest"
        }

        containerNames = {
            "Squid": getNRP + "_" + getIP,
        }

        niceLogger = NiceLogger()
        niceLogger.log("Variables:")
        niceLogger.log("")

        dockerHelper = DockerHelper()

        niceLogger.log("Creating {0} network.".format(config["NetworkName"]))
        dockerHelper.create_network()

        niceLogger.log("Adding New Container")
        dockerHelper.run_container(containerNames["Squid"], containerImages['Squid'], ['-p', ''+index_port+':3128'])
        

        return "sukses"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

