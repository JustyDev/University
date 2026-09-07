#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ставит в очередь раннера сборку и запуск внешней обработки.
usage: queue_epf.py <tag> <name> <src_xml_win> <base_win>"""
import os, sys
HOME = os.path.expanduser('~')
R = os.path.join(HOME, 'mnt', 'University', '_runner')
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runepf.ps1.tmpl')

tag, name, src, base = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
t = open(T, encoding='utf-8').read()
for k, v in (('@@TAG@@', tag), ('@@NAME@@', name), ('@@SRC@@', src), ('@@BASE@@', base)):
    t = t.replace(k, v)
with open(os.path.join(R, 'in', tag + '.ps1'), 'w', encoding='utf-8-sig') as f:
    f.write(t)
print('queued', tag)
