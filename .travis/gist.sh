#!/usr/bin/env bash
set -e

source colors.sh

echo -e "${COLOR[lightyellow_fg]}=> Setup gist${COLOR[default_fg]}"

echo -e "${COLOR[lightyellow_fg]}==> Downloading and installing gist${COLOR[default_fg]}"
if [[ "${TRAVIS_OS_NAME}" == 'osx' ]]; then  # OS X
    brew install gist
else  # Linux
    gem install gist
fi
# gist is already installed by .travis.yml on Linux

# write gist token to ~/.gist
echo -e "${COLOR[lightyellow_fg]}==> Sets gist token to ~/.gist${COLOR[default_fg]}"
python - << END
import os
with open(os.path.join(os.path.expanduser('~'), '.gist'), 'w') as f:
    f.write(os.environ['GITHUB_GIST_TOKEN'])
END
