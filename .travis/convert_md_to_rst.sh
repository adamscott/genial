#!/usr/bin/env bash

pandoc -s -S README.md -o README.rst
pandoc -s -S README_fr.md -o README_fr.rst
pandoc -s -S CHANGES.md -o CHANGES.rst