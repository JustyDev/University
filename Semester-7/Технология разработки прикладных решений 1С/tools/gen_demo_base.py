#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генерирует исходники конфигурации «Простой склад» указанного уровня
и встраивает в них служебный модуль ДемоДанные.

usage: gen_demo_base.py <out_dir> <level>
"""
import os, sys, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_sklad, add_demo

out = sys.argv[1]
lvl = int(sys.argv[2])
gen_sklad.build(out, lvl)
txt = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'demo_sklad.bsl'),
              encoding='utf-8-sig').read()
add_demo.inject(out, txt)
print('demo injected ->', out)
