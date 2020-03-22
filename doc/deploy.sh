#!/usr/bin/env bash

make
cp -r out/* repo/
cd repo/
git add -A .
git commit -m "Deploy: $(date)"
git push
