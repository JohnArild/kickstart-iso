#!/usr/bin/bash

mkdir output || exit 1
cp -rv /opt/Rocky-9-5/BaseOS/* output || exit 1
mv $(find output/Packages -type f) output/Packages || exit 1
rmdir $(find output/Packages/* -type d) || exit 1
cp $(find output/repodata -name "*GROUPS.xml") output/GROUPS.xml || exit 1
python3 ks-download.py || exit 1
createrepo_c -g GROUPS.xml output || exit 1
