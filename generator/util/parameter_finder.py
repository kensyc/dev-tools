import os
from typing import Optional

from docker.models.containers import Container

class ParameterFinder:

    @staticmethod
    def get_env(env: str, container: Optional[Container]) -> str:
        os_env = os.getenv(env)
        if os_env:
            return os_env

        if container is not None:
            for cont_env in container.attrs['Config']['Env']: # pyright: ignore
                if env in cont_env:
                    splitenv = cont_env.split(sep='=')
                    return splitenv[1]
        
        return ''
