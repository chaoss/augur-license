import subprocess
import psycopg2
from subprocess import PIPE
import json
import re
import os

#class DoSOCSv2(object):
    #"""Uses the DoSOCSv2 database to return dataframes with interesting GitHub indicators"""

def scan(repo_name):
    connection = psycopg2.connect(
        user = "augur",
        password = "mcguire18",
        database = "augur",
        host = "localhost",
        port = 5433,
    )
    cur = connection.cursor()
    cur.execute("SET search_path to spdx;")

    print("hold on...")
    cur.execute("SELECT dosocs_pkg_id FROM augur_repo_map WHERE dosocs_pkg_name = "+ chr(39) + repo_name + chr(39) + ";")
    records = cur.fetchall()
    print("Package_id: " + str(records[0][0]))
    proc = subprocess.Popen("dosocs2 generate " + str(records[0][0]), shell=True, stdout=PIPE, stderr=PIPE)
    varerr = str(str(proc.stderr.read()).split(" ")[3])
    charvarerr = varerr.split("\\")[0]
    print(proc.stderr.read())
    print(varerr)
    print(charvarerr)
    print("Document_id: " + str(charvarerr))
    f = open("/home/sean/dosocs2/accessDB/scans-tv/" + repo_name + ".txt","w")
    proc = subprocess.call("dosocs2 print " + str(charvarerr) + " -T 2.0.tag.coverage", shell=True, stdout=f, stderr=f)
    pope = subprocess.Popen("dosocs2 print " + str(charvarerr) + " -T 2.0.tag.coverage", shell=True, stdout=PIPE, stderr=PIPE)
    out, err = pope.communicate()
    #if out:
        #print(out)
    if err:
        print(err.decode('UTF-8'))
    #print (out)
    package_sx_1 = re.findall(r'(SPDXVersion): (.*)\n(DataLicense): (.*)\n(DocumentNamespace): (.*)\n(DocumentName): (.*)\n(SPDXID): (.*)\n(DocumentComment): (.*)\n', out.decode('UTF-8'))
    package_sr_1 = re.findall(r'(PackageName): (.*)\n(SPDXID): (.*)\n(PackageVersion|)? ?(.*|)\n?(PackageFileName): (.*)\n(PackageSupplier): (.*)\n(PackageOriginator): (.*)\n(PackageDownloadLocation): (.*)\n(PackageVerificationCode):? ?(.*|)\n?(PackageHomePage): (.*)\n(PackageLicenseConcluded):', out.decode('UTF-8'))
    package_sr_2 = re.findall(r'(PackageLicenseInfoFromFiles): (.*)\n?', out.decode('UTF-8'))
    package_sr_3 = re.findall(r'(PackageLicenseDeclared): (.*)\n(PackageLicenseComments): (.*)\n(PackageCopyrightText): (.*)\n(PackageSummary): (.*)\n(PackageDescription): (.*)\n(PackageComment): (.*|)', out.decode('UTF-8'))
    package_cr_1 = re.findall(r'(Creator): (.*)\n(Created): (.*)\n(CreatorComment): (.*)\n(LicenseListVersion): (.*)\n', out.decode('UTF-8'))
    package_li_1 = re.findall(r'(LicenseID): (.*)\n(LicenseName): (.*)\n(ExtractedText): (.*)\n(LicenseCrossReference): (.*)\n(LicenseComment): (.*)\n', out.decode('UTF-8'))
    package_ff_1 = re.findall(r'(FileName): (.*)\n(SPDXID): (.*)\n(FileType): (.*)\n(FileChecksum): (.*)\n(LicenseConcluded): (.*)\n(LicenseInfoInFile): (.*)\n(LicenseComments): (.*)\n(FileCopyrightText): (.*)\n(FileComment): (.*)\n(FileNotice): (.*)\n', out.decode('UTF-8'))
    package_lc_1 = re.findall(r'(TotalFiles): (.*)\n(DeclaredLicenseFiles): (.*)\n(PercentTotalLicenseCoverage): (.*)\n', out.decode('UTF-8'))
    def concat():
        return (package_sx_1, package_sr_1, package_sr_2, package_sr_3, package_cr_1, package_li_1, package_ff_1, package_lc_1)
    #scan_results = [('LicenseID', 'LicenseRef-Python', 'LicenseName', 'Python', 'ExtractedText', 'licenses/CNRI-Python.html",\\n        "is_spdx_official": true,\\n        "name": "CNRI Python License', 'LicenseCrossReference', '', 'LicenseComment', 'found by nomos\n'), ('LicenseID', 'LicenseRef-IJG-possibility', 'LicenseName', 'IJG-possibility', 'ExtractedText', 'Independent JPEG Group', 'LicenseCrossReference', '', 'LicenseComment', 'found by nomos\n'), ('LicenseID', 'LicenseRef-Classpath-exception-2.0', 'LicenseName', 'Classpath-exception-2.0', 'ExtractedText', 'Classpath exception', 'LicenseCrossReference', '', 'LicenseComment', 'found by nomos\n')]
    return concat()

