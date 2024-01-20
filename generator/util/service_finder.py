from typing import Optional
from docker.models.containers import Container, ContainerCollection

class ServiceFinder:

    def __init__(self, query: list[str]) -> None:
        self.query = query
        self.container = None


    def _in_container_command(
        self,
        container: Container
    ) -> bool:
        return any(
            psub in cmd
            for cmd in container.attrs["Args"] # pyright: ignore
            for psub in self.query
        )


    def _in_container_name(
        self,
        container: Container
    ) -> bool:
        return any(
            psub in container.labels["com.docker.compose.service"]
            for psub in self.query
        )


    def _in_container_image(
        self,
        container: Container
    ) -> bool:
        return any(
            psub in tag
            for tag in container.image.tags # pyright: ignore
            for psub in self.query
        )


    def find_service_by_container(
        self,
        containers: ContainerCollection
    ) -> Optional[Container]:
        for container in containers:  # pyright: ignore
            if self._in_container_name(container):
                self.container = container
                return container

        for container in containers:  # pyright: ignore
            if self._in_container_command(container):
                self.container = container
                return container

        for container in containers:  # pyright: ignore
            if self._in_container_image(container):
                self.container = container
                return container

        return None


    def find_service_by_docker_compose(
        self,
        compose_yaml: dict
    ) -> Optional[str]:
        for psub in self.query:
            for service_name, service in compose_yaml["services"].items():
                if psub in service_name or psub in service.get("image", ""):
                    return service_name

        return None


    def find_service(
            self,
            containers: Optional[ContainerCollection],
            compose_yaml: Optional[dict]
        ) -> str:
        if containers:
            service = self.find_service_by_container(containers)

            if service:
                return service.labels["com.docker.compose.service"]

        if compose_yaml:
            serviceName = self.find_service_by_docker_compose(compose_yaml)

            if serviceName:
                return serviceName

        return ''
