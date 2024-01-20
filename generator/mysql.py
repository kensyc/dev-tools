import sys
from typing import Optional
from util.service_finder import ServiceFinder
from util.project_data import ProjectData
from util.parameter_finder import ParameterFinder

class Mysql:
    query = ['mysql', 'mariadb', 'percona']

    def __init__(
            self,
            project_data: ProjectData,
        ) -> None:
        self.serviceFinder = ServiceFinder(self.query)

        compose_yaml = project_data.compose_yaml
        self.serviceName = self.serviceFinder.find_service(
            project_data.get_containers(),
            compose_yaml
        )
        if compose_yaml:
            self.serviceYaml = compose_yaml["services"].get(self.serviceName)



    def database(self) -> str:
        return ParameterFinder.get_env(
            'MYSQL_DATABASE',
            self.serviceFinder.container,
            self.serviceYaml
        )


    def user(self) -> str:
        return ParameterFinder.get_env(
            'MYSQL_USER',
            self.serviceFinder.container,
            self.serviceYaml
        )


    def user_password(self) -> str:
        return ParameterFinder.get_env(
            'MYSQL_PASSWORD',
            self.serviceFinder.container,
            self.serviceYaml
        )


    def root_password(self) -> str:
        return ParameterFinder.get_env(
            'MYSQL_ROOT_PASSWORD',
            self.serviceFinder.container,
            self.serviceYaml
        )


    def __str__(self) -> str:
        return self.serviceName
