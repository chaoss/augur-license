# Augur-SPDX 

Dependencies
------------

- Python 3.6 or later version
- PostgreSQL 8.x or later version (can be on a separate machine)
- Installed instance of [Augur](https://github.com/chaoss/augur) that has had the `facade worker` run at least one time. Without this step there will be no cloned repos to scan. 

Python libraries:
- All Python dependencies are handled automatically by `pip` during installation.

**Augur-SPDX runs as a process to populate the `SPDX` schema with SPDX license information in [Augur](https://github.com/chaoss/augur). Available [Fossology](https://www.fossology.org/) license scanners only compile on Ubuntu's current long term maintenance version due to library dependencies. Believe us, we have spent many hours trying to compile on Mac OSX and Fedora. In the future, we will provide a docker container to enable this functionality across platforms**

Installation
------------

### Step 1 - Download and install
1. `git clone https://github.com/chaoss/augur-spdx`
2. `sudo make install-spdx` **It is necessary to compile using sudo because the license scanners provided by [Fossology](https://www.fossology.org/) are designed only to be installed at the system level**
3. `pip install .`
4. **temporary** Edit the `spdx.config.json` file so that the path points to the location of your [Augur](https://github.com/chaoss/augur) cloned repositories. This can be found in the `augur.config.json` file for the instance you wish to scan licenses for. 

### Step 2 - Run Augur-SPDX **NOTE: You can only run one instance of Augur-SPDX at at time**
1. `nohup python3 director.py <path to augur instance root> >spdx.log 2>spdx.err &` Usually, this is something like `nohup python3 director.py ../augur-chaoss >spdx.log 2>spdx.err &`
2. Wait about 30 seconds to make sure there is not an error that terminates the process. 
3. `tail -30 spdx.log` - Check that licenses are being scanned
4. `cat spdx.err` - Check that there are not a lot of errors. 
5. When the process finishes, check to see if there are any Augur repos not in the mapping table by executing `cat spdx.log | grep MAPPING` . If you see any rows, create an issue with the full output of the log at https://github.com/chaoss/augur-spdx 

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

[Matt Snell](https://github.com/nebrethar)
[Sean Goggins](https://github.com/sgoggins)

# License and Copyright
---------------------

Copyright © 2015 University of Nebraska at Omaha

Copyright © 2020 University of Nebraska at Omaha, and University of Missouri

Augur-SPDX is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 2 of the License, or (at your option) any later
version. See the file LICENSE for more details.

All associated documentation is licensed under the terms of the Creative
Commons Attribution Share-Alike 3.0 license. See the file CC-BY-SA-3.0 for more
details.

(This work has been funded through the National Science Foundation VOSS-IOS Grant: 1122642, the Sloan Foundation, and the Reynolds Journalism Institute at the University of Missouri.)
