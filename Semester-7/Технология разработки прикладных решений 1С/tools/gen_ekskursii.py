# -*- coding: utf-8 -*-
"""Задание 1. Конфигурация «Экскурсии».

Постановка — лабораторная работа № 5 сборника 1С (учёт посещений клиентами
экскурсий), доработки — по заданию курса:
  1) отчёт с гистограммой по самой доходной экскурсии;
  2) колонка «Регион» в списке документов «Посещение экскурсии»;
  3) переоформленный «Отчёт по доходам 2»;
  4) колонка «Регион» в списке — по аналогии со списком «Бронь».
"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdxml import (HDR, u, syn, gentypes, type_ref, type_number, type_date,
                   attribute, write)
import forms, dcs
from report_chart import report_chart
from gen_sklad import catalog, document, subsystem, report, configuration

ENUM_CATS = ['Ref', 'Manager', 'List']

MOD_POSESHENIE = '''Процедура ОбработкаЗаполнения(ДанныеЗаполнения, СтандартнаяОбработка)

\t// Ввод на основании документа «Бронь»: переносим клиента и экскурсию.
\tЕсли ТипЗнч(ДанныеЗаполнения) = Тип("ДокументСсылка.Бронь") Тогда
\t\tБронь = ДанныеЗаполнения;
\t\tКлиент = ДанныеЗаполнения.Клиент;
\t\tЭкскурсия = ДанныеЗаполнения.Экскурсия;
\t\tСумма = ДанныеЗаполнения.Экскурсия.Стоимость;
\tКонецЕсли;

КонецПроцедуры
'''


def enumeration(out, name, synonym, values):
    kids = []
    for val_name, val_syn in values:
        kids += [
            '\t\t\t<EnumValue uuid="%s">' % u(),
            '\t\t\t\t<Properties>',
            '\t\t\t\t\t<Name>%s</Name>' % val_name,
            syn(val_syn, 5),
            '\t\t\t\t\t<Comment/>',
            '\t\t\t\t</Properties>',
            '\t\t\t</EnumValue>',
        ]
    body = [
        '\t<Enum uuid="%s">' % u(),
        '\t\t<InternalInfo>',
        gentypes('Enum', name, ENUM_CATS, 3),
        '\t\t</InternalInfo>',
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<UseStandardCommands>true</UseStandardCommands>',
        '\t\t</Properties>',
        '\t\t<ChildObjects>',
    ] + kids + [
        '\t\t</ChildObjects>',
        '\t</Enum>',
    ]
    write(os.path.join(out, 'Enums', name + '.xml'), '\n'.join(body))


def list_form(out, docname, extra_columns):
    """Форма списка документа с дополнительными колонками (задание 1, пункты 2 и 4)."""
    ids = forms.Ids(1)
    cols = [forms.input_field('Список' + c[0].replace('.', ''), 'Список.' + c[0], ids,
                              level=4, title=c[1]) for c in extra_columns]
    base_cols = [
        forms.input_field('СписокДата', 'Список.Date', ids, level=4),
        forms.input_field('СписокНомер', 'Список.Number', ids, level=4),
    ]
    items = [forms.table('Список', 'Список', ids, base_cols + cols)]
    attrs = [
        '\t\t<Attribute name="Список" id="1">',
        '\t\t\t<Type>',
        '\t\t\t\t<v8:Type>cfg:DynamicList</v8:Type>',
        '\t\t\t</Type>',
        '\t\t\t<MainAttribute>true</MainAttribute>',
        '\t\t\t<SavedData>true</SavedData>',
        '\t\t\t<Settings xsi:type="DynamicList">',
        '\t\t\t\t<ManualQuery>false</ManualQuery>',
        '\t\t\t\t<MainTable>Document.%s</MainTable>' % docname,
        '\t\t\t\t<DynamicDataRead>true</DynamicDataRead>',
        '\t\t\t</Settings>',
        '\t\t</Attribute>',
    ]
    xml = forms.form_xml(items, attrs)
    forms.write_form(os.path.join(out, 'Documents', docname), 'ФормаСписка', 'Форма списка', xml)


def build(out):
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)

    catalog(out, 'Регионы', 'Регионы', 'Регион', 'Регионы', descr_len=50)
    catalog(out, 'Клиенты', 'Клиенты', 'Клиент', 'Клиенты', descr_len=100)
    catalog(out, 'Экскурсии', 'Экскурсии', 'Экскурсия', 'Экскурсии', descr_len=100, attrs=[
        attribute('Регион', 'Регион', type_ref('Catalog', 'Регионы'), fill='ShowError'),
        attribute('Стоимость', 'Стоимость', type_number(15, 2, nonneg=True)),
    ])

    enumeration(out, 'СпособОплаты', 'Способ оплаты', [
        ('Наличными', 'Наличными'),
        ('БанковскойКартой', 'Банковской картой'),
    ])

    document(out, 'Бронь', 'Бронь', attrs=[
        attribute('Клиент', 'Клиент', type_ref('Catalog', 'Клиенты'), fill='ShowError'),
        attribute('Экскурсия', 'Экскурсия', type_ref('Catalog', 'Экскурсии'), fill='ShowError'),
    ], forms_=['ФормаСписка'], default_forms={'list': 'ФормаСписка'}, posting='Allow')

    document(out, 'ПосещениеЭкскурсии', 'Посещение экскурсии', attrs=[
        attribute('Бронь', 'Бронь', type_ref('Document', 'Бронь'), fill='ShowError'),
        attribute('Клиент', 'Клиент', type_ref('Catalog', 'Клиенты'), fill='ShowError'),
        attribute('Экскурсия', 'Экскурсия', type_ref('Catalog', 'Экскурсии'), fill='ShowError'),
        attribute('Сумма', 'Сумма', type_number(15, 2, nonneg=True), fill='ShowError'),
        attribute('СпособОплаты', 'Способ оплаты', '<v8:Type>cfg:EnumRef.СпособОплаты</v8:Type>',
                  fill='ShowError'),
    ], module=MOD_POSESHENIE, based_on=['Document.Бронь'],
       forms_=['ФормаСписка'], default_forms={'list': 'ФормаСписка'}, posting='Allow')

    # задания 1.2 и 1.4 — колонка «Регион» в списках документов
    list_form(out, 'Бронь', [('Клиент', 'Клиент'), ('Экскурсия', 'Экскурсия'),
                             ('Экскурсия.Регион', 'Регион')])
    list_form(out, 'ПосещениеЭкскурсии', [('Клиент', 'Клиент'), ('Экскурсия', 'Экскурсия'),
                                          ('Экскурсия.Регион', 'Регион'),
                                          ('Сумма', 'Сумма'), ('СпособОплаты', 'Способ оплаты')])

    subsystem(out, 'Справочники', 'Справочники',
              ['Catalog.Клиенты', 'Catalog.Экскурсии', 'Catalog.Регионы'])
    subsystem(out, 'Учет', 'Учёт', ['Document.Бронь', 'Document.ПосещениеЭкскурсии'])
    subsystem(out, 'Отчеты', 'Отчёты',
              ['Report.ДоходыСЭкскурсий', 'Report.ОтчетПоДоходам2', 'Report.СамаяДоходнаяЭкскурсия'])

    build_reports(out)

    configuration(out, 'Экскурсии', 'Экскурсии', [
        '<Subsystem>Справочники</Subsystem>',
        '<Subsystem>Учет</Subsystem>',
        '<Subsystem>Отчеты</Subsystem>',
        '<Catalog>Регионы</Catalog>',
        '<Catalog>Клиенты</Catalog>',
        '<Catalog>Экскурсии</Catalog>',
        '<Enum>СпособОплаты</Enum>',
        '<Document>Бронь</Document>',
        '<Document>ПосещениеЭкскурсии</Document>',
        '<Report>ДоходыСЭкскурсий</Report>',
        '<Report>ОтчетПоДоходам2</Report>',
        '<Report>СамаяДоходнаяЭкскурсия</Report>',
    ])
    print('generated ->', out)


QUERY_DOHOD = ("ВЫБРАТЬ\n"
               "\tПосещениеЭкскурсии.Экскурсия КАК Экскурсия,\n"
               "\tПосещениеЭкскурсии.Экскурсия.Регион КАК Регион,\n"
               "\tПосещениеЭкскурсии.Клиент КАК Клиент,\n"
               "\tПосещениеЭкскурсии.СпособОплаты КАК СпособОплаты,\n"
               "\tПосещениеЭкскурсии.Сумма КАК Сумма\n"
               "ИЗ\n"
               "\tДокумент.ПосещениеЭкскурсии КАК ПосещениеЭкскурсии\n"
               "ГДЕ\n"
               "\tПосещениеЭкскурсии.Проведен")


def build_reports(out):
    base_fields = [
        dcs.field('Экскурсия', 'Экскурсия'),
        dcs.field('Регион', 'Регион'),
        dcs.field('Клиент', 'Клиент'),
        dcs.field('СпособОплаты', 'СпособОплаты'),
        dcs.field('Сумма', 'Сумма'),
    ]
    totals = [('Сумма', 'Сумма(Сумма)')]

    # Базовый отчёт из лабораторной: список с группировкой по способу оплаты.
    v1 = dcs.variant_details('Основной', 'Основной',
                             ['Экскурсия', 'Клиент', 'СпособОплаты', 'Сумма'],
                             order=[('Сумма', 'Desc')],
                             group_fields=['СпособОплаты'])
    report(out, 'ДоходыСЭкскурсий', 'Доходы с экскурсий',
           dcs.schema(QUERY_DOHOD, base_fields, totals=totals, variants=[v1]))

    # Задание 1, пункт 3: «Отчёт по доходам 2», оформленный как положено —
    # группировка по экскурсии, детальные записи внутри, отбор по региону.
    v2 = dcs.variant_details('Основной', 'Основной',
                             ['Экскурсия', 'Регион', 'Клиент', 'СпособОплаты', 'Сумма'],
                             filters=[('Регион', 'Equal', u(), 'Регион')],
                             order=[('Сумма', 'Desc')],
                             group_fields=['Экскурсия'])
    report(out, 'ОтчетПоДоходам2', 'Отчёт по доходам 2',
           dcs.schema(QUERY_DOHOD, base_fields, totals=totals, variants=[v2]))

    # Задание 1, пункт 1: самая доходная экскурсия, гистограмма.
    q_chart = ("ВЫБРАТЬ\n"
               "\tПосещениеЭкскурсии.Экскурсия КАК Точка,\n"
               "\tСУММА(ПосещениеЭкскурсии.Сумма) КАК Значение\n"
               "ИЗ\n"
               "\tДокумент.ПосещениеЭкскурсии КАК ПосещениеЭкскурсии\n"
               "ГДЕ\n"
               "\tПосещениеЭкскурсии.Проведен\n"
               "СГРУППИРОВАТЬ ПО\n"
               "\tПосещениеЭкскурсии.Экскурсия\n"
               "УПОРЯДОЧИТЬ ПО\n"
               "\tЗначение УБЫВ")
    report_chart(out, 'СамаяДоходнаяЭкскурсия', 'Самая доходная экскурсия', q_chart, "Доход")


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_build', 'ekskursii')
    build(target)
