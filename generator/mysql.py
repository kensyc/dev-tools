from util.service_finder import ServiceFinder
from util.project_data import ProjectData
from util.parameter_finder import ParameterFinder

class Mysql:
    query = ['mysql', 'mariadb', 'percona']

    def __init__(self, project_data: ProjectData) -> None:
        self.serviceFinder = ServiceFinder(self.query)
        self.serviceName = self.serviceFinder.find_service(
            project_data.get_containers(),
            project_data.get_compose_services()
        )


    def database(self) -> str:
        return ParameterFinder.get_env(
            'MYSQL_DATABASE',
            self.serviceFinder.container
        )


    def user(self) -> str:
        return ParameterFinder.get_env(
            'MYSQL_USER',
            self.serviceFinder.container
        )


    def user_password(self) -> str:
        return ParameterFinder.get_env(
            'MYSQL_PASSWORD',
            self.serviceFinder.container
        )


    def root_password(self) -> str:
        return ParameterFinder.get_env(
            'MYSQL_ROOT_PASSWORD',
            self.serviceFinder.container
        )


    def __str__(self) -> str:
        return self.serviceName
