from pathlib import Path
import sbom_populate as p
import initial_scans as s
import sys
import json
import os.path 
import re

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
        ipath = config["Workers"]["facade_worker"]["repo_directory"]
        home = os.path.expanduser("~/")

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
