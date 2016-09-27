#!/usr/bin/env bash
set -ex

declare -A LOCAL  # sets local variable array

LOCAL[tmp_dir]=`mktemp -d 2>/dev/null || mktemp -d -t 'qt_tmp_dir'`
LOCAL[qt_install_dir]=$(echo ~)/qt

mkdir -p "${LOCAL[tmp_dir]}"
mkdir -p "${LOCAL[qt_install_dir]}"

pushd "${LOCAL[tmp_dir]}"
wget https://download.qt.io/official_releases/qt/5.7/5.7.0/single/qt-everywhere-opensource-src-5.7.0.tar.xz
tar xf qt-everywhere-opensource-src-5.7.0.tar.xz

pushd qt-everywhere-opensource-src-5.7.0
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

set +e  # Disable temporarily exit on error

LOCAL[gist_id]="b1f0f29a43cc76a36c8f5fdc10528a25"
LOCAL[make_log]="make-${TRAVIS_OS_NAME}.log"
LOCAL[make_install_log]="make_install-${TRAVIS_OS_NAME}.log"
BUILD_WAIT_LOG="${LOCAL[make_log]}"

build_wait make -j3
sudo make -j3 install &> "${LOCAL[make_install_log]}"
gist \
    -u "${LOCAL[gist_id]}" \
    "${LOCAL[make_log]}" \
    "${LOCAL[make_install_log]}"
set -e  # Reenable exit on error

export PATH="${LOCAL[qt_install_dir]}/bin":$PATH

popd  # ~/tmp/qt-everywhere-opensource-src-5.7.0
popd  # ~/tmp

unset LOCAL  # unsets local variable array
