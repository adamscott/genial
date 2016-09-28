#!/usr/bin/env bash
set -e

source helpers.sh

log_verbose "=> Setup doit"
log_verbose "==> Installing doit"
pip install doit
