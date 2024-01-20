from util.service_finder import ServiceFinder
from util.project_data import ProjectData
from util.parameter_finder import ParameterFinder

class Mssql:
    query = ['mssql']

    def __init__(self, project_data: ProjectData) -> None:
        self.serviceFinder = ServiceFinder(self.query)

        compose_yaml = project_data.compose_yaml
        self.serviceName = self.serviceFinder.find_service(
            project_data.get_containers(),
            compose_yaml
        )
        if compose_yaml:
            self.serviceYaml = compose_yaml["services"].get(self.serviceName)


    def sa_password(self) -> str:
        return ParameterFinder.get_env(
            'MSSQL_SA_PASSWORD',
            self.serviceFinder.container,
            self.serviceYaml
        )


    def __str__(self) -> str:
        return self.serviceName
