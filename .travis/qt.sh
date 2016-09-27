#!/usr/bin/env bash
set -e

source colors.sh
source helper.sh

echo -e "${COLOR[lightyellow_fg]}=> Qt installation${COLOR[default_fg]}"

_tmp_dir=`mktemp -d 2>/dev/null || mktemp -d -t 'qt_tmp_dir'`

mkdir -p "${LOCAL[tmp_dir]}"
mkdir -p QT_INSTALL_DIR

pushd "${LOCAL[tmp_dir]}"
echo -e "${COLOR[lightyellow_fg]}==> Downloading Qt source code${COLOR[default_fg]}"
wget https://download.qt.io/official_releases/qt/5.7/5.7.0/single/qt-everywhere-opensource-src-5.7.0.tar.xz
echo -e "${COLOR[lightyellow_fg]}==> Extracting Qt source code${COLOR[default_fg]}"
tar xf qt-everywhere-opensource-src-5.7.0.tar.xz

pushd qt-everywhere-opensource-src-5.7.0
echo -e "${COLOR[lightyellow_fg]}==> configure${COLOR[default_fg]}"
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

LOCAL[gist_id]="b1f0f29a43cc76a36c8f5fdc10528a25"
LOCAL[make_log]="make-${TRAVIS_OS_NAME}.log"
LOCAL[make_install_log]="make_install-${TRAVIS_OS_NAME}.log"
BUILD_WAIT_LOG="${LOCAL[make_log]}"

echo -e "${COLOR[lightyellow_fg]}==> make${COLOR[default_fg]}"
build_wait make -j3

echo -e "${COLOR[lightyellow_fg]}==> make install${COLOR[default_fg]}"
sudo make -j3 install &> "${LOCAL[make_install_log]}"

echo -e "${COLOR[lightyellow_fg]}==> Sending logs to gist${COLOR[default_fg]}"
gist \
    -u "${LOCAL[gist_id]}" \
    "${LOCAL[make_log]}" \
    "${LOCAL[make_install_log]}"
