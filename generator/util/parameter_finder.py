import os
from typing import Optional

from docker.models.containers import Container


class ParameterFinder:
    @staticmethod
    def get_env(
        env: str, container: Optional[Container], compose_yaml: Optional[dict]
    ) -> str:
        os_env = os.getenv(env)
        if os_env:
            return os_env

        if container is Container:
            for cont_env in container.attrs["Config"]["Env"]:
                if env in cont_env:
                    splitenv = cont_env.split(sep="=")
                    return splitenv[1]

        if compose_yaml:
            env_yaml = compose_yaml.get("environment")

            if env_yaml is None:
                return ""

            for env_str in env_yaml:
                splitenv = env_str.split(sep="=")
                if splitenv[0] == env:
                    return splitenv[1]
                    # todo: get value from something like "${MYSQL_ROOT_PASSWORD:-toor}"

        return ""
