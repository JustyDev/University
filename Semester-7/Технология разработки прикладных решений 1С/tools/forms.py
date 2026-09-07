# -*- coding: utf-8 -*-
"""Сборка управляемых форм 1С.

Форму описываем минимально — только элементы и пути к данным. Всю обвязку
(контекстные меню, подсказки, строку поиска) платформа достраивает сама при
загрузке конфигурации из файлов.
"""
import os
from mdxml import HDR, u, syn, write

FORM_HDR = ('<Form xmlns="http://v8.1c.ru/8.3/xcf/logform" '
            'xmlns:app="http://v8.1c.ru/8.2/managed-application/core" '
            'xmlns:cfg="http://v8.1c.ru/8.1/data/enterprise/current-config" '
            'xmlns:ent="http://v8.1c.ru/8.1/data/enterprise" '
            'xmlns:lf="http://v8.1c.ru/8.2/managed-application/logform" '
            'xmlns:style="http://v8.1c.ru/8.1/data/ui/style" '
            'xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" '
            'xmlns:v8="http://v8.1c.ru/8.1/data/core" '
            'xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" '
            'xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" '
            'xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows" '
            'xmlns:xr="http://v8.1c.ru/8.3/xcf/readable" '
            'xmlns:xs="http://www.w3.org/2001/XMLSchema" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="2.16">')


class Ids(object):
    """Раздатчик идентификаторов элементов формы."""
    def __init__(self, start=2):
        self.n = start

    def next(self):
        self.n += 1
        return self.n


def ind(level):
    return '\t' * level


def input_field(name, path, ids, level=2, title=None, footer_path=None, extra=()):
    t = ind(level)
    out = [t + '<InputField name="%s" id="%d">' % (name, ids.next()),
           t + '\t<DataPath>%s</DataPath>' % path]
    if title:
        out.append(t + '\t<Title>\n' + t + '\t\t<v8:item>\n' + t + '\t\t\t<v8:lang>ru</v8:lang>\n'
                   + t + '\t\t\t<v8:content>%s</v8:content>\n' % title + t + '\t\t</v8:item>\n' + t + '\t</Title>')
    if footer_path:
        out.append(t + '\t<FooterDataPath>%s</FooterDataPath>' % footer_path)
        out.append(t + '\t<FooterHorizontalAlign>Right</FooterHorizontalAlign>')
    out.extend(t + '\t' + e for e in extra)
    out.append(t + '</InputField>')
    return '\n'.join(out)


def label_field(name, path, ids, level=2, title=None, width=None, extra=()):
    t = ind(level)
    out = [t + '<LabelField name="%s" id="%d">' % (name, ids.next()),
           t + '\t<DataPath>%s</DataPath>' % path]
    if title:
        out.append(t + '\t<Title>\n' + t + '\t\t<v8:item>\n' + t + '\t\t\t<v8:lang>ru</v8:lang>\n'
                   + t + '\t\t\t<v8:content>%s</v8:content>\n' % title + t + '\t\t</v8:item>\n' + t + '\t</Title>')
    if width:
        # без явной ширины платформа обрезает длинный текст многоточием
        out.append(t + '\t<Width>%d</Width>' % width)
        out.append(t + '\t<AutoMaxWidth>false</AutoMaxWidth>')
        out.append(t + '\t<MultiLine>true</MultiLine>')
    out.extend(t + '\t' + e for e in extra)
    out.append(t + '</LabelField>')
    return '\n'.join(out)


def table(name, path, ids, children, level=2, footer=False, extra=()):
    t = ind(level)
    tid = ids.next()
    out = [t + '<Table name="%s" id="%d">' % (name, tid),
           t + '\t<DataPath>%s</DataPath>' % path]
    if footer:
        out.append(t + '\t<Footer>true</Footer>')
    out.extend(t + '\t' + e for e in extra)
    out.append(t + '\t<ChildItems>')
    out.extend(children)
    out.append(t + '\t</ChildItems>')
    out.append(t + '\t<AutoCommandBar name="%sКоманднаяПанель" id="-%d"/>' % (name, tid))
    out.append(t + '</Table>')
    return '\n'.join(out)


