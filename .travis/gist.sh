#!/usr/bin/env bash
set -e

source helpers.sh

log_verbose "=> Setup gist"

log_verbose "==> Downloading and installing gist"
if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then  # OS X
    brew install gist
else  # Linux
    gem install gist
fi
# gist is already installed by .travis.yml on Linux

# write gist token to ~/.gist
log_verbose "==> Sets gist token to ~/.gist"
python - <<EOF
import os
with open(os.path.join(os.path.expanduser('~'), '.gist'), 'w') as f:
    f.write(os.environ['GITHUB_GIST_TOKEN'])
EOF
