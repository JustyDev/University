#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Готовит базу к скриншотам: демо-конфигурация -> наполнение -> чистая конфигурация.
usage: queue_prep.py <tag> <src_demo_win> <src_clean_win> <base_win> [shot_png_win]"""
import os, sys
R = os.path.join(os.path.expanduser('~'), 'mnt', 'University', '_runner')
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prep_base.ps1.tmpl')
tag, demo, clean, base = sys.argv[1:5]
shot = sys.argv[5] if len(sys.argv) > 5 else ''
reports = sys.argv[6] if len(sys.argv) > 6 else ''
t = open(T, encoding='utf-8').read()
for k, v in (('@@TAG@@', tag), ('@@SRCDEMO@@', demo), ('@@SRCCLEAN@@', clean),
             ('@@BASE@@', base), ('@@SHOT@@', shot), ('@@REPORTS@@', reports)):
    t = t.replace(k, v)
with open(os.path.join(R, 'in', tag + '.ps1'), 'w', encoding='utf-8-sig') as f:
    f.write(t)
print('queued', tag)
