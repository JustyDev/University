# -*- coding: utf-8 -*-
"""Обработка «Сервисные операции» — команды из части 2 пособия Семёнова
с доработками по заданиям 3–9.

Модуль формы лежит в отдельном файле `module_service.bsl` и разбит на области;
для каждой лабораторной берутся только те области, которые к ней относятся,
чтобы конфигурация в labN соответствовала состоянию на момент сдачи работы.
"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdxml import HDR, u, syn, gentypes, write
import forms

DP_CATS = ['Object', 'Manager']
MODULE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'module_service.bsl')

# область модуля -> минимальный номер задания, начиная с которого она нужна
REGION_LEVEL = {
    'СлужебныеПроцедуры': (3, 99),
    'ЗаменаЦветаИСтраны': (3, 99),
    'СозданиеГруппы': (4, 99),
    'УдалениеТовара': (4, 99),
    'ВыгрузкаВТекстовыйФайл': (4, 99),
    'ЗагрузкаИзТекстовогоФайлаБазовая': (4, 4),
    'ЗагрузкаИзТекстовогоФайла': (5, 99),
    'ОбменДокументами': (6, 99),
    'КопированиеДокумента': (7, 99),
    'ПереносМеждуГруппами': (9, 99),
}

# элемент формы -> минимальный номер задания
CONTROL_LEVEL = {
    'КатегорияТоваров': 3,
    'ЗаменаЦвета': 3,
    'ЗаменаСтраны': 3,
    'НоваяГруппа': 4,
    'СоздатьГруппу': 4,
    'ТоварДляУдаления': 4,
    'УдалитьТовар': 4,
    'ПутьКФайлу': 4,
    'ВыгрузитьТекст': 4,
    'ЗагрузитьТекст': 4,
    'ДокументПрихода': 6,
    'ПутьКФайлуДокумента': 6,
    'ВыгрузитьДокумент': 6,
    'ЗагрузитьДокумент': 6,
    'КопироватьДокумент': 7,
    'ГруппаПриемник': 9,
    'СтранаОтбора': 9,
    'ПереносИзОднойГруппыВДругую': 9,
}


def module_for_level(level):
    """Собирает текст модуля из областей, актуальных для указанного задания."""
    text = open(MODULE_FILE, encoding='utf-8').read()
    head, _, rest = text.partition('#Область ')
    out = [head.rstrip('\n')]
    for chunk in ('#Область ' + rest).split('#Область ')[1:]:
        name = chunk.split('\n', 1)[0].strip()
        lo, hi = REGION_LEVEL.get(name, (99, 99))
        if lo <= level <= hi:
            out.append('#Область ' + chunk.rstrip('\n'))
    return '\n\n'.join(out) + '\n'


def data_processor(out, name, synonym, form_name='Форма'):
    body = [
        '\t<DataProcessor uuid="%s">' % u(),
        '\t\t<InternalInfo>',
        gentypes('DataProcessor', name, DP_CATS, 3),
        '\t\t</InternalInfo>',
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<UseStandardCommands>true</UseStandardCommands>',
        '\t\t\t<DefaultForm>DataProcessor.%s.Form.%s</DefaultForm>' % (name, form_name),
        '\t\t</Properties>',
        '\t\t<ChildObjects>',
        '\t\t\t<Form>%s</Form>' % form_name,
        '\t\t</ChildObjects>',
        '\t</DataProcessor>',
    ]
    write(os.path.join(out, 'DataProcessors', name + '.xml'), '\n'.join(body))


NUM10 = ('<v8:Type>xs:decimal</v8:Type>\n\t\t\t\t<v8:NumberQualifiers>'
         '\n\t\t\t\t\t<v8:Digits>10</v8:Digits>'
         '\n\t\t\t\t\t<v8:FractionDigits>0</v8:FractionDigits>'
         '\n\t\t\t\t\t<v8:AllowedSign>Any</v8:AllowedSign>'
         '\n\t\t\t\t</v8:NumberQualifiers>')

STR200 = ('<v8:Type>xs:string</v8:Type>\n\t\t\t\t<v8:StringQualifiers>'
          '\n\t\t\t\t\t<v8:Length>200</v8:Length>'
          '\n\t\t\t\t\t<v8:AllowedLength>Variable</v8:AllowedLength>'
          '\n\t\t\t\t</v8:StringQualifiers>')

FOLDERS = ['<ChoiceFoldersAndItems>Folders</ChoiceFoldersAndItems>']

# имя -> (вид, тип, заголовок, extra)
ATTRS = {
    'КатегорияТоваров':    ('<v8:Type>cfg:CatalogRef.Товары</v8:Type>', 'Категория товаров', FOLDERS),
    'НоваяГруппа':         (STR200, 'Новая группа', []),
    'ТоварДляУдаления':    ('<v8:Type>cfg:CatalogRef.Товары</v8:Type>', 'Товар для удаления', []),
    'ПутьКФайлу':          (STR200, 'Файл номенклатуры', []),
    'ДокументПрихода':     ('<v8:Type>cfg:DocumentRef.ПриходТоваров</v8:Type>', 'Документ прихода', []),
    'ПутьКФайлуДокумента': (STR200, 'Файл документа', []),
    'ГруппаПриемник':      ('<v8:Type>cfg:CatalogRef.Товары</v8:Type>', 'Группа-приёмник', FOLDERS),
    'СтранаОтбора':        ('<v8:Type>cfg:CatalogRef.СтраныТоваров</v8:Type>', 'Страна для отбора', []),
}

# имя команды -> заголовок кнопки
COMMANDS = [
    ('ЗаменаЦвета', 'Замена цвета'),
    ('ЗаменаСтраны', 'Замена страны'),
    ('СоздатьГруппу', 'Создать группу'),
    ('УдалитьТовар', 'Удалить товар'),
    ('ВыгрузитьТекст', 'Выгрузить в текстовый файл'),
    ('ЗагрузитьТекст', 'Загрузить из текстового файла'),
    ('ВыгрузитьДокумент', 'Выгрузить документ в файл'),
    ('ЗагрузитьДокумент', 'Загрузить документ из файла'),
    ('КопироватьДокумент', 'Скопировать документ'),
    ('ПереносИзОднойГруппыВДругую', 'Перенос из одной группы в другую'),
]

# порядок элементов на форме: реквизиты и кнопки идут вперемешку по смыслу
LAYOUT = [
    ('attr', 'КатегорияТоваров'),
    ('cmd',  'ЗаменаЦвета'),
    ('cmd',  'ЗаменаСтраны'),
    ('attr', 'НоваяГруппа'),
    ('cmd',  'СоздатьГруппу'),
    ('attr', 'ТоварДляУдаления'),
    ('cmd',  'УдалитьТовар'),
    ('attr', 'ПутьКФайлу'),
    ('cmd',  'ВыгрузитьТекст'),
    ('cmd',  'ЗагрузитьТекст'),
    ('attr', 'ДокументПрихода'),
    ('attr', 'ПутьКФайлуДокумента'),
    ('cmd',  'ВыгрузитьДокумент'),
    ('cmd',  'ЗагрузитьДокумент'),
    ('cmd',  'КопироватьДокумент'),
    ('attr', 'ГруппаПриемник'),
    ('attr', 'СтранаОтбора'),
    ('cmd',  'ПереносИзОднойГруппыВДругую'),
]


def build(out, level):
    name = 'СервисныеОперации'
    data_processor(out, name, 'Сервисные операции')

    ids = forms.Ids(1)
    items = []
    used_attrs = []
    used_cmds = []
    titles = dict(COMMANDS)

    for kind, key in LAYOUT:
        if CONTROL_LEVEL.get(key, 99) > level:
            continue
        if kind == 'attr':
            typexml, title, extra = ATTRS[key]
            items.append(forms.input_field(key, key, ids, title=title, extra=extra))
            used_attrs.append((key, typexml, title))
        else:
            items.append(forms.button(key, key, ids, title=titles[key]))
            used_cmds.append((key, titles[key]))

    attrs = [forms.attribute('Объект', '<v8:Type>cfg:DataProcessorObject.%s</v8:Type>' % name,
                             main=True, aid=1)]
    aid = 80
    for key, typexml, title in used_attrs:
        aid += 1
        attrs.append(forms.attribute(key, typexml, title=title, aid=aid))

    cmds = [forms.command(key, title, key, ids) for key, title in used_cmds]

    xml = forms.form_xml(items, attrs, cmds)
    forms.write_form(os.path.join(out, 'DataProcessors', name), 'Форма', 'Форма',
                     xml, module=module_for_level(level))


# обратная совместимость со старым вызовом
def build_lab3(out):
    build(out, 3)
