#!/usr/bin/env bash
set -ex

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
