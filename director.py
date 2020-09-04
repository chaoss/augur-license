import subprocess
import psycopg2
from subprocess import PIPE
import json
import re
import os
import requests

import sbom_populate as p
import initial_scans as s

if __name__ == "__main__":
    with open("../../augur.config.json") as json_file:
        config = json.load(json_file)
        dbname = config["Database"]["database"]
        user = config["Database"]["user"]
        password = config["Database"]["password"]
        host = config["Database"]["host"]
        port = config["Database"]["port"]
        dsfile = config["Workers"]["license_worker"]["tagfile"]
        ipath = config["Workers"]["facade_worker"]["repo_directory"]

        configtools = 'postgresql://{}:{}@{}:{}/{}'.format(
            user, password, host, port, dbname
        )

        with open("dosocs2-example.conf") as configfile:
            content = configfile.read()
            content_new = re.sub('(connection_uri = .*)\n', "connection_uri = " + configtools + "\n", content)
            with open("dosocs2.conf","w+") as outfile:
                outfile.write(content_new)

        print("---------------------")
        print("INITIAL SCANS RUNNING")
        print("---------------------")
        s.scan(dbname, user, password, host, port, dsfile, ipath)
        print("------------------")
        print("SBOM SCANS RUNNING")
        print("------------------")
        p.scan(dbname, user, password, host, port, dsfile, ipath)
