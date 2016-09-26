#!/usr/bin/env bash

pids=`lsof -i:7400 -t`
if [[ "$pids" != "" ]]; then
	kill -TERM $pids
fi

