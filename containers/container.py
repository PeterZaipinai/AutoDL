# containers/container.py

class Container:

    def __init__(self, deploy, container_uuid):
        self.deploy = deploy
        self.uuid = container_uuid

    def stop(self, decrease_replica=False):
        return self.deploy.stop_container(self.uuid, decrease_replica)

    def get_events(self):
        return self.deploy.get_container_events(self.uuid)