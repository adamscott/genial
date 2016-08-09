#!/usr/bin/env bash
set -ex

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # Install some custom requirements on OS X
    export QMAKE=/usr/local/Cellar/qt5/5.6.1-1/bin/qmake
    eval "$(pyenv init -)"
    pyenv install 3.5.2
    pyenv global 3.5.2
    pyenv versions

else
    # Install some custom requirements on Linux
    source /opt/qt56/bin/qt56-env.sh
    eval "$(pyenv init -)"
    case "${TOXENV}" in
        py35-32-pyqt5)
            export CONFIGURE_OPTS="--with-arch=i386"
            export CFLAGS="-arch i386"
            export LDFLAGS="-arch i386"
            ;;
        py35-64-pyqt5)
            echo "" > /dev/null
            ;;
    esac
    pyenv install 3.5.2
    pyenv global 3.5.2
    pyenv versions
fi

sudo pip install --upgrade pip
sudo pip install tox

pushd ~
SIP_DIR="sip-4.18"
if [ ! -d "${SIP_DIR}" ]; then
    CACHED_SIP=false
    wget http://sourceforge.net/projects/pyqt/files/sip/sip-4.18/sip-4.18.tar.gz
    sleep 1
    tar -zxf sip-4.18.tar.gz
    sleep 1
    mv sip-4.18 sip
    sleep 1
else
    CACHED_SIP=true
fi
pushd sip
ls -l
if [ ! "${CACHED_SIP}" = true ]; then
    python configure.py
    make -j3
fi
make install -j3
popd # sip
popd # ~

pushd ~
PYQT5_DIR="PyQt5_gpl-5.6"
if [ ! -d "${PYQT5_DIR}" ]; then
    CACHED_PYQT5=false
    wget http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.6/PyQt5_gpl-5.6.tar.gz
    sleep 1
    tar -zxf PyQt5_gpl-5.6.tar.gz
    sleep 1
    mv PyQt5_gpl-5.6 PyQt5_gpl
    sleep 1
else
    CACHED_PYQT5=true
fi
pushd PyQt5_gpl
if [ ! "${CACHED_PYQT5}" = true ]; then
    python configure.py --qmake $QMAKE --confirm-license
    make -j3
fi
make install -j3
popd # PyQt5
popd # ~
