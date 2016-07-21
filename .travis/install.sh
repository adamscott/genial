#!/usr/bin/env bash
set -ex

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # Install some custom requirements on OS X
    export QMAKE=/usr/local/Cellar/qt5/5.6.1-1/bin/qmake
    eval "$(pyenv init -)"
    pyenv install 3.5.2
    pyenv global 3.5.2

else
    # Install some custom requirements on Linux
    case "${TOXENV}" in
        py34-32-pyqt5 | py35-32-pyqt5)
            sudo dpkg --add-architecture i386
            sudo apt-get -qq update
            case "${TOXENV}" in
                py34-32-pyqt5)
                    sudo apt-get install -y python3.4:i386
                    ;;
                py35-32-pyqt5)
                    sudo apt-get install -y python3.5:i386
                    ;;
            esac
            ;;
        py34-64-pyqt5 | py35-64-pyqt5)
            pip install --upgrade pip
            pip install tox
            ;;
    esac
fi

sudo pip install --upgrade pip
sudo pip install tox

wget http://sourceforge.net/projects/pyqt/files/sip/sip-4.18/sip-4.18.tar.gz
tar -zxf sip-4.18.tar.gz
pushd sip-4.18 && python configure.py && make && sudo make install && popd
wget http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.6/PyQt5_gpl-5.6.tar.gz
tar -zxf PyQt5_gpl-5.6.tar.gz
pushd PyQt5_gpl-5.6 && python configure.py --qmake $QMAKE && make && sudo make install && popd
