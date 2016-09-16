#!/usr/bin/env bash
set -ex

if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then
    # Install some custom requirements on OS X
    brew update

    # install gist package
    brew install gist

    # write gist token to ~/.gist
    pushd ~
    echo "${GITHUB_GIST_TOKEN}" &>".gist"
    popd # ~

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
        -skip qtxmlpatterns
    set +e # Disable temporarily exit on error

    # puts make to the background
    echo "Begining make"
    echo ""
    nohup make -j3 &> genial-travis-qt5.7-1_make.log &
    make_pid=$(lsof -t 'genial-travis-qt5.7-1_make.log')
    dots=0
    while [[ ! -z "$(ps cax | grep \'${make_pid}\')" ]]; do
        columns=$(tput cols)
        if [[ "$dots" -gt "$columns" ]]; then
            dots=0
        fi
        python -c "print('\r' + ('.' * ${dots}) + (' ' * (${columns} - ${dots})), end='')"
        let dots+=1
        sleep 5
    done

    # puts make to the background
    echo "Begining make install"
    echo ""
    sudo make -j3 install &> genial-travis-qt5.7-2_make_install.log
    make_pid=$(lsof -t 'genial-travis-qt5.7-1_make.log')
    dots=0
    while [[ ! -z "$(ps cax | grep \'${make_pid}\')" ]]; do
        columns=$(tput cols)
        if [[ "$dots" -gt "$columns" ]]; then
            dots=0
        fi
        python -c "print('\r' + ('.' * ${dots}) + (' ' * (${columns} - ${dots})), end='')"
        let dots+=1
        sleep 5
    done

    gist \
        -u b1f0f29a43cc76a36c8f5fdc10528a25 \
        genial-travis-qt5.7-1_make.log \
        genial-travis-qt5.7-2_make_install.log
    set -e # Reenable exit on error
    gist b1f0f29a43cc76a36c8f5fdc10528a25
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
