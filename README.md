Augur-SPDX
=======

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


License and Copyright
---------------------

Copyright © 2015 University of Nebraska at Omaha

Augur-SPDX is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 2 of the License, or (at your option) any later
version. See the file LICENSE for more details.

All associated documentation is licensed under the terms of the Creative
Commons Attribution Share-Alike 3.0 license. See the file CC-BY-SA-3.0 for more
details.


Dependencies
------------

- Python 3.6

Optional:
- PostgreSQL 8.x or later version (can be on a separate machine)

Python libraries:
- All Python dependencies are handled automatically by `pip`.


Installation
------------

### Step 1 - Download and install

Augur-SPDX is most easily installed under the CHAOSS Project Augur

To install tha latest `master` version of Augur-SPDX, use the Makefile in Augur:

    $ make install-spdx

#### Alternate Install

You can also Install augur-spdx manually.

We recommend doing this inside a Python
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), but it
is not a requirement.

This installation can be achieved through the Makefile in the augur-sbom directory.

    $ sudo make install

If you have any problems installing Nomos, run the install script individually:

    $ ./DoSOCSv2-0.x.x/scripts/install-nomos.sh

Usage: Command Line Tool
-----

The simplest use case is scanning a package, generating a
document, and printing an SPDX document in one shot:

    $ dosocs2 oneshot package.tar.gz
    dosocs2: package.tar.gz: package_id: 1
    dosocs2: running nomos on package 1
    dosocs2: package.tar.gz: document_id: 1
    [... document output here ...]

Also works on directories:

    $ dosocs2 oneshot ./path/to/directory

The scan results and other collected metadata are saved in the database
so that subsequent document generations will be much faster.

To just scan a package and store its information in the database:

    $ dosocs2 scan package.tar.gz
    dosocs2: package_tar_gz: package_id: 456
    dosocs2: running nomos on package 456

In the default configuration, if a scanner is not specified, only `nomos`
is run by default. It gathers license information, but is a bit slow.
One can use the `-s` option to explicitly specify which scanners to run:

    $ dosocs2 scan -s nomos_deep,dummy package.tar.gz
    dosocs2: package_tar_gz: package_id: 456
    dosocs2: running nomos_deep on package 456
    dosocs2: running dummy on package 456

After `dosocs2 scan`, no SPDX document has yet been created.
To create one in the database (specifying the package ID):

    $ dosocs2 generate 456
    dosocs2: (package_id 456): document_id: 123

Then, to compile and output the document in tag-value format:

    $ dosocs2 print 123
    [... document output here ...]

Use `dosocs2 --help` to get the full help text. The `doc` directory
here also provides more detailed information about how `dosocs2` works
and how to use it.

Usage: Augur Worker
-----

NOTE: This method is experimental <br />
NOTE: Make sure you are using Python3 with a virtualenv

Augur Includes many extra tools that help automate the work of Augur-SPDX.<br />
Right now, the best way to run augur-SPDX is to use Augur's extra built-in tools.<br />
Augur-SPDX will work with some files in augur and take some steps in order.

Here is the process that Augur-SPDX uses:

1. Find all repositories in the Augur database<br />
2. Scan each stored repository with the Augur-SPDX command-line tool<br />
3. Generate SPDX Documents for each scanned repository

The scanned repositories and SPDX documents will provide data to augur, namely on the risk page under any repo scanned.

Here are the steps to get it up and running:

1. Switch to the Augur-SPDX branch of Augur:
    ```
    git checkout dev-spdx-scanner
    ```

2. Run the `make` installation for Augur-SPDX under Augur's Makefile:
    ```
    make install-spdx
    ```
    
3. Ensure your augur configuration is pointing to the database you want to access and scan
    ```
    nano augur.config.json
    ```
    
4. Navigate to the folder with the Augur-SPDX executable

    ```
    cd /augur/workers/spdx_worker/
    ```
    
5. run the file `director.py`

    ```
    python3 director.py
    ```
    
The Director will provide information of what it is doing. <br />
It will scan the repositories in the Augur database, then generate SPDX documents.

Each repository can take anywhere from 10 seconds to 1 hour to scan, and SPDX Documents are usually quicker.<br />

This method is experimental!<br />
Please report any bugs to 
[Matt Snell](https://github.com/nebrethar) at <msnell@unomaha.edu>

History
-------
Augur-SPDX owes its software name and concept to the
[DoSOCS](https://github.com/socs-dev-env/DoSOCS) tool created by Zac
McFarland, which in turn was spun off from the [do_spdx](https://github.com/ttgurney/yocto-spdx/blob/master/src/spdx.bbclass) plugin for Yocto
Project, created by Jake Cloyd and Liang Cao.
Augur-SPDX aims to fill the same role as DoSOCS, but with support for future versions of Augur, a
larger feature set, and a more modular implementation.


Maintainers
-----------

[Matt Snell](https://github.com/nebrethar)
[Sean Goggins](https://github.com/sgoggins)


(This work has been funded through the National Science Foundation VOSS-IOS Grant: 1122642.)
