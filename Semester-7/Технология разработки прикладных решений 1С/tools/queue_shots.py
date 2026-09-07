#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Снимает скриншоты работающей конфигурации.
usage: queue_shots.py <tag> <base_win> <dir_win> "<param>|<file.png>;..." """
import os, sys
R = os.path.join(os.path.expanduser('~'), 'mnt', 'University', '_runner')
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots.ps1.tmpl')
tag, base, d, specs = sys.argv[1:5]
t = open(T, encoding='utf-8').read()
for k, v in (('@@TAG@@', tag), ('@@BASE@@', base), ('@@DIR@@', d), ('@@SPECS@@', specs)):
    t = t.replace(k, v)
with open(os.path.join(R, 'in', tag + '.ps1'), 'w', encoding='utf-8-sig') as f:
    f.write(t)
print('queued', tag)
