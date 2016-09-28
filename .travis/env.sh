#@IgnoreInspection BashAddShebang

# Add ~/.pyenv to $PATH
if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then  # OS X
    export PATH="/Users/travis/.pyenv/bin:$PATH"
else  # Linux
    export PATH="/home/travis/.pyenv/bin:$PATH"
fi

# Sets $PATH to access Qt binaries
if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then  # OS X
    export QT_INSTALL_DIR="$(echo ~)/qt"
    export PATH="${QT_INSTALL_DIR}/bin":$PATH
else
    export QT_INSTALL_DIR="/opt/qt57"
    export PATH="${QT_INSTALL_DIR}/bin":$PATH
fi

# Sets coloredlogs pattern
export COLOREDLOGS_LOG_FORMAT='[%(asctime)s] %(levelname)s %(message)s'
export COLOREDLOGS_FIELD_STYLES='asctime=green;levelname=magenta'
