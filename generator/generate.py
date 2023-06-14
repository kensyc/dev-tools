#!/usr/bin/env python

import os
import sys

from mysql import Mysql
from php import Php
from util.project_data import ProjectData

output = ""


def add_to_output(key: str, value: str):
    global output
    output += f"{key}={value}\n"


project_data = ProjectData(sys.argv[1], sys.argv[2])
cachedir = os.getenv(
    "DEV_TOOLS_CACHE_DIR", os.path.expanduser("~/.cache/dev-tools/")
)

services = {"PHP": Php(project_data), "MYSQL": Mysql(project_data)}

for tool, service in services.items():
    add_to_output(tool + "_SERVICE", service)

# PROJECT
add_to_output("COMPOSE_PROJECT_NAME", project_data.project_name)
add_to_output("COMPOSE_FILE", project_data.compose_file)
add_to_output("PROJECT_FOLDER", project_data.project_folder)

# MYSQL
add_to_output("MYSQL_DATABASE", services["MYSQL"].database())
add_to_output("MYSQL_USER", services["MYSQL"].user())
add_to_output("MYSQL_PASSWORD", services["MYSQL"].user_password())
add_to_output("MYSQL_ROOT_PASSWORD", services["MYSQL"].root_password())

# NODE
add_to_output("NODE_SERVICE", "node:alpine")

filename = os.path.expanduser(cachedir + "/" + sys.argv[2])
os.makedirs(os.path.dirname(filename), exist_ok=True)

f = open(filename, "w")
f.write(output)
f.close()
