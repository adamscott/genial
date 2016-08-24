#!/usr/bin/env bash

QT_BASE_DIR=/opt/qt56
export QTDIR=$QT_BASE_DIR
export PATH=$QT_BASE_DIR/bin:$PATH

if [[ "${TOXENV}" == 'py35-64-pyqt5' ]]; then
  export LD_LIBRARY_PATH=$QT_BASE_DIR/lib/x86_64-linux-gnu:$QT_BASE_DIR/lib:$LD_LIBRARY_PATH
else
  export LD_LIBRARY_PATH=$QT_BASE_DIR/lib/i386-linux-gnu:$QT_BASE_DIR/lib:$LD_LIBRARY_PATH
fi

export PKG_CONFIG_PATH=$QT_BASE_DIR/lib/pkgconfig:$PKG_CONFIG_PATH

export QMAKE=$QT_BASE_DIR/bin/qmake

TEST=`echo $0 | grep wrapper`
if [ "$TEST" != "" ]; then
   exec `echo $0 | sed s/-wrapper//` $*
fi