#!/usr/bin/env sh
# Enables recursive search.
shopt -s globstar
# Removes non matching patterns.
shopt -s nullglob

# Pycharm passes project dir as the first parameter
basedir=""
if [ -z $1 ]; then
    basedir="."
else
    basedir="$1"
fi

function main() {
    function compile() {
        local compiler=$1
        local for_pattern=$2
        local sed_pattern=$3
        for file in $for_pattern; do
            local output=$(echo $file  | sed -E "${sed_pattern}")
            echo "==> $compiler $file -o $output"
            local error=$(eval "${compiler} ${file} -o ${output} 2>&1")
            if ! [ $? -eq 0 ]; then
                echo "====> An error occured when compiling $file." 1>&2
                echo $error 1>&2
                exit 1
            fi
        done
    }

    compile 'pyuic5' "$basedir/genial/**/*.ui" 's/((.*\/)(.*)).ui/\2ui_\3.py/g'
    compile 'pyrcc5' "$basedir/genial/**/*.qrc" 's/(.*).qrc/\1_rc.py/g'
}

main