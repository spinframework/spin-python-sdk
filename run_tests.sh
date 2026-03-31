#!/bin/bash

source venv/bin/activate

if [ ! -d examples/matrix-math/numpy ]
then
  (cd examples/matrix-math \
     && curl -OL https://github.com/dicej/wasi-wheels/releases/download/v0.0.2/numpy-wasi.tar.gz \
     && tar xf numpy-wasi.tar.gz)
fi

for example in examples/*
do
  echo "building $example"
  (cd $example && spin build) || exit 1
done

pushd examples/hello
spin up &
spin_pid=$!

for x in $(seq 1 10)
do
  message="$(curl -s localhost:3000)"
  if [ "$message" = "Hello from Python!" ]
  then
    result=success
    break
  fi
  sleep 1
done

kill "$spin_pid"

if [ "$result" != "success" ]
then
  exit 1
fi
popd

# TODO: run more examples
