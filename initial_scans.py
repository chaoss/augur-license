import subprocess
import psycopg2
from subprocess import PIPE
import json
import re
import time
import os
import requests

flevel = 0

def depthwalk(ipath, depth, match):
   k = 0
   #print("IPATH " + ipath)
   if depth > 0:
     for dir in os.listdir(ipath):
       if not ipath.endswith("/"):
           usedir = ipath + "/" + dir
       else:
           usedir = ipath + dir
       #print(str(usedir) + " " + str(depth))
       if os.path.isdir(usedir):
           #print("directory!")
           if dir == match:
              print("FOLDER FOUND: " + str(usedir))
              pathtot.append(usedir)
              break
           depthwalk(usedir, depth - 1, match)
       #else:
           #print("not dir")

def scan(dbname, user, password, host, port, dsfile, ipath, depth):
    connection = psycopg2.connect(
        user = user,
        password = password,
        database = dbname,
        host = host,
        port = port,
    )
    print("********************")
    cur = connection.cursor()
    r = cur.execute("set search_path to augur_data; select repo_path, repo_id, repo_group_id, repo_name from repo order by repo_group_id;")
    rec = cur.fetchall()
    for sector in rec:
        global pathtot
        pathtot = []
        print(sector)
        repo_id = sector[1]
        print("****************")
        print(repo_id)
        cur.execute("set search_path to spdx;")
        cur.execute("select sbom_scan from augur_data.repo_sbom_scans where repo_id = " + str(repo_id) + " LIMIT 1;")
        determin = cur.fetchall()
        if not determin:
            cur.execute("select dosocs_pkg_id from spdx.augur_repo_map where repo_id = " + str(repo_id) + " LIMIT 1;")
            records = cur.fetchall()
            print("****************")
            print(str(sector[0]))
            if not ipath.endswith("/"):
            	ipath = ipath + "/"
            #path = ipath + str(sector[3])
            os.chdir(ipath)
            print("---------------")
            #need to make this a config parameter
            depthwalk(ipath, depth, sector[3])
            time.sleep(0.2)
            print("INSIDE: "  + str(pathtot))
            print("---------------")
            if pathtot != []:
                path = pathtot[0]
                print("PATH: " + str(path))
                print("SELECT repo_path FROM spdx.augur_repo_map WHERE " + chr(39) + path + chr(39) + " " + chr(61) + " repo_path;")
                cur.execute("SELECT repo_path FROM spdx.augur_repo_map WHERE " + chr(39) + path + chr(39) + " " + chr(61) + " repo_path;")
                if str(len(cur.fetchall())) == "0":
                    print("ALL CHECKS PASSED")
                    #Create a new record in "packages" table.
                    #dosocs will determine whether the entry has already been made
                    print("Creating Record for " + str(sector[1]))
                    #cur.execute("INSERT INTO spdx.augur_repo_map(repo_id, repo_path) VALUES (" + str(sector[1]) + "," + chr(39) + str(sector[0]) + str(sector[3]) + chr(39) + ");")
                    cur.execute("INSERT INTO spdx.augur_repo_map(repo_id, repo_path) VALUES (" + str(sector[1]) + "," + chr(39) + path + chr(39) + ");")
                    connection.commit()
                    #Attempt to create new DoSOCS entry
                    print("CREATING NEW DOSOCS DOCUMENT")
                    print(path)
                    p = subprocess.Popen(['dosocs2', 'scan', str(path)], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print(str(p.communicate()))
                    (output) = p
                    print("####################")
                    print(output)
                    print("RECORD CREATED")
                else:
                    print("RECORD EXISTS IN MAP TABLE")
            else:
                print("NO DIRECTORY, SKIPPING")
        else:
            print("DUPLICATE RECORD FOUND IN REPO_SBOM_SCANS. SKIPPING...")
    cur.execute("update augur_repo_map a set dosocs_pkg_name = b.name from packages b where a.repo_path = b.download_location;")
    cur.execute("update augur_repo_map a set dosocs_pkg_id = b.package_id from packages b where a.repo_path = b.download_location;")
    connection.commit()
    cur.close()
    connection.close()
    return
