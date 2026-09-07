#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ставит в очередь раннера сборку конфигурации 1С.
usage: queue_build.py <tag> <src_win> <base_win> [dump_win] [cf_win]"""
import os, sys
HOME = os.path.expanduser('~')
R = os.path.join(HOME, 'mnt', 'University', '_runner')
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build1c.ps1.tmpl')

def main():
    tag, src, base = sys.argv[1], sys.argv[2], sys.argv[3]
    dump = sys.argv[4] if len(sys.argv) > 4 else ''
    cf   = sys.argv[5] if len(sys.argv) > 5 else ''
    t = open(T, encoding='utf-8').read()
    for k, v in (('@@TAG@@', tag), ('@@SRC@@', src), ('@@BASE@@', base),
                 ('@@DUMP@@', dump), ('@@CF@@', cf)):
        t = t.replace(k, v)
    p = os.path.join(R, 'in', tag + '.ps1')
    with open(p, 'w', encoding='utf-8-sig') as f:
        f.write(t)
    print('queued', p)

if __name__ == '__main__':
    main()
