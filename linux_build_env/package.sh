#!/usr/bin/env bash 

full_path=$(realpath $0)
dir_path=$(dirname $full_path)
cd $dir_path

cd $dir_path/../
pip3 install wheel
pip3 install -r requirements.txt pyinstaller
pyinstaller crawl.py --onefile

rm -rf build crawl.spec
chmod -R 777 dist
