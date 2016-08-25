#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then
    # Install some custom requirements on OS X
    brew update

    pushd /tmp
    wget https://download.qt.io/official_releases/qt/5.7/5.7.0/single/qt-everywhere-opensource-src-5.7.0.tar.gz
    gunzip qt-everywhere-opensource-src-5.7.0.tar.gz
    tar xvf qt-everywhere-opensource-src-5.7.0.tar
    pushd qt-everywhere-opensource-src-5.7.0
    QT_BASE_DIR=/opt/qt57
    sudo mkdir -p "$QT_BASE_DIR"
    ./configure -opensource -confirm-license -release \
        -prefix "$QT_BASE_DIR" \
        -nomake docs -nomake examples -nomake demos -nomake tests \
        -skip activeqt -skip qt3d -skip enginio -skip qtandroidextras \
        -skip qtbluetooth -skip qtcanvas3d -skip qtconcurrent \
        -skip qtdbus -skip qtgraphicaleffects -skip qtimageformats \
        -skip qtlocation -skip qtmacextras -skip qtnfc -skip qtopengl \
        -skip qtplatformheaders -skip qtpositioning -skip qtprintsupport \
        -skip qtpurchasing -skip qtquickcontrols2 -skip qtquickextras \
        -skip qtquickwidgets -skip qtscript -skip qtscripttools \
        -skip qtsensors -skip qtserialport -skip qtsvg -skip qtwebchannel \
        -skip qtwebengine -skip qtwebsockets -skip qtwebview \
        -skip qtwindowsextras -skip qtx11extras -skip qtxml \
        -skip qtxmlpatterns -skip qtcharts -skip qtdatavisualization \
        -skip qtvirtualkeyboard -skip qtquick2drenderer
    make -j3
    sudo make -j3 install
    export PATH=$QT_BASE_DIR/bin:$PATH
    popd # /tmp/qt-everywhere-opensource-src-5.7.0
    popd # /tmp

    brew install pandoc
    brew upgrade pyenv
else
    # Install some custom requirements on Linux
    if [[ "${TOXENV}" == 'py35-32-pyqt5' ]]; then
        # Adds i386 packages
        echo "foreign-architecture i386" | sudo tee --append /etc/dpkg/dpkg.cfg.d/architectures > /dev/null
    fi
    sudo apt-add-repository ppa:beineri/opt-qt57-trusty -y
    sudo apt-get update
    case "${TOXENV}" in
        py35-32-pyqt5)
            sudo apt-get install qt57-meta-full:i386
            ;;
        py35-64-pyqt5)
            sudo apt-get install qt57-meta-full
            ;;
    esac
    # Disable temporarily exit on error
    set +e
    source ~/build/adamscott/genial/.travis/qt5-env.sh
    # Reenable exit on error
    set -e
    # Install pyenv
    wget -qO- https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
    export PATH="/home/travis/.pyenv/bin:$PATH"
fi
