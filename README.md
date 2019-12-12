Augur-SPDX
=======

Augur-SPDX is a command-line tool for managing SPDX 2.0 documents and data. It can
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
information. Augur-SPDX supports the SPDX 2.0 standard, released in May 2015.


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

    $ Augur make-SPDX

## Alternate Install

You can also Install augur-spdx manually.

We recommend doing this inside a Python
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), but it
is not a requirement.

This installation can be achieved through the Makefile in the augur-sbom directory.

    $ sudo make install

If you have any problems installing Nomos, run the install script individually:

    $ ./DoSOCSv2-0.x.x/scripts/install-nomos.sh

Usage
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

Potential Organizational Use of augur-SPDX
---------------------------------------

![alt text](https://cloud.githubusercontent.com/assets/656208/20320341/30b9468c-ab37-11e6-8e3f-c63543b85453.png)

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


(This work has been funded through the National Science Foundation VOSS-IOS Grant: 1122642.)
