# Augur-SPDX 

Dependencies
------------

- Python 3.6 or later version
- PostgreSQL 8.x or later version (can be on a separate machine)
- Installed instance of [Augur](https://github.com/chaoss/augur) that has had the `facade worker` run at least one time. Without this step there will be no cloned repos to scan. 
- Necessary libraries for compilation of python source: 
```
  sudo apt install gcc
  sudo apt install python3-dev
  sudo apt-get install libpq-dev
```

Python libraries:
- All Python dependencies are handled automatically by `pip` during installation.

**Augur-SPDX runs as a process to populate the `SPDX` schema with SPDX license information in [Augur](https://github.com/chaoss/augur). Available [Fossology](https://www.fossology.org/) license scanners only compile on Ubuntu's current long term maintenance version due to library dependencies. Believe us, we have spent many hours trying to compile on Mac OSX and Fedora. In the future, we will provide a docker container to enable this functionality across platforms**

Installation
------------

### Step 1 - Download and install
1. `git clone https://github.com/chaoss/augur-spdx`
2. Create a python3 virtual enviornment `virtualenv --python=python3 venv-name`
3. Activate Python virtual environment `source venv-name/bin/activate`
4. `pip install .`
5. `sudo make install-spdx` 
Note: It is necessary to compile using sudo because the license scanners provided by [Fossology](https://www.fossology.org/) are designed only to be installed at the system level

### Step 2 - Install System Level libmagic
1. `sudo apt install libmagic1`

**This is necessary for the scanners**

### Step 3 - Initialize the Database Schema (spdx) <br/>
NOTE: You can also use these steps to reinitialize or update a database
1. `python3 initial.py <path to augur instance root>` <br> Example: `python3 initial.py ../augur-chaoss`
2. After this, run `dosocs2 dbinit --config dosocs2.conf` in the augur-spdx directory
3. The program will prompt you to ensure that you have the right database. Please double check
4. Any existing tables that fit the schema will be dropped, and a new set of tables will be created and populated.

### Step 3 - Run Augur-SPDX <br/>
NOTE: You can only run one instance of Augur-SPDX at at time
1. `nohup python3 director.py <path to augur instance root> >spdx.log 2>spdx.err &` <br> Example: `nohup python3 director.py ../augur-chaoss >spdx.log 2>spdx.err &`
2. Wait about 30 seconds to allow the program to run. 
3. `tail -30 spdx.log` - Check that licenses are being scanned.
4. `cat spdx.err` - Check for errors. 
5. When the process finishes, check to see if there are any Augur repos not in the mapping table by executing `cat spdx.log | grep MAPPING` . 

- If you see any problems, create an issue with the full output of the log at https://github.com/chaoss/augur-spdx 

-----

# Augur-SPDX Description and Purpose

-----

Augur-SPDX is a command-line tool for managing SPDX documents and data. It can
scan source code distributions to produce SPDX information, store that
information in a relational database, and extract it in a plain-text format
on request.

The discovery and presentation of software package license information is a complex
problem facing organizations that rely on open source software within their 
innovation streams. Augur-SPDX enables creation of an SPDX document for any 
software package to represent associated license information. In addition, Augur-SPDX 
can be used in the creation and continuous maintenance of an inventory of all 
open-source software used in an organization. The primary audience for Augur-SPDX is open source
software teams seeking to advance the representation and maintenance of open source 
software package license information. 

[SPDX](http://www.spdx.org) is a standard format for communicating information
about the contents of a software package, including license and copyright
information. Augur-SPDX supports the SPDX standard.

-------

# History

-------

Augur-SPDX owes its software name and concept to the
[DoSOCS](https://github.com/socs-dev-env/DoSOCS) tool created by Zac
McFarland, which in turn was spun off from the [do_spdx](https://github.com/ttgurney/yocto-spdx/blob/master/src/spdx.bbclass) plugin for Yocto
Project, created by Jake Cloyd and Liang Cao.
Augur-SPDX aims to fill the same role as DoSOCS, but with support for future versions of Augur, a
larger feature set, and a more modular implementation.


# Maintainers
-----------

[Matt Snell](https://github.com/nebrethar) <br/>
[Sean Goggins](https://github.com/sgoggins)

# License and Copyright
---------------------

Copyright © 2015 University of Nebraska at Omaha

Copyright © 2022 University of Nebraska at Omaha, and University of Missouri

All associated documentation is licensed under the terms of the Creative
Commons Attribution Share-Alike 3.0 license. See the file CC-BY-SA-3.0 for more
details.

(This work has been funded through the National Science Foundation VOSS-IOS Grant: 1122642, the Sloan Foundation, and the Reynolds Journalism Institute at the University of Missouri.)
