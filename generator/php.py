from util.service_finder import ServiceFinder
from util.project_data import ProjectData

class Php:
    query = ['php', 'application']

    def __init__(self, project_data: ProjectData) -> None:
        serviceFinder = ServiceFinder(self.query)

        self.serviceName = serviceFinder.find_service(
            project_data.get_containers(),
            project_data.compose_yaml
        )

    def __str__(self) -> str:
        return self.serviceName
