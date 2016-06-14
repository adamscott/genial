#!/usr/bin/env bash
set -ex

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # Install some custom requirements on OS X
    brew update
    brew install qt5
    brew install pandoc
else
    # Install some custom requirements on Linux
    sudo add-apt-repository --yes ppa:ubuntu-sdk-team/ppa
    sudo apt-get update
    sudo apt-get install -y qt5-default
    sudo apt-get install -y qt5-qmake
    case "${TOXENV}" in
        py34-32-pyqt5 | py35-32-pyqt5)
            sudo apt-get install -y pandoc
            export QMAKE=/usr/lib/i686-linux-gnu/qt5/bin/qmake
            ;;
        py34-64-pyqt5 | py35-64-pyqt5)
            # Pandoc is handled by Travis
            export QMAKE=/usr/lib/x86_64-linux-gnu/qt5/bin/qmake
            ;;
    esac
fi