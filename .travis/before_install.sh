#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then
    # Install some custom requirements on OS X
    brew update

    pushd /tmp
    wget https://download.qt.io/official_releases/qt/5.7/5.7.0/single/qt-everywhere-opensource-src-5.7.0.tar.gz
    gunzip qt-everywhere-opensource-src-5.7.0.tar.gz
    tar xf qt-everywhere-opensource-src-5.7.0.tar
    pushd qt-everywhere-opensource-src-5.7.0
    QT_BASE_DIR=/opt/qt57
    sudo mkdir -p "$QT_BASE_DIR"
    ./configure \
        $(: === MISC ===)\
        -opensource \
        -confirm-license \
        -release \
        -prefix "/opt/qt57" \
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
        -skip qtxmlpatterns \
        $(: === NO-FEATURE ===)\
        -no-feature-properties \
        -no-feature-texthtmlparser \
        -no-feature-textodfwriter \
        -no-feature-cssparser \
        -no-feature-regularexpression \
        -no-feature-concurrent \
        -no-feature-draganddrop \
        -no-feature-sessionmanager \
        -no-feature-shortcut \
        -no-feature-action \
        -no-feature-cursor \
        -no-feature-clipboard \
        -no-feature-wheelevent \
        -no-feature-tabletevent \
        -no-feature-effects \
        -no-feature-sharedmemory \
        -no-feature-systemsemaphore \
        -no-feature-xmlstream \
        -no-feature-xmlstreamreader \
        -no-feature-xmlstreamwriter \
        -no-feature-im \
        $(: -no-feature-textdate) \
        $(: -no-feature-datestring) \
        -no-feature-process \
        -no-feature-temporaryfile \
        -no-feature-library \
        -no-feature-settings \
        -no-feature-dom \
        -no-feature-filesystemmodel \
        -no-feature-filesystemwatcher \
        -no-feature-filesystemiterator \
        -no-feature-treewidget \
        -no-feature-listwidget \
        -no-feature-tablewidget \
        -no-feature-datetimeedit \
        -no-feature-stackedwidget \
        -no-feature-textbrowser \
        -no-feature-splashscreen \
        -no-feature-splitter \
        -no-feature-lcdnumber \
        -no-feature-menu \
        -no-feature-lineedit \
        -no-feature-spinbox \
        -no-feature-tabbar \
        -no-feature-tabwidget \
        -no-feature-combobox \
        -no-feature-fontcombobox \
        -no-feature-toolbutton \
        -no-feature-toolbar \
        -no-feature-toolbox \
        -no-feature-groupbox \
        -no-feature-buttongroup \
        -no-feature-mainwindow \
        -no-feature-dockwidget \
        -no-feature-mdiarea \
        -no-feature-resizehandler \
        -no-feature-statusbar \
        -no-feature-menubar \
        -no-feature-contextmenu \
        -no-feature-progressbar \
        -no-feature-slider \
        -no-feature-scrollbar \
        -no-feature-dial \
        -no-feature-scrollarea \
        -no-feature-graphicsview \
        -no-feature-graphicseffect \
        -no-feature-spinwidget \
        -no-feature-textedit \
        -no-feature-syntaxhighlighter \
        -no-feature-rubberband \
        -no-feature-tooltip \
        -no-feature-statustip \
        -no-feature-whatsthis \
        -no-feature-validator \
        -no-feature-sizegrip \
        -no-feature-calendarwidget \
        -no-feature-printpreviewwidget \
        -no-feature-keysequenceedit \
        -no-feature-messagebox \
        -no-feature-colordialog \
        -no-feature-filedialog \
        -no-feature-fontdialog \
        -no-feature-printdialog \
        -no-feature-printpreviewdialog \
        -no-feature-progressdialog \
        -no-feature-inputdialog \
        -no-feature-errormessage \
        -no-feature-wizard \
        -no-feature-itemviews \
        -no-feature-dirmodel \
        -no-feature-standarditemmodel \
        -no-feature-proxymodel \
        -no-feature-sortfilterproxymodel \
        -no-feature-identityproxymodel \
        -no-feature-stringlistmodel \
        -no-feature-listview \
        -no-feature-tableview \
        -no-feature-treeview \
        -no-feature-datawidgetmapper \
        -no-feature-columnview \
        -no-feature-style_windows \
        -no-feature-style_fusion \
        -no-feature-style_windowsxp \
        -no-feature-style_windowsvista \
        -no-feature-style_windowsce \
        -no-feature-style_windowsmobile \
        -no-feature-style_stylesheet \
        -no-feature-imageformatplugin \
        -no-feature-movie \
        -no-feature-imageformat_bmp \
        -no-feature-imageformat_ppm \
        -no-feature-imageformat_xbm \
        -no-feature-imageformat_xpm \
        -no-feature-imageformat_png \
        -no-feature-imageformat_jpeg \
        -no-feature-image_heuristic_mask \
        -no-feature-image_text \
        -no-feature-picture \
        -no-feature-colornames \
        -no-feature-pdf \
        -no-feature-printer \
        -no-feature-cups \
        -no-feature-paint_debug \
        -no-feature-freetype \
        -no-feature-translation \
        -no-feature-textcodec \
        -no-feature-codecs \
        -no-feature-big_codecs \
        -no-feature-iconv \
        -no-feature-ftp \
        -no-feature-http \
        -no-feature-udpsocket \
        -no-feature-networkproxy \
        -no-feature-socks5 \
        -no-feature-networkinterface \
        -no-feature-networkdiskcache \
        -no-feature-bearermanagement \
        -no-feature-localserver \
        -no-feature-completer \
        -no-feature-fscompleter \
        -no-feature-desktopservices \
        -no-feature-mimetype \
        -no-feature-systemtrayicon \
        -no-feature-undocommand \
        -no-feature-undostack \
        -no-feature-undogroup \
        -no-feature-undoview \
        -no-feature-accessibility \
        -no-feature-animation \
        $(: -no-feature-statemachine) \
        -no-feature-gestures \
        -no-feature-dbus \
        -no-feature-xmlschema
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
