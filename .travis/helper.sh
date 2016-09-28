#@IgnoreInspection BashAddShebang

# Based on travis_wait
# https://github.com/travis-ci/travis-build/blob/bbe7c12b6f2c8bdc6cd9a7d3e839a729048648ae/lib/travis/build/templates/header.sh
build_wait() {
  local timeout=$1

  if [[ $timeout =~ ^[0-9]+$ ]]; then
    # looks like an integer, so we assume it's a timeout
    shift
  else
    # default value
    timeout=20
  fi

  local cmd="$@"
  local log_file=travis_wait_$$.log

  if [ -z "${BUILD_WAIT_LOG}" ]; then
    BUILD_WAIT_LOG=$log_file
  fi

  $cmd &>$log_file &
  local cmd_pid=$!

  travis_jigger $! $timeout $cmd &
  local jigger_pid=$!
  local result

  {
    wait $cmd_pid 2>/dev/null
    result=$?
    ps -p$jigger_pid &>/dev/null && kill $jigger_pid
  }

  if [ $result -eq 0 ]; then
    echo -e "\n${ANSI_GREEN}The command $cmd exited with $result.${ANSI_RESET}"
  else
    echo -e "\n${ANSI_RED}The command $cmd exited with $result.${ANSI_RESET}"
  fi

  # Copy log to the determined log file name
  echo -e "\n${ANSI_GREEN}Writing log to file '${BUILD_WAIT_LOG}'.${ANSI_RESET}\n"
  cp $log_file "${BUILD_WAIT_LOG}"

  return $result
}

install_coloredlogs() {
    pip install --user coloredlogs
}

is_coloredlogs_installed() {
    local list
    list=$(pip list)
    echo "${list}" | grep -q coloredlogs
    echo $?
}

log_info() { local text=$1; _log info "${text}"; }
log_debug() { local text=$1; _log debug "{$text}"; }
log_warn() { local text=$1; _log warn "${text}"; }
log_error() { local text=$1; _log error "${text}"; }
log_critical() { local text=$1; _log critical "${text}"; }

_log() {
    if [[ "$(is_coloredlogs_installed)" -ne "0" ]]; then
        install_coloredlogs
    fi

    local type=$1

    if [[ "$type" =~ ^(info|debug|warn|error|critical)$ ]]; then
        type=info
    fi

    if [[ "$#" -gt "1" ]]; then
        shift
    fi

    local text=$1

    local script=''
    read -r -d '' script <<EOF
import logging
import os
import sys
import coloredlogs

logger = logging.getLogger()
coloredlogs.install(level='DEBUG', stream=sys.stdout)
logger.${type}('${text}')
EOF

    python -c "${script}"
}
