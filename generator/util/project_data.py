import os
from typing import Optional

import docker
import yaml
from docker.models.containers import ContainerCollection


class ProjectData:
    def __init__(
        self, project_folder: str, name: str, compose_file: str
    ) -> None:
        self.project_folder = os.path.expanduser(project_folder)
        self.name = name
        self.client = docker.from_env()
        self.containers = self._get_containers()
        self.compose_file = compose_file
        self.compose_yaml = yaml.load(
            open(self.compose_file, "r"), yaml.Loader
        )

    @property
    def project_name(self):
        return os.getenv("COMPOSE_PROJECT_NAME", self.name)

    @property
    def startup_folder(self):
        return os.path.expanduser(
            os.getenv("PROJECT_FOLDER", self.project_folder)
        )

    def get_containers(self) -> Optional[ContainerCollection]:
        return self.containers

    def _get_containers(self) -> Optional[ContainerCollection]:
        filters = {"label": "com.docker.compose.project=" + self.project_name}
        containers = self.client.containers.list(all=True, filters=filters)

        if containers:
            return containers  # pyright: ignore

        return None
