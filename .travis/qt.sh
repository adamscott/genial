#!/usr/bin/env bash
set -e

source helpers.sh

log_verbose "=> Qt installation"

_tmp=`mktemp -d 2>/dev/null || mktemp -d -t 'qt_tmp_dir'`

mkdir -p "${_tmp}"
mkdir -p QT_INSTALL_DIR

pushd "${_tmp}"
log_verbose "==> Downloading Qt source code"
wget 'https://download.qt.io/official_releases/qt/5.7/5.7.0/single/qt-everywhere-opensource-src-5.7.0.tar.xz'
log_verbose "==> Extracting Qt source code"
tar xf 'qt-everywhere-opensource-src-5.7.0.tar.xz'

pushd qt-everywhere-opensource-src-5.7.0

if [[ "${TRAVIS_OS_NAME}" == 'linux' ]]; then  # Linux
    log_verbose "==> Updating gcc and g++ references to gcc-5 and g++-5"
    echo 'QMAKE_COMPILER = gcc-5' >>qtbase/mkspecs/linux-g++-64/qmake.conf
    echo 'QMAKE_CC = gcc-5' >>qtbase/mkspecs/linux-g++-64/qmake.conf
    echo 'QMAKE_CXX = g++-5' >>qtbase/mkspecs/linux-g++-64/qmake.conf
fi

log_verbose "==> configure"
./configure \
    $(: === MISC ===)\
    -opensource \
    -confirm-license \
    -release \
    -prefix "${QT_INSTALL_DIR}" \
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

_gist_id="b1f0f29a43cc76a36c8f5fdc10528a25"
_make_log="make-${TRAVIS_OS_NAME}.log"
_make_install_log="make_install-${TRAVIS_OS_NAME}.log"
BUILD_WAIT_LOG="${_make_log}"

log_verbose "==> make"
build_wait make -j3

log_verbose "==> make install"
make -j3 install &> "${_make_install_log}"

log_verbose "==> Sending logs to gist"
gist \
    -u "${LOCAL[gist_id]}" \
    "${LOCAL[make_log]}" \
    "${LOCAL[make_install_log]}"
