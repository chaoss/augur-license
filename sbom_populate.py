import subprocess
import psycopg2
from subprocess import PIPE
import json
import re
import os
import requests

#class DoSOCSv2(object):
    #"""Uses the DoSOCSv2 database to return dataframes with interesting GitHub indicators"""

def parse_json(doc_1, cre_1, pac_1, pac_lif_1, pac_2, fil_dat_1, fil_rel_1, bas_rel_1, cov_1, cur, repo_id):
    license_information = {}
    temp_1 = {}
    for i in range(0, int(len(doc_1[0])/2)):
        j = i*2
        temp_1[doc_1[0][j]] = doc_1[0][j+1]

    doc_1_temp = {**temp_1}

    temp_1 = {}
    for i in range(0, int(len(cre_1[0])/2)):
        j = i*2
        temp_1[cre_1[0][j]] = cre_1[0][j+1]

    cre_1_temp = {**temp_1}

    temp_1 = {}
    for i in range(0, int(len(pac_1[0])/2)):
        j = i*2
        temp_1[pac_1[0][j]] = pac_1[0][j+1]
    temp_2 = {}
    for i in range(0, int(len(pac_lif_1[0])/2)):
        j = i*2
        temp_2[pac_lif_1[0][j]] = pac_lif_1[0][j+1]
    temp_3 = {}
    for i in range(0, int(len(pac_2[0])/2)):
        j = i*2
        temp_3[pac_2[0][j]] = pac_2[0][j+1]

    pac_temp = {**temp_1, **temp_2, **temp_3}

    temp_2 = {}
    for g in range(0, int(len(fil_dat_1))):
        temp_1 = {}
        for i in range(0, int(len(fil_dat_1[g])/2)):
            j = i*2
            temp_1[fil_dat_1[g][j]] = fil_dat_1[g][j+1]
        temp_1['File Relationship'] = fil_rel_1[g][2].split(": ")[1]
        temp_2["File " + str(g)] = temp_1
    fil_temp = {**temp_2}

    temp_2 = {}
    for k in range(0, int(len(bas_rel_1))):
        temp_2["Relationship " + str(k)] = bas_rel_1[k][1]
    bas_rel_temp = {**temp_2}

    temp_1 = {}
    for i in range(0, int(len(cov_1[0])/2)):
        j = i*2
        temp_1[cov_1[0][j]] = cov_1[0][j+1]

    cov_temp = {**temp_1}

    license_information['Document Information'] = doc_1_temp
    license_information['Creation Information'] = cre_1_temp
    license_information['Package Information'] = pac_temp
    license_information['File Information'] = fil_temp
    license_information['Package Relationships'] = bas_rel_temp
    license_information['License Coverage'] = cov_temp

    #print(license_information)

    #with open('ex.json', 'w+') as example:
    #    json.dump(license_information, example)
    cur.execute("insert into augur_data.repo_sbom_scans(repo_id, sbom_scan) VALUES(" + str(repo_id)  + "," +  chr(39) + str(json.dumps(license_information)).replace("'", "") + chr(39) + ");")

def grabreg(records, repo_id, dsfile):
    print("DETAILS FOUND. CREATING DOCUMENT")
    proc = subprocess.Popen("dosocs2 generate " + str(records[0][0]), shell=True, stdout=PIPE, stderr=PIPE)
    varerr = str(str(proc.stderr.read()).split(" ")[3])
    charvarerr = varerr.split("\\")[0]
    print("Document_id: " + str(charvarerr))
    #f = open("/home/sean/dosocs2/accessDB/scans-tv/" + repo_name + "-full.txt","w")
    #proc = subprocess.call("dosocs2 print " + str(charvarerr) + " -T 2.0.tag.coverage", shell=True, stdout=f, stderr=f)
    pope = subprocess.Popen("dosocs2 print " + str(charvarerr) + " -T " + dsfile, shell=True, stdout=PIPE, stderr=PIPE)
    out, err = pope.communicate()
    #if out:
        #with open('ex-raw.txt', 'w+') as example:
        #    example.write(out.decode('UTF-8'))
    if err:
        print(err.decode('UTF-8'))
    #print (out)
    #package_sr_1 = re.findall(r'(PackageName): (.*)\n(SPDXID): (.*)\n(PackageVersion|)? ?(.*|)\n?(PackageFileName): (.*)\n(PackageSupplier): (.*)\n(PackageOriginator): (.*)\n(PackageDownloadLocation): (.*)\n(PackageVerificationCode):? ?(.*|)\n?(PackageHomePage): (.*)\n(PackageLicenseConcluded):', out.decode('UTF-8'))
    doc_1 = re.findall(r'(DataLicense): (.*)\n(SPDXID): (.*)\n(DocumentNamespace): (.*)\n(DocumentName): (.*)\n(DocumentComment|): ?(.*|)\n?(LicenseListVersion):(.*)', out.decode('UTF-8'))
    cre_1 = re.findall(r'(Creator): (.*)\n(Created): (.*)\n(CreatorComment|): ?(.*|)', out.decode('UTF-8'))
    pac_1 = re.findall(r'(PackageName): (.*)\n(SPDXID): (.*)\n(PackageFileName): (.*)\n(PackageDownloadLocation): (.*)\n(PackageVerificationCode): (.*)\n(PackageHomePage): (.*)\n(PackageLicenseConcluded): (.*)\n(PackageLicenseDeclared): (.*)', out.decode('UTF-8'))
    pac_lif_1 = re.findall(r'(PackageLicenseInfoFromFiles): (.*)', out.decode('UTF-8'))
    pac_2 = re.findall(r'(PackageCopyrightText): (.*)', out.decode('UTF-8'))
    fil_dat_1 = re.findall(r'(FileName): (.*)\n(SPDXID): (.*)\n(FileType): (.*)\n(FileChecksum): (.*)\n(LicenseConcluded): (.*)\n(LicenseInfoInFile): (.*)\n(LicenseComments|): ?(.*|)\n(FileCopyrightText): (.*)\n(FileComment|): ?(.*|)\n(FileNotice|): ?(.*|)\n', out.decode('UTF-8'))
    fil_rel_1 = re.findall(r'(## Relationships)\n((\w.*)\n)*', out.decode('UTF-8'))
    bas_rel_1 = re.findall(r'## --------------- Relationship ---------------\n(Relationship): (.*?)\n', out.decode('UTF-8'))
    cov_1 = re.findall(r'(TotalFiles): (.*)\n(DeclaredLicenseFiles): (.*)\n(PercentTotalLicenseCoverage): (.*)\n', out.decode('UTF-8'))
    return (doc_1, cre_1, pac_1, pac_lif_1, pac_2, fil_dat_1, fil_rel_1, bas_rel_1, cov_1)

def scan(dbname, user, password, host, port, dsfile, ipath):
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
            if records and records[0][0] != None:
                (doc_1, cre_1, pac_1, pac_lif_1, pac_2, fil_dat_1, fil_rel_1, bas_rel_1, cov_1) = grabreg(records, repo_id, dsfile)
                parse_json(doc_1, cre_1, pac_1, pac_lif_1, pac_2, fil_dat_1, fil_rel_1, bas_rel_1, cov_1, cur, repo_id)
                connection.commit()
            else:
                print("ERROR: RECORD DOES NOT EXIST IN MAPPING TABLE")
        else:
            print("DUPLICATE RECORD FOUND. SKIPPING")
    return
