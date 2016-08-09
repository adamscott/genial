#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then
    # Install some custom requirements on OS X
    brew update
    brew install qt5
    brew install pandoc
    brew upgrade pyenv
else
    # Install some custom requirements on Linux
    if [[ "${TOXENV}" == 'py35-32-pyqt5' ]]; then
        echo "foreign-architecture i386" >> /etc/dpkg/dpkg.cfg.d/architectures
    fi
    sudo apt-add-repository ppa:beineri/opt-qt561 -y
    sudo apt-get update
    case "${TOXENV}" in
        py35-32-pyqt5)
            sudo apt-get install qt56-meta-full:i386
            ;;
        py35-64-pyqt5)
            sudo apt-get install qt56-meta-full
            ;;
    esac
    # Disable temporarily exit on error
    set +e
    source ~/build/adamscott/genial/.travis/qt56-env.sh
    # Reenable exit on error
    set -e
fi
