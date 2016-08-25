#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then
    # Install some custom requirements on OS X
    export QMAKE=/usr/local/Cellar/qt5/5.6.1-1/bin/qmake
    # Initialize pyenv
    eval "$(pyenv init -)"
    pyenv install 3.5.2
    pyenv global 3.5.2
    pyenv versions

else
    # Install some custom requirements on Linux
    # Disable temporarily exit on error
    set +e
    source ~/build/adamscott/genial/.travis/qt56-env.sh
    # Reenable exit on error
    set -e
    # Initialize pyenv
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
sudo pip install -r setup_requirements.txt
