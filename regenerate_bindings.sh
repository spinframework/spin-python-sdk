#!/bin/bash

componentize-py \
    -d src/spin_sdk/wit \
    -w "spin:up/http-trigger@4.0.0" \
    -w "spin:up/redis-trigger@4.0.0" \
    -w "wasi:http/service@0.3.0-rc-2026-03-15" \
    -w "fermyon:spin/http-trigger@3.0.0" \
    -w "fermyon:spin/redis-trigger" \
    --export-interface-name "wasi:http/handler@0.3.0-rc-2026-03-15=http-handler" \
    --export-interface-name "spin:redis/inbound-redis@3.0.0=redis-handler" \
    --world-module spin_sdk.wit \
    --full-names \
    bindings \
    bindings
rm -r src/spin_sdk/wit/imports src/spin_sdk/wit/exports src/componentize_py_*
mv bindings/spin_sdk/wit/* src/spin_sdk/wit/
mv bindings/componentize_py_* src/
# `pdoc3` needs to be able to load all modules in order to generate docs, so we
# provide a stub version of `componentize_py_runtime` to make it happy:
sed 's/\.\.\./raise NotImplementedError/' < src/componentize_py_runtime.pyi > src/componentize_py_runtime.py
rm -r bindings
