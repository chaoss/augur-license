# augur-spdx TODO
1. DOSOCS2: Have the database config refer to the `augur.config.json` so that multiple different augur instances can use the same installation of augur-spdx. Another way of saying this is that we want `~/.config/dosocs2/dosocs2.conf` to go away, and we want `augur-spdx` to read values from the `augur.config.json` for the directory it is in. 
2. Have the spdx-scanner directory refer to the augur.config.json for database credentials AND facade repo path.
3. Welcome 
