# -*- coding: utf-8 -*-
"""Минимальный генератор XML-исходников конфигурации 1С:Предприятие 8.3 (схема 2.16).

Пишем только те свойства, которые реально задаём; остальное 1С добьёт значениями
по умолчанию при загрузке (/LoadConfigFromFiles) и вернёт канонический XML при
обратной выгрузке (/DumpConfigToFiles). Именно канонический вариант кладётся в репозиторий.
"""
import os, uuid

HDR = ('<MetaDataObject xmlns="http://v8.1c.ru/8.3/MDClasses" '
       'xmlns:app="http://v8.1c.ru/8.2/managed-application/core" '
       'xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" '
       'xmlns:cmi="http://v8.1c.ru/8.2/managed-application/cmi" '
       'xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" '
       'xmlns:lf="http://v8.1c.ru/8.2/managed-application/logform" '
       'xmlns:style="http://v8.1c.ru/8.1/data/ui/style" '
       'xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" '
       'xmlns:v8="http://v8.1c.ru/8.1/data/core" '
       'xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" '
       'xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" '
       'xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" '
       'xmlns:xen="http://v8.1c.ru/8.3/xcf/enums" '
       'xmlns:xpr="http://v8.1c.ru/8.3/xcf/predef" '
       'xmlns:xr="http://v8.1c.ru/8.3/xcf/readable" '
       'xmlns:xs="http://www.w3.org/2001/XMLSchema" '
       'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.16">')

def u():
    return str(uuid.uuid4())

def syn(text, indent=3):
    t = '\t' * indent
    if not text:
        return t + '<Synonym/>'
    return (t + '<Synonym>\n' + t + '\t<v8:item>\n' + t + '\t\t<v8:lang>ru</v8:lang>\n'
            + t + '\t\t<v8:content>' + text + '</v8:content>\n' + t + '\t</v8:item>\n' + t + '</Synonym>')

def named(tag, text, indent=3):
    t = '\t' * indent
    if not text:
        return t + '<%s/>' % tag
    return (t + '<%s>\n' % tag + t + '\t<v8:item>\n' + t + '\t\t<v8:lang>ru</v8:lang>\n'
            + t + '\t\t<v8:content>' + text + '</v8:content>\n' + t + '\t</v8:item>\n' + t + '</%s>' % tag)

def gentypes(prefix, name, cats, indent=2):
    t = '\t' * indent
    out = []
    for cat in cats:
        out.append(t + '<xr:GeneratedType name="%s%s.%s" category="%s">' % (prefix, cat, name, cat))
        out.append(t + '\t<xr:TypeId>%s</xr:TypeId>' % u())
        out.append(t + '\t<xr:ValueId>%s</xr:ValueId>' % u())
        out.append(t + '</xr:GeneratedType>')
    return '\n'.join(out)

def type_ref(kind, name):
    """kind: Catalog | Document ..."""
    return '<v8:Type>cfg:%sRef.%s</v8:Type>' % (kind, name)

def type_string(length=0):
    if length:
        return ('<v8:Type>xs:string</v8:Type>\n\t\t\t\t\t<v8:StringQualifiers>\n'
                '\t\t\t\t\t\t<v8:Length>%d</v8:Length>\n'
                '\t\t\t\t\t\t<v8:AllowedLength>Variable</v8:AllowedLength>\n'
                '\t\t\t\t\t</v8:StringQualifiers>' % length)
    return '<v8:Type>xs:string</v8:Type>'

def type_number(digits=10, frac=0, nonneg=False):
    sign = 'Nonnegative' if nonneg else 'Any'
    return ('<v8:Type>xs:decimal</v8:Type>\n\t\t\t\t\t<v8:NumberQualifiers>\n'
            '\t\t\t\t\t\t<v8:Digits>%d</v8:Digits>\n'
            '\t\t\t\t\t\t<v8:FractionDigits>%d</v8:FractionDigits>\n'
            '\t\t\t\t\t\t<v8:AllowedSign>%s</v8:AllowedSign>\n'
            '\t\t\t\t\t</v8:NumberQualifiers>' % (digits, frac, sign))

def type_date(parts='DateTime'):
    return ('<v8:Type>xs:dateTime</v8:Type>\n\t\t\t\t\t<v8:DateQualifiers>\n'
            '\t\t\t\t\t\t<v8:DateFractions>%s</v8:DateFractions>\n'
            '\t\t\t\t\t</v8:DateQualifiers>' % parts)

def attribute(name, synonym, typexml, fill='DontCheck', indent=2, tag='Attribute'):
    t = '\t' * indent
    return '\n'.join([
        t + '<%s uuid="%s">' % (tag, u()),
        t + '\t<Properties>',
        t + '\t\t<Name>%s</Name>' % name,
        syn(synonym, indent + 2),
        t + '\t\t<Comment/>',
        t + '\t\t<Type>',
        t + '\t\t\t' + typexml,
        t + '\t\t</Type>',
        t + '\t\t<FillChecking>%s</FillChecking>' % fill,
        t + '\t</Properties>',
        t + '</%s>' % tag,
    ])

def write(path, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n' + HDR + '\n' + body + '\n</MetaDataObject>\n')
