from flask import Flask, request
from flask_cors import *
import docker
import json
import sys


app = Flask(__name__)
CORS(app, supports_credentials=True)

client = docker.from_env()


def parse_start_port():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return 4000


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/docker/containers')
def docker_containers():
    result = []
    for container in client.containers.list(all=True):
        ports = [parse_port(key, value)
                 for key, value in container.attrs['HostConfig']['PortBindings'].items()]
        command = parse_command(container.attrs['Config'])
        dto = {'short_id': container.short_id,
               'name': container.name,
               'image': container.attrs['Config']['Image'],
               'ports': ports,
               'started': container.attrs['State']['StartedAt'],
               'command': command,
               'status': container.status,
               # 'attrs': container.attrs
               }
        result.append(dto)

    return json.dumps(result)


def parse_port(key, value):
    hostPorts = [item['HostPort'] for item in value]
    return '/'.join(hostPorts) + '->' + key


def parse_command(entrypoint):
    if entrypoint['Entrypoint'] == None:
        return ' '.join(entrypoint['Cmd'])
    else:
        return ' '.join(entrypoint['Entrypoint'])


@app.route('/docker/containers/stop/<id_or_name>')
def docker_containers_stop(id_or_name):
    result = 'Unhandle'
    try:
        container = client.containers.get(id_or_name)
        container.stop()
    except:
        result = 'Error'
    else:
        result = 'OK'

    return result


@app.route('/docker/images')
def docker_images():
    result = []
    for image in client.images.list():
        dto = {'short_id': image.short_id[7:],
               'id': image.id[7:],
               'tags': image.tags}
        result.append(dto)

    return json.dumps(result)


@app.route('/docker/images/remove/<name>')
def docker_images_remove(name):
    result = 'Unhandle'
    try:
        client.images.remove(name, True)
    except:
        result = 'Error'
    else:
        result = 'OK'

    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=parse_start_port())
