import glob
import os
from typing import Generator, Optional

import docker
import yaml
from docker.models.containers import ContainerCollection


class ProjectData:
    cached_compose_file = ""

    def __init__(self, project_folder: str, name: str) -> None:
        self.project_folder = os.path.expanduser(project_folder)
        self.name = name
        self.client = docker.from_env()
        self.containers = self._get_containers()

    @property
    def project_name(self):
        return os.getenv("COMPOSE_PROJECT_NAME", self.name)

    @property
    def startup_folder(self):
        return os.path.expanduser(
            os.getenv("PROJECT_FOLDER", self.project_folder)
        )

    @property
    def compose_file(self):
        if not self.cached_compose_file:
            self.cached_compose_file = self.get_compose_file()

        return self.cached_compose_file

    def get_containers(self) -> Optional[ContainerCollection]:
        return self.containers

    def _get_containers(self) -> Optional[ContainerCollection]:
        filters = {"label": "com.docker.compose.project=" + self.project_name}
        containers = self.client.containers.list(all=True, filters=filters)

        if containers:
            return containers  # pyright: ignore

        return None

    def gitignore(self, file: str) -> Generator:
        for line in file:
            if line and "#" not in line:
                yield line

    def get_compose_file(self) -> str:
        compose_file = os.getenv("COMPOSE_FILE")

        if compose_file:
            return compose_file

        compose_file = glob.glob(
            self.project_folder + "/**/docker-compose*", recursive=True
        )

        gitignores = glob.glob(
            self.project_folder + "/**/.gitignore", recursive=True
        )

        # @todo: alternatively just use fd
        ignored_files = []
        for gitignore in gitignores:
            with open(gitignore, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and line != "docker-compose" and "#" not in line:
                        ignored_files.append(line)

        compose_file = list(
            filter(
                lambda file: not any(
                    exclude in file for exclude in ignored_files
                ),
                compose_file,
            )
        )

        match compose_file:
            case 0:
                print("No docker-compose.yml file found in project")
                exit(1)
            case 1:
                compose_file = compose_file[0]
            case _:
                print("Select a compose file:")
                for index in range(0, len(compose_file)):
                    print(f"[{index}] {compose_file[index]}")

                print("")
                compose_file = compose_file[int(input("Selection: "))]

        return compose_file

    def get_compose_services(self) -> dict:
        return yaml.load(open(self.compose_file, "r"), yaml.Loader)
