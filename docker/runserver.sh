#!/bin/bash

set -e

nohup django.sh
nohup beat.sh
nohup worker.sh