def button(name, command_name, ids, level=2, title=None):
    t = ind(level)
    out = [t + '<Button name="%s" id="%d">' % (name, ids.next()),
           t + '\t<Type>UsualButton</Type>',
           t + '\t<CommandName>Form.Command.%s</CommandName>' % command_name]
    if title:
        out.append(t + '\t<Title>\n' + t + '\t\t<v8:item>\n' + t + '\t\t\t<v8:lang>ru</v8:lang>\n'
                   + t + '\t\t\t<v8:content>%s</v8:content>\n' % title + t + '\t\t</v8:item>\n' + t + '\t</Title>')
    out.append(t + '</Button>')
    return '\n'.join(out)


def attribute(name, typexml, level=2, main=False, title=None, aid=100):
    t = ind(level)
    out = [t + '<Attribute name="%s" id="%d">' % (name, aid),
           t + '\t<Type>',
           t + '\t\t' + typexml,
           t + '\t</Type>']
    if main:
        out.append(t + '\t<MainAttribute>true</MainAttribute>')
        out.append(t + '\t<SavedData>true</SavedData>')
    if title:
        out.append(t + '\t<Title>\n' + t + '\t\t<v8:item>\n' + t + '\t\t\t<v8:lang>ru</v8:lang>\n'
                   + t + '\t\t\t<v8:content>%s</v8:content>\n' % title + t + '\t\t</v8:item>\n' + t + '\t</Title>')
    out.append(t + '</Attribute>')
    return '\n'.join(out)


def command(name, title, action, ids, level=2):
    t = ind(level)
    return '\n'.join([
        t + '<Command name="%s" id="%d">' % (name, ids.next()),
        t + '\t<Title>',
        t + '\t\t<v8:item>',
        t + '\t\t\t<v8:lang>ru</v8:lang>',
        t + '\t\t\t<v8:content>%s</v8:content>' % title,
        t + '\t\t</v8:item>',
        t + '\t</Title>',
        t + '\t<Action>%s</Action>' % action,
        t + '</Command>',
    ])


def form_xml(items, attributes, commands=(), events=()):
    out = ['<?xml version="1.0" encoding="UTF-8"?>', FORM_HDR, '\t<ChildItems>']
    out.extend(items)
    out.append('\t</ChildItems>')
    out.append('\t<AutoCommandBar name="ФормаКоманднаяПанель" id="-1"/>')
    out.append('\t<Attributes>')
    out.extend(attributes)
    out.append('\t</Attributes>')
    if commands:
        out.append('\t<Commands>')
        out.extend(commands)
        out.append('\t</Commands>')
    if events:
        # события самой формы: без этого блока платформа не вызывает обработчики
        out.append('\t<Events>')
        for name, handler in events:
            out.append('\t\t<Event name="%s">%s</Event>' % (name, handler))
        out.append('\t</Events>')
    out.append('</Form>')
    return '\n'.join(out) + '\n'


def write_form(owner_dir, form_name, synonym, xml, module=None):
    """owner_dir — например .../Documents/ПриходТоваров"""
    body = '\n'.join([
        '\t<Form uuid="%s">' % u(),
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % form_name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<FormType>Managed</FormType>',
        '\t\t\t<IncludeHelpInContents>false</IncludeHelpInContents>',
        '\t\t\t<UsePurposes>',
        '\t\t\t\t<v8:Value xsi:type="app:ApplicationUsePurpose">PlatformApplication</v8:Value>',
        '\t\t\t\t<v8:Value xsi:type="app:ApplicationUsePurpose">MobilePlatformApplication</v8:Value>',
        '\t\t\t</UsePurposes>',
        '\t\t</Properties>',
        '\t</Form>',
    ])
    write(os.path.join(owner_dir, 'Forms', form_name + '.xml'), body)
    d = os.path.join(owner_dir, 'Forms', form_name, 'Ext')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'Form.xml'), 'w', encoding='utf-8') as f:
        f.write(xml)
    if module:
        md = os.path.join(d, 'Form')
        os.makedirs(md, exist_ok=True)
        with open(os.path.join(md, 'Module.bsl'), 'w', encoding='utf-8-sig') as f:
            f.write(module)
