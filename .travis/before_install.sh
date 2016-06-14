#!/usr/bin/env bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # Install some custom requirements on OS X
    brew update
    brew install qt5
    brew install pandoc
else
    # Install some custom requirements on Linux
    case "${TOXENV}" in
        py34-32-pyqt5 | py35-32-pyqt5)
            sudo apt-get update
            sudo apt-get install qt5-default
            sudo apt-get install qt5-qmake
            sudo apt-get install pandoc
            ;;
        py34-64-pyqt5 | py35-64-pyqt5)
            # Do not need to install anything, the image is already ready.
            ;;
    esac
fi