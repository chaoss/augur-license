import subprocess
import psycopg2
from subprocess import PIPE
import json
import re
import os
import requests
from os.path import expanduser
from pathlib import Path
import sbom_populate as p
import initial_scans as s
import sys

if __name__ == "__main__":
    if not len(sys.argv) > 1:
      print("Please provide a path")
      exit()
    else:
      args1 = sys.argv[1]
      if not args1.endswith("/"):
        args1 += "/"

    with open(args1 + "augur.config.json") as json_file:
      with open("spdx.config.json") as json_file2:
        config = json.load(json_file)
        dbname = config["Database"]["database"]
        user = config["Database"]["user"]
        password = config["Database"]["password"]
        host = config["Database"]["host"]
        port = config["Database"]["port"]
        config2 = json.load(json_file2)
        dsfile = config2["license_worker"]["tagfile"]
        depth = config2["license_worker"]["search_depth"]
        ipath = config["workers"]["facade_worker"]["repo_directory"]
        home = expanduser("~")

        print("IPATH EQUALS " + ipath)
        print("HOME EQUALS " + home)

        configtools = 'postgresql://{}:{}@{}:{}/{}'.format(
            user, password, host, port, dbname
        )

        Path(home+"/.config/dosocs2").mkdir(parents=True, exist_ok=True) 

        with open("dosocs2-example.conf") as configfile:
            content = configfile.read()
            content_new = re.sub('(connection_uri = .*)\n', "connection_uri = " + configtools + "?options=--search_path=spdx\n", content)
            with open("dosocs2.conf","w+") as outfile:
                outfile.write(content_new)
            with open(home + "/.config/dosocs2/dosocs2.conf","w+") as coreconfig:
                coreconfig.write(content_new)

        wd = os.getcwd()
        mwd = wd + "/dosocs2.conf"

        print("---------------------")
        print("INITIAL SCANS RUNNING")
        print("---------------------")
        s.scan(dbname, user, password, host, port, dsfile, ipath, depth, mwd)
        #print(os.getcwd())
        os.chdir(wd)
        #print(os.getcwd())
        print("------------------")
        print("SBOM SCANS RUNNING")
        print("------------------")
        p.scan(dbname, user, password, host, port, dsfile, ipath, mwd)
