# -*- coding: utf-8 -*-
"""Сборка схемы компоновки данных (СКД) для отчётов."""

DCS_HDR = ('<DataCompositionSchema xmlns="http://v8.1c.ru/8.1/data-composition-system/schema" '
           'xmlns:dcscor="http://v8.1c.ru/8.1/data-composition-system/core" '
           'xmlns:dcsset="http://v8.1c.ru/8.1/data-composition-system/settings" '
           'xmlns:v8="http://v8.1c.ru/8.1/data/core" '
           'xmlns:xs="http://www.w3.org/2001/XMLSchema" '
           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')


def field(path, name, role=None, title=None):
    out = ['\t\t<field xsi:type="DataSetFieldField">',
           '\t\t\t<dataPath>%s</dataPath>' % path,
           '\t\t\t<field>%s</field>' % name]
    if title:
        out.append('\t\t\t<title xsi:type="v8:LocalStringType"><v8:item><v8:lang>ru</v8:lang>'
                   '<v8:content>%s</v8:content></v8:item></title>' % title)
    if role:
        out.append('\t\t\t<role>')
        if role == 'dimension':
            out.append('\t\t\t\t<dcscor:dimension>true</dcscor:dimension>')
        elif role == 'balance':
            out.append('\t\t\t\t<dcscor:balance>true</dcscor:balance>')
            out.append('\t\t\t\t<dcscor:accountingBalanceType>AccountingBalance</dcscor:accountingBalanceType>')
        out.append('\t\t\t</role>')
    out.append('\t\t</field>')
    return '\n'.join(out)


def schema(query, fields, totals=(), params=(), variants=()):
    out = ['<?xml version="1.0" encoding="UTF-8"?>', DCS_HDR,
           '\t<dataSource>',
           '\t\t<name>ИсточникДанных1</name>',
           '\t\t<dataSourceType>Local</dataSourceType>',
           '\t</dataSource>',
           '\t<dataSet xsi:type="DataSetQuery">',
           '\t\t<name>НаборДанных1</name>']
    out.extend(fields)
    out.append('\t\t<dataSource>ИсточникДанных1</dataSource>')
    out.append('\t\t<query>%s</query>' % query)
    out.append('\t</dataSet>')
    for path, expr in totals:
        out.append('\t<totalField>')
        out.append('\t\t<dataPath>%s</dataPath>' % path)
        out.append('\t\t<expression>%s</expression>' % expr)
        out.append('\t</totalField>')
    for name, title, vtype in params:
        out.append('\t<parameter>')
        out.append('\t\t<name>%s</name>' % name)
        out.append('\t\t<title xsi:type="v8:LocalStringType"><v8:item><v8:lang>ru</v8:lang>'
                   '<v8:content>%s</v8:content></v8:item></title>' % title)
        out.append('\t\t<valueType>%s</valueType>' % vtype)
        out.append('\t\t<use>Auto</use>')
        out.append('\t</parameter>')
    out.extend(variants)
    out.append('</DataCompositionSchema>')
    return '\n'.join(out)


def variant_details(name, presentation, selection_fields, filters=(), order=(), group_fields=None):
    """Вариант настроек компоновки.

    filters: список (поле, вид сравнения, uuid пользовательской настройки, представление)
             — все выводятся в быстрые настройки и по умолчанию выключены (необязательный отбор).
    """
    S = '\t\t\t'
    out = ['\t<settingsVariant>',
           '\t\t<dcsset:name>%s</dcsset:name>' % name,
           '\t\t<dcsset:presentation xsi:type="xs:string">%s</dcsset:presentation>' % presentation,
           '\t\t<dcsset:settings xmlns:style="http://v8.1c.ru/8.1/data/ui/style" '
           'xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" '
           'xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" '
           'xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows">']
    out.append(S + '<dcsset:selection>')
    for f in selection_fields:
        out.append(S + '\t<dcsset:item xsi:type="dcsset:SelectedItemField">')
        out.append(S + '\t\t<dcsset:field>%s</dcsset:field>' % f)
        out.append(S + '\t</dcsset:item>')
    out.append(S + '</dcsset:selection>')
    if filters:
        out.append(S + '<dcsset:filter>')
        for fld, comp, userid, pres in filters:
            out.append(S + '\t<dcsset:item xsi:type="dcsset:FilterItemComparison">')
            out.append(S + '\t\t<dcsset:use>false</dcsset:use>')
            out.append(S + '\t\t<dcsset:left xsi:type="dcsset:FieldField">%s</dcsset:left>' % fld)
            out.append(S + '\t\t<dcsset:comparisonType>%s</dcsset:comparisonType>' % comp)
            out.append(S + '\t\t<dcsset:viewMode>QuickAccess</dcsset:viewMode>')
            out.append(S + '\t\t<dcsset:userSettingID>%s</dcsset:userSettingID>' % userid)
            out.append(S + '\t\t<dcsset:userSettingPresentation xsi:type="xs:string">%s</dcsset:userSettingPresentation>' % pres)
            out.append(S + '\t</dcsset:item>')
        out.append(S + '</dcsset:filter>')
    if order:
        out.append(S + '<dcsset:order>')
        for fld, direction in order:
            out.append(S + '\t<dcsset:item xsi:type="dcsset:OrderItemField">')
            out.append(S + '\t\t<dcsset:field>%s</dcsset:field>' % fld)
            out.append(S + '\t\t<dcsset:orderType>%s</dcsset:orderType>' % direction)
            out.append(S + '\t</dcsset:item>')
        out.append(S + '</dcsset:order>')
    # структура отчёта
    out.append(S + '<dcsset:item xsi:type="dcsset:StructureItemGroup">')
    out.append(S + '\t<dcsset:groupItems>')
    for gf in (group_fields or []):
        out.append(S + '\t\t<dcsset:item xsi:type="dcsset:GroupItemField">')
        out.append(S + '\t\t\t<dcsset:field>%s</dcsset:field>' % gf)
        out.append(S + '\t\t\t<dcsset:groupType>Items</dcsset:groupType>')
        out.append(S + '\t\t\t<dcsset:periodAdditionType>None</dcsset:periodAdditionType>')
        out.append(S + '\t\t\t<dcsset:periodAdditionBegin xsi:type="xs:dateTime">0001-01-01T00:00:00</dcsset:periodAdditionBegin>')
        out.append(S + '\t\t\t<dcsset:periodAdditionEnd xsi:type="xs:dateTime">0001-01-01T00:00:00</dcsset:periodAdditionEnd>')
        out.append(S + '\t\t</dcsset:item>')
    out.append(S + '\t</dcsset:groupItems>')
    out.append(S + '\t<dcsset:order>')
    out.append(S + '\t\t<dcsset:item xsi:type="dcsset:OrderItemAuto"/>')
    out.append(S + '\t</dcsset:order>')
    out.append(S + '\t<dcsset:selection>')
    out.append(S + '\t\t<dcsset:item xsi:type="dcsset:SelectedItemAuto"/>')
    out.append(S + '\t</dcsset:selection>')
    out.append(S + '</dcsset:item>')
    out.append('\t\t</dcsset:settings>')
    out.append('\t</settingsVariant>')
    return '\n'.join(out)


def variant_chart(name, presentation, point_field, value_field, series_field=None,
                  chart_type='Histogram'):
    """Вариант настроек с диаграммой: точки — по полю, значение — ресурс.

    Группы точек и серий записываются без xsi:type: внутри диаграммы это
    элементы типа «группировка диаграммы», и лишний xsi:type заставляет
    компоновщик считать их обычными группировками с детальными записями,
    а детальные записи в диаграмме не допускаются.
    """
    S = '\t\t\t'

    def group(field):
        return [
            S + '\t\t<dcsset:item>',
            S + '\t\t\t<dcsset:groupItems>',
            S + '\t\t\t\t<dcsset:item xsi:type="dcsset:GroupItemField">',
            S + '\t\t\t\t\t<dcsset:field>%s</dcsset:field>' % field,
            S + '\t\t\t\t\t<dcsset:groupType>Items</dcsset:groupType>',
            S + '\t\t\t\t\t<dcsset:periodAdditionType>None</dcsset:periodAdditionType>',
            S + '\t\t\t\t\t<dcsset:periodAdditionBegin xsi:type="xs:dateTime">0001-01-01T00:00:00</dcsset:periodAdditionBegin>',
            S + '\t\t\t\t\t<dcsset:periodAdditionEnd xsi:type="xs:dateTime">0001-01-01T00:00:00</dcsset:periodAdditionEnd>',
            S + '\t\t\t\t</dcsset:item>',
            S + '\t\t\t</dcsset:groupItems>',
            S + '\t\t</dcsset:item>',
        ]

    out = ['\t<settingsVariant>',
           '\t\t<dcsset:name>%s</dcsset:name>' % name,
           '\t\t<dcsset:presentation xsi:type="xs:string">%s</dcsset:presentation>' % presentation,
           '\t\t<dcsset:settings xmlns:style="http://v8.1c.ru/8.1/data/ui/style" '
           'xmlns:sys="http://v8.1c.ru/8.1/data/ui/fonts/system" '
           'xmlns:v8ui="http://v8.1c.ru/8.1/data/ui" '
           'xmlns:web="http://v8.1c.ru/8.1/data/ui/colors/web" '
           'xmlns:win="http://v8.1c.ru/8.1/data/ui/colors/windows">',
           S + '<dcsset:selection>',
           S + '\t<dcsset:item xsi:type="dcsset:SelectedItemField">',
           S + '\t\t<dcsset:field>%s</dcsset:field>' % value_field,
           S + '\t</dcsset:item>',
           S + '</dcsset:selection>',
           S + '<dcsset:item xsi:type="dcsset:StructureItemChart">',
           S + '\t<dcsset:point>'] + group(point_field) + [
           S + '\t</dcsset:point>',
           S + '\t<dcsset:series>'] + (group(series_field) if series_field else []) + [
           S + '\t</dcsset:series>',
           S + '</dcsset:item>',
           '\t\t</dcsset:settings>',
           '\t</settingsVariant>']
    return '\n'.join(out)
