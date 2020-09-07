#!/bin/bash
REPO=$(mktemp -d)
echo $REPO
echo "[$0] git clone https://github.com/fossology/fossology $REPO"
git clone https://github.com/fossology/fossology $REPO || exit 1
sed -i -e 's/-lfossology //g' $REPO/Makefile.conf || exit 1
sed -i -e 's/-lfossologyCPP //g' $REPO/Makefile.conf || exit 1
pushd $REPO/src/nomos/agent || exit 1
yes | mv Makefile.sa Makefile || exit 1
echo "[$0] make"
make || exit 1
echo "[$0] sudo make install"
sudo make install || exit 1
popd || exit 1
echo "[$0] rm -rf $REPO"
rm -rf $REPO
echo "[$0] sudo ln -s /usr/local/share/fossology/nomos/agent/nomossa $NOMOSSA_PATH"
sudo ln -s /usr/local/share/fossology/nomos/agent/nomossa /usr/local/bin/nomossa || exit 1
echo "[$0] done!"
