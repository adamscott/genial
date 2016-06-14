#!/usr/bin/env bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    # Install some custom requirements on OS X

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
            curl -O http://sourceforge.net/projects/pyqt/files/sip/sip-4.18/sip-4.18.tar.gz
            tar zxvf sip-4.18.tar.gz
            curl -O http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.6/PyQt5_gpl-5.6.tar.gz
            tar zxvf PyQt5_gpl-5.6.tar.gz
            ;;
        py34-64-pyqt5 | py35-32-pyqt5)
            # Do not need to install python, it's already installed.
            ;;
    esac
fi

# Install tox for every target
sudo pip install --upgrade pip
sudo pip install virtualenv
sudo pip install virtualenvwrapper
mkdir ~/.virtualenvs/genial/
source /urs/local/bin/virtualenvwrapper.sh
mkvirtualenv work_env
workon work_env
pip install tox
