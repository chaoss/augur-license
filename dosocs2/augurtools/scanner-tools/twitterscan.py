import requests
import subprocess
import sys
import psycopg2
from urllib.parse import urlparse
from subprocess import PIPE

connection_uri = "postgresql://augur:mcguire18@localhost:5433/augur_dev"

connection = psycopg2.connect(
    user = "augur",
    password = "****",
    database = "augur_dev",
    host = "localhost",
    port = 5433,
)
cur = connection.cursor()
cur.execute("SET search_path to spdx;")

i = 0
#API call to get repository path list
r = requests.get("http://newtwitter.augurlabs.io/api/unstable/dosocs/repos").json()
for sector in r:
    #Attain path from sector ('path')
    inner = sector["path"]
    print(inner)
    #Check for MAP entries in augur_repo_map.
    #If no MAP entry, create one
    cur.execute("SELECT repo_path FROM augur_repo_map WHERE" + chr(39) + inner + chr(39) + " " + chr(61) + " repo_path;")
    check = bool(cur.rowcount)
    if check == True:
        print("Record Exists in Mapping Table")
    else:
        #Create a new record in "packages" table.
        #dosocs will determine whether the entry has already been made
        print("Creating Record for " + str(sector["repo_id"]))
        cur.execute("INSERT INTO augur_repo_map(repo_id, repo_path) VALUES (" + str(sector["repo_id"]) + "," + chr(39) + sector['path'] + chr(39) + ");")
        connection.commit()
    #Attempt to create new DoSOCS entry
    print('attempting')
    p = subprocess.Popen('dosocs2 scan ' + inner, shell=True, stdout=PIPE, stderr=PIPE)
    (output, err) = p.communicate()
    print(output)
    print(err)
cur.execute("UPDATE spdx.augur_repo_map a SET dosocs_pkg_name = b.name FROM spdx.packages b WHERE a.repo_path = b.download_location;")
connection.commit()
connection.close()
