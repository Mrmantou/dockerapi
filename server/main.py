from flask import Flask, request
from flask_cors import *
import docker
import json
import sys
import datetime


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
        ports = parse_ports(container.attrs['HostConfig']['PortBindings'])
        command = parse_command(container.attrs['Config'])
        dto = {'short_id': container.short_id,
               'name': container.name,
               'image': container.attrs['Config']['Image'],
               'ports': ports,
               'created': parse_created(container.attrs['Created']),
               'command': command,
               'status': parse_status(container),   # container.status,
               'started': container.attrs['State']['StartedAt'],
               'ended': container.attrs['State']['FinishedAt'],
               'exitcode': container.attrs['State']['ExitCode'],
               # 'attrs': container.attrs
               }
        result.append(dto)

    return json.dumps(result)


def parse_port(key, value):
    hostPorts = [item['HostPort'] for item in value]
    return '/'.join(hostPorts) + '->' + key


def parse_ports(portBindings):
    if portBindings == None:
        return []
    else:
        return [parse_port(key, value) for key, value in portBindings.items()]


def parse_command(entrypoint):
    if entrypoint['Entrypoint'] == None:
        return ' '.join(entrypoint['Cmd'])
    else:
        return ' '.join(entrypoint['Entrypoint'])


def parse_status(container):
    if container.status == 'running':
        started = container.attrs['State']['StartedAt']
        return f'Up {calculate_timeperiod(started)}'
    elif container.status == 'exited':
        ended = container.attrs['State']['FinishedAt']
        exitcode = container.attrs['State']['ExitCode']
        return f'Exited({exitcode}) {calculate_timeperiod(ended)} ago'


def parse_created(created):
    return f'{calculate_timeperiod(created)} ago'


def calculate_timeperiod(started):
    start = datetime.datetime.strptime(started[:19], '%Y-%m-%dT%H:%M:%S')
    end = datetime.datetime.utcnow()
    diff = end-start
    print(started)
    print(f'start={start} end={end} diff={diff}')
    if(diff.days > 0):
        return f'{diff.days} day(s)'
    elif int(diff.seconds/60/60) > 0:
        return f'{int(diff.seconds/60/60)} hour(s)'
    elif int(diff.seconds/60) > 0:
        return f'{int(diff.seconds/60)} minute(s)'
    elif diff.seconds > 0:
        return f'{diff.seconds} second(s)'
    else:
        return 'A moument'


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


@app.route('/docker/containers/start/<id_or_name>')
def docker_containers_start(id_or_name):
    result = 'Unhandle'
    try:
        container = client.containers.get(id_or_name)
        container.start()
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
