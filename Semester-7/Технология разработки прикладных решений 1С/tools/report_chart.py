#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Отчёт-гистограмма на форме с элементом «Диаграмма».

Схема компоновки для диаграммы не используется: вариант настроек с
StructureItemChart компоновщик 8.3.23 разворачивает в детальные записи
(«Детальные записи в диаграмме не допустимы»). Диаграмма, заполняемая
запросом в модуле формы, даёт тот же результат и полностью управляема.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdxml import u, syn, gentypes, write
import forms

MODULE = '''&НаСервере
Процедура ПриСозданииНаСервере(Отказ, СтандартнаяОбработка)

	СформироватьНаСервере();

КонецПроцедуры

&НаКлиенте
Процедура Сформировать(Команда)

	СформироватьНаСервере();

КонецПроцедуры

&НаСервере
Процедура СформироватьНаСервере()

	Запрос = Новый Запрос;
	Запрос.Текст =
%(query)s;

	Выборка = Запрос.Выполнить().Выбрать();

	Диаграмма.Очистить();
	Диаграмма.ТипДиаграммы = ТипДиаграммы.Гистограмма;
	Серия = Диаграмма.УстановитьСерию("%(series)s");

	Пока Выборка.Следующий() Цикл
		Точка = Диаграмма.УстановитьТочку(Строка(Выборка.Точка));
		Диаграмма.УстановитьЗначение(Точка, Серия, Выборка.Значение);
	КонецЦикла;

КонецПроцедуры
'''


def bsl_string(text):
    """Текст запроса -> многострочный литерал встроенного языка."""
    lines = text.split('\n')
    out = ['\t\t"' + lines[0]]
    for l in lines[1:]:
        out.append('\t\t|' + l)
    out[-1] += '"'
    return '\n'.join(out)


def report_chart(out, name, synonym, query, series_title):
    """query обязан возвращать колонки Точка и Значение."""
    body = [
        '\t<Report uuid="%s">' % u(),
        '\t\t<InternalInfo>',
        gentypes('Report', name, ['Object', 'Manager'], 3),
        '\t\t</InternalInfo>',
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<UseStandardCommands>true</UseStandardCommands>',
        '\t\t\t<DefaultForm>Report.%s.Form.ФормаОтчета</DefaultForm>' % name,
        '\t\t</Properties>',
        '\t\t<ChildObjects>',
        '\t\t\t<Form>ФормаОтчета</Form>',
        '\t\t</ChildObjects>',
        '\t</Report>',
    ]
    write(os.path.join(out, 'Reports', name + '.xml'), '\n'.join(body))

    ids = forms.Ids(1)
    items = [
        forms.button('Сформировать', 'Сформировать', ids, title='Сформировать'),
        '\t\t<ChartField name="Диаграмма" id="%d">\n'
        '\t\t\t<DataPath>Диаграмма</DataPath>\n'
        '\t\t\t<Height>20</Height>\n'
        '\t\t\t<AutoMaxHeight>false</AutoMaxHeight>\n'
        '\t\t\t<VerticalStretch>true</VerticalStretch>\n'
        '\t\t\t<HorizontalStretch>true</HorizontalStretch>\n'
        '\t\t</ChartField>' % ids.next(),
    ]
    attrs = [
        forms.attribute('Объект', '<v8:Type>cfg:ReportObject.%s</v8:Type>' % name, main=True, aid=1),
        forms.attribute('Диаграмма', '<v8:Type>v8ui:Chart</v8:Type>', title='Диаграмма', aid=86),
    ]
    cmds = [forms.command('Сформировать', 'Сформировать', 'Сформировать', ids)]
    xml = forms.form_xml(items, attrs, cmds,
                         events=[('OnCreateAtServer', 'ПриСозданииНаСервере')])
    module = MODULE % {'query': bsl_string(query), 'series': series_title}
    forms.write_form(os.path.join(out, 'Reports', name), 'ФормаОтчета', 'Форма отчёта',
                     xml, module=module)
