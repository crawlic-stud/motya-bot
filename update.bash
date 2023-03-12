#!/bin/bash

bash stop.bash
sleep(1)
git stash
git pull
bash run.bash
