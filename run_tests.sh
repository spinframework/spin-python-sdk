#!/bin/bash

source venv/bin/activate

# First, install any example-specific dependencies (common dependencies such as
# `componentize-py`, `spin-sdk`, and `mypy` are assumed to have been installed
# in the virtual environment).

if [ ! -d examples/matrix-math/numpy ]
then
  (cd examples/matrix-math \
     && curl -OL https://github.com/dicej/wasi-wheels/releases/download/v0.0.2/numpy-wasi.tar.gz \
     && tar xf numpy-wasi.tar.gz)
fi

# Next, run MyPy on all the examples

for example in examples/*
do
  echo "linting $example"
  if [ $example = "examples/matrix-math" ]
  then
    # NumPy fails linting as of this writing, so we skip it
    extra_option="--follow-imports silent"
  else
    unset extra_option
  fi
  export MYPYPATH=$(pwd)/src
  (cd $example && mypy --strict $extra_option -m app) || exit 1
done

# Next, build all the examples

for example in examples/*
do
  echo "building $example"
  (cd $example && spin build) || exit 1
done

# Finally, run some of the examples and test that they behave as expected

for example in examples/hello examples/external-lib-example examples/spin-kv examples/spin-variables
do
  pushd $example
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
done

for example in examples/streaming
do
  pushd $example
  spin up &
  spin_pid=$!

  for x in $(seq 1 10)
  do
    message="$(curl -s -d 'Hello from Python!' localhost:3000/echo)"
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
done

# TODO: run more examples
