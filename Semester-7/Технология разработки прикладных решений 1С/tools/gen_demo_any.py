#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерирует исходники конфигурации и встраивает модуль ДемоДанные.
usage: gen_demo_any.py <gen_module> <demo_bsl> <out_dir> [level]"""
import os, sys, io, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_demo

genname, bsl, out = sys.argv[1:4]
lvl = sys.argv[4] if len(sys.argv) > 4 else None
mod = importlib.import_module(genname)
if lvl is not None:
    mod.build(out, int(lvl))
else:
    mod.build(out)
txt = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), bsl), encoding='utf-8-sig').read()
add_demo.inject(out, txt)
print('demo injected ->', out)
