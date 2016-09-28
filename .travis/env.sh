# Add ~/.pyenv to $PATH
if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then  # OS X
    export PATH="/Users/travis/.pyenv/bin:$PATH"
else  # Linux
    export PATH="/home/travis/.pyenv/bin:$PATH"
fi

# Sets $PATH to access Qt binaries
export QT_INSTALL_DIR="$(echo ~)/qt"
export PATH="${QT_INSTALL_DIR}/bin":$PATH

# Sets coloredlogs pattern
export COLOREDLOGS_LOG_FORMAT='[%(hostname)s] %(asctime)s - %(message)s'
