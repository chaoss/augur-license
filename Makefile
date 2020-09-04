default:install-spdx

install-spdx:
	@ ./scripts/install/install-spdx-sudo.sh
	@ ./scripts/install/install-nomos.sh

create:
	dosocs2 newconfig
	dosocs2 dbinit
