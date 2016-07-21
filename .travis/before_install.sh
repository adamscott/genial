#!/usr/bin/env bash
set -ex

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # Install some custom requirements on OS X
    brew update
    brew install qt5
    brew install pandoc
else
    # Install some custom requirements on Linux
    case "${TOXENV}" in
        py35-32-pyqt5)
            export CONFIGURE_OPTS="--with-arch=i386"
            export CFLAGS="-arch i386"
            export LDFLAGS="-arch i386"
            ;;
        py35-64-pyqt5)

            ;;
    esac
fi