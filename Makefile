default:install-spdx

install-spdx:
	@ ./scripts/install/install-spdx-sudo.sh
	@ ./scripts/install/install-nomos.sh
install-augur: 
	sudo apt-get install libpq-dev && sudo apt-get install libglib2.0-dev libjsoncpp-dev libjson-c-dev
	pip3 install .
	./scripts/install-nomos.sh

install:
	sudo apt-get install git python3-pip postgresql && sudo apt-get install libpq-dev && sudo apt-get install libglib2.0-dev libjsoncpp-dev libjson-c-dev
	pip3 install .
	./scripts/install-nomos.sh

create:
	dosocs2 newconfig
	dosocs2 dbinit
