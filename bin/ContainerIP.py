import docker
def IPget ():
    client = docker.DockerClient()
    container = client.containers.get("Username4")
    ip_add = container.attrs['NetworkSettings']['IPAddress']
    return ip_add