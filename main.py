from flask import Flask, request
from flask_cors import *
import docker
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

client = docker.from_env()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/docker/containers')
def docker_containers():
    result = []
    for container in client.containers.list():
        dto = {'short_id': container.short_id,
               'name': container.name,
               'status': container.status}
        result.append(dto)

    return json.dumps(result)


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
        tags = []
        for tag in image.tags:
            tags.append(tag)
        dto = {'short_id': image.short_id,
               'tag': json.dumps(tags)}
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
    app.run(host='0.0.0.0', port=8002)
