#!/bin/bash

bash stop.bash
git stash
git pull
bash run.bash
