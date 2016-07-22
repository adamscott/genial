#!/usr/bin/env bash
set -ex

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # Install some custom requirements on OS X
    brew update
    brew install qt5
    brew install pandoc
    brew upgrade pyenv
else
    # Install some custom requirements on Linux
    sudo apt-add-repository ppa:beineri/opt-qt561 -y
    sudo apt-get update
    case "${TOXENV}" in
        py35-32-pyqt5)
            sudo apt-get install qt-latest:i386
            ;;
        py35-64-pyqt5)
            sudo apt-get install qt-latest
            ;;
    esac
    source /opt/qt56/bin/qt56-env.sh
fi
