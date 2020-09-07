# augur_sbom_scanner
Goal: This will be a worker. For now, it runs augur-sbom, which is installed separately. 

REMEMBER: Be in your virtual environment. 


## To Run to Gather License Information: 
1. Install `augur-spdx` : `git clone https://github.com/chaoss/augur-spdx.git`
2. `make install` 
2. Run `dosocs2 newconfig`
3. Replace contents with augur configuration: 
```
connection_uri = postgresql://user:pasword@host:port/database

schema = spdx

default_scanners = nomos

echo = False

scanner_nomos_path = /usr/local/share/fossology/nomos/agent/nomossa
```
4. Run `python director.py`

## Pre-Requisites
### Mac OSX
`brew install cmake autoconf automake libtool pkg-config glib libzip libusb python3 qt5 boost check fftw json-c`

qt is keg-only, which means it was not symlinked into /usr/local,
because Qt 5 has CMake issues when linked.

If you need to have qt first in your PATH run:
  echo 'export PATH="/usr/local/opt/qt/bin:$PATH"' >> ~/.zshrc

For compilers to find qt you may need to set:
  export LDFLAGS="-L/usr/local/opt/qt/lib"
  export CPPFLAGS="-I/usr/local/opt/qt/include"

For pkg-config to find qt you may need to set:
  export PKG_CONFIG_PATH="/usr/local/opt/qt/lib/pkgconfig"

5. Edit the augur_sbom_config.json with db credentials (Yes, redundent).
6. 
