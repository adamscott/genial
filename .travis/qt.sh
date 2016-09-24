#!/usr/bin/env bash
set -ex

QT_BASE_DIR=/opt/qt57

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then # OSX
    # install gist package
    brew install gist

    # write gist token to ~/.gist
    pushd ~
    python -c """with open('.gist', 'w') as f: f.write('${GITHUB_GIST_TOKEN}')"""
    popd # ~

    pushd /tmp
    wget https://download.qt.io/official_releases/qt/5.7/5.7.0/single/qt-everywhere-opensource-src-5.7.0.tar.gz
    gunzip qt-everywhere-opensource-src-5.7.0.tar.gz
    tar xf qt-everywhere-opensource-src-5.7.0.tar
    pushd qt-everywhere-opensource-src-5.7.0
    sudo mkdir -p "$QT_BASE_DIR"

    ./configure \
        $(: === MISC ===)\
        -opensource \
        -confirm-license \
        -release \
        -prefix "${QT_BASE_DIR}" \
        $(: === NO MAKE ===)\
        -nomake libs \
        -nomake examples \
        -nomake tests \
        $(: === SKIP ===)\
        -skip qt3d \
        -skip activeqt \
        -skip qtandroidextras \
        -skip qtcanvas3d \
        -skip qtcharts \
        -skip qtconnectivity \
        -skip qtdatavis3d \
        -skip qtdeclarative \
        -skip qtdoc \
        -skip qtgamepad \
        -skip qtgraphicaleffects \
        -skip qtimageformats \
        -skip qtlocation \
        -skip qtmacextras \
        -skip qtmultimedia \
        -skip qtpurchasing \
        -skip qtquickcontrols \
        -skip qtquickcontrols2 \
        -skip qtscript \
        -skip qtscxml \
        -skip qtsensors \
        -skip qtserialbus \
        -skip qtserialport \
        -skip qtsvg \
        $(: -skip qttranslations) \
        -skip qtvirtualkeyboard \
        -skip qtwayland \
        -skip qtwebchannel \
        -skip qtwebengine \
        -skip qtwebsockets \
        -skip qtwebview \
        -skip qtwinextras \
        -skip qtx11extras \
        -skip qtxmlpatterns

    set +e # Disable temporarily exit on error
    LOG_FILE_NAME="genial-travis-qt5.7-1_make.log"
    build_wait make -j3 &> genial-travis-qt5.7-1_make.log
    sudo make -j3 install &> genial-travis-qt5.7-2_make_install.log
    gist \
        -u b1f0f29a43cc76a36c8f5fdc10528a25 \
        genial-travis-qt5.7-1_make.log \
        genial-travis-qt5.7-2_make_install.log
    set -e # Reenable exit on error

    export PATH=$QT_BASE_DIR/bin:$PATH
    popd # /tmp/qt-everywhere-opensource-src-5.7.0
    popd # /tmp

else # Linux
    sudo apt-add-repository ppa:beineri/opt-qt57-trusty -y
    sudo apt-get update
    sudo apt-get install qt57-meta-full
fi

export QTDIR=$QT_BASE_DIR
export PATH=$QT_BASE_DIR/bin:$PATH
export QMAKE=$QT_BASE_DIR/bin/qmake