def retrieve_license_information(repo_name):
    package_sx_1, package_sr_1, package_sr_2, package_sr_3, package_cr_1, package_li_1, package_ff_1, package_lc_1 = scan(repo_name)

    #Print all returned expression
    #print()
    #print(package_sx_1)
    #print()
    #print(package_sr_1)
    #print()
    #print(package_sr_2)
    #print()
    #print(package_sr_3)
    #print()
    #print(package_cr_1)
    #print()
    #print(package_li_1)
    #print()
    #Big Print
    #print(package_ff_1)
    #print()

    license_information = {}

    temp_1 = {}
    for i in range(0, int(len(package_lc_1[0])/2)):
        j = i*2
        temp_1[package_lc_1[0][j]] = package_lc_1[0][j+1]

    coverage_temp = {**temp_1}

    temp_1 = {}
    for i in range(0, int(len(package_sx_1[0])/2)):
        j = i*2
        temp_1[package_sx_1[0][j]] = package_sx_1[0][j+1]

    spdx_temp = {**temp_1}

    temp_1 = {}
    for i in range(0, int(len(package_sr_1[0])/2)):
        j = i*2
        if package_sr_1[0][j] != '':
            temp_1[package_sr_1[0][j]] = package_sr_1[0][j+1]
    temp_2 = {}
    i = 0
    for i in range(0, len(package_sr_2[0])):
        temp_2["License #" + str(i)] = package_sr_2[i][1]
        i += 1
    temp_3 = {}
    for i in range(0, int(len(package_sr_3[0])/2)):
        j = i*2
        temp_3[package_sr_3[0][j]] = package_sr_3[0][j+1]

    package_temp = {**temp_1, **temp_2, **temp_3}

    temp_1 = {}
    for i in range(0, int(len(package_cr_1[0])/2)):
        j = i*2
        temp_1[package_cr_1[0][j]] = package_cr_1[0][j+1]

    creation_temp = {**temp_1}

    temp_1 = {}
    for i in range(0, int(len(package_li_1[0])/2)):
        j = i*2
        temp_1[package_li_1[0][j]] = package_li_1[0][j+1]

    license_temp = {**temp_1}

    temp_2 = {}
    for g in range(0, int(len(package_ff_1))):
        temp_1 = {}
        for i in range(0, int(len(package_ff_1[g])/2)):
            j = i*2
            temp_1[package_ff_1[g][j]] = package_ff_1[g][j+1]
        temp_2["File Data " + str(g)] = temp_1

    fileby_temp = {**temp_2}

    license_information['Coverage'] = coverage_temp
    license_information['SPDX Data'] = spdx_temp
    license_information['Package'] = package_temp
    license_information['Creation'] = creation_temp
    license_information['Licenses'] = license_temp
    license_information['File-by-File'] = fileby_temp

    with open("/home/sean/dosocs2/accessDB/scans-json/" + repo_name + ".json","w") as g:
            json.dump(license_information, g)
    return json.dumps(license_information)

if __name__ == "__main__":
    repo_name = input("Enter REPO name: ")
    retrieve_license_information(repo_name)
