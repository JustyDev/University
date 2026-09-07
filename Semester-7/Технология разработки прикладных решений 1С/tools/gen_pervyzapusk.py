# -*- coding: utf-8 -*-
"""Задание 8. Форма первого запуска информационной системы.

- Константа `ПервыйЗапускОсуществлен` (Булево).
- Реквизит `Инвентаризация` (Дата) у справочника «Склады».
- Общая форма «ФормаПервогоЗапуска», которая показывает склады с инвентаризацией
  на сегодня; кнопки «Больше не показывать» на ней нет — признак выставляется сам.
- Модуль управляемого приложения: форма не открывается для администратора,
  независимо от значения константы.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdxml import HDR, u, syn, gentypes, write
import forms

APP_MODULE = """Процедура ПриНачалеРаботыСистемы()

\t// Задание 8: решение о показе формы принимается на сервере — в модуле
\t// управляемого приложения нет доступа ни к константам, ни к правам доступа.
\tЕсли ПервыйЗапускСервер.НужноПоказатьФормуПервогоЗапуска() Тогда
\t\tОткрытьФорму("ОбщаяФорма.ФормаПервогоЗапуска");
\tКонецЕсли;

КонецПроцедуры
"""

COMMON_MODULE = """// Серверные проверки для формы первого запуска.

Функция НужноПоказатьФормуПервогоЗапуска() Экспорт

\t// Задание 8, пункт 1: администратору форма не показывается независимо
\t// от значения константы ПервыйЗапускОсуществлен.
\tЕсли ПравоДоступа("Администрирование", Метаданные) Тогда
\t\tВозврат Ложь;
\tКонецЕсли;

\tВозврат НЕ Константы.ПервыйЗапускОсуществлен.Получить();

КонецФункции
"""


def common_module(out, name, synonym, text):
    body = [
        '\t<CommonModule uuid="%s">' % u(),
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<Global>false</Global>',
        '\t\t\t<ClientManagedApplication>false</ClientManagedApplication>',
        '\t\t\t<Server>true</Server>',
        '\t\t\t<ExternalConnection>false</ExternalConnection>',
        '\t\t\t<ClientOrdinaryApplication>false</ClientOrdinaryApplication>',
        '\t\t\t<ServerCall>true</ServerCall>',
        '\t\t\t<Privileged>false</Privileged>',
        '\t\t\t<ReturnValuesReuse>DontUse</ReturnValuesReuse>',
        '\t\t</Properties>',
        '\t</CommonModule>',
    ]
    write(os.path.join(out, 'CommonModules', name + '.xml'), '\n'.join(body))
    d = os.path.join(out, 'CommonModules', name, 'Ext')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'Module.bsl'), 'w', encoding='utf-8-sig') as f:
        f.write(text)


FORM_MODULE = '''&НаСервере
Процедура ПриСозданииНаСервере(Отказ, СтандартнаяОбработка)

\tПриветствие = "Добро пожаловать в конфигурацию «Простой склад»! Это окно "
\t\t+ "показывается один раз — при первом запуске программы.";

\t// Задание 8, пункт 2: показываем склады, у которых инвентаризация сегодня.
\tЗапрос = Новый Запрос;
\tЗапрос.Текст =
\t\t"ВЫБРАТЬ
\t\t|\tСклады.Наименование КАК Наименование,
\t\t|\tСклады.АдресСклада КАК АдресСклада
\t\t|ИЗ
\t\t|\tСправочник.Склады КАК Склады
\t\t|ГДЕ
\t\t|\tНАЧАЛОПЕРИОДА(Склады.Инвентаризация, ДЕНЬ) = &Сегодня";
\tЗапрос.УстановитьПараметр("Сегодня", НачалоДня(ТекущаяДатаСеанса()));

\tВыборка = Запрос.Выполнить().Выбрать();
\tСтроки = Новый Массив;
\tПока Выборка.Следующий() Цикл
\t\tСтроки.Добавить(Выборка.Наименование + " (" + Выборка.АдресСклада + ")");
\tКонецЦикла;

\tЕсли Строки.Количество() = 0 Тогда
\t\tСкладыСИнвентаризацией = "На сегодня инвентаризация не запланирована ни на одном складе.";
\tИначе
\t\tСкладыСИнвентаризацией = "Сегодня инвентаризация на складах: "
\t\t\t+ СтрСоединить(Строки, ", ") + ".";
\tКонецЕсли;

\t// Признак первого запуска выставляем сами — кнопка «Больше не показывать» не нужна.
\tУстановитьПризнакПервогоЗапуска();

КонецПроцедуры

&НаСервереБезКонтекста
Процедура УстановитьПризнакПервогоЗапуска()

\tКонстанты.ПервыйЗапускОсуществлен.Установить(Истина);

КонецПроцедуры
'''


def constant(out, name, synonym, typexml):
    body = [
        '\t<Constant uuid="%s">' % u(),
        '\t\t<InternalInfo>',
        '\n'.join(
            '\t\t\t<xr:GeneratedType name="%s.%s" category="%s">\n'
            '\t\t\t\t<xr:TypeId>%s</xr:TypeId>\n'
            '\t\t\t\t<xr:ValueId>%s</xr:ValueId>\n'
            '\t\t\t</xr:GeneratedType>' % (pref, name, cat, u(), u())
            for pref, cat in (('ConstantManager', 'Manager'),
                              ('ConstantValueManager', 'ValueManager'),
                              ('ConstantValueKey', 'ValueKey'))),
        '\t\t</InternalInfo>',
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<Type>',
        '\t\t\t\t' + typexml,
        '\t\t\t</Type>',
        '\t\t\t<UseStandardCommands>true</UseStandardCommands>',
        '\t\t</Properties>',
        '\t</Constant>',
    ]
    write(os.path.join(out, 'Constants', name + '.xml'), '\n'.join(body))


def common_form(out, name, synonym):
    body = [
        '\t<CommonForm uuid="%s">' % u(),
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<FormType>Managed</FormType>',
        '\t\t\t<IncludeHelpInContents>false</IncludeHelpInContents>',
        '\t\t\t<UsePurposes>',
        '\t\t\t\t<v8:Value xsi:type="app:ApplicationUsePurpose">PlatformApplication</v8:Value>',
        '\t\t\t\t<v8:Value xsi:type="app:ApplicationUsePurpose">MobilePlatformApplication</v8:Value>',
        '\t\t\t</UsePurposes>',
        '\t\t</Properties>',
        '\t</CommonForm>',
    ]
    write(os.path.join(out, 'CommonForms', name + '.xml'), '\n'.join(body))

    ids = forms.Ids(1)
    items = [
        forms.label_field('ПриветствиеНадпись', 'Приветствие', ids, width=80),
        forms.label_field('СкладыСИнвентаризациейНадпись', 'СкладыСИнвентаризацией', ids, width=80),
    ]
    STR500 = ('<v8:Type>xs:string</v8:Type>\n\t\t\t\t<v8:StringQualifiers>'
              '\n\t\t\t\t\t<v8:Length>500</v8:Length>'
              '\n\t\t\t\t\t<v8:AllowedLength>Variable</v8:AllowedLength>'
              '\n\t\t\t\t</v8:StringQualifiers>')
    attrs = [
        forms.attribute('Приветствие', STR500, aid=81, title='Приветствие'),
        forms.attribute('СкладыСИнвентаризацией', STR500, aid=82, title='Инвентаризация'),
    ]
    xml = forms.form_xml(items, attrs, events=[('OnCreateAtServer', 'ПриСозданииНаСервере')])
    d = os.path.join(out, 'CommonForms', name, 'Ext')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'Form.xml'), 'w', encoding='utf-8') as f:
        f.write(xml)
    md = os.path.join(d, 'Form')
    os.makedirs(md, exist_ok=True)
    with open(os.path.join(md, 'Module.bsl'), 'w', encoding='utf-8-sig') as f:
        f.write(FORM_MODULE)


def build(out):
    common_module(out, 'ПервыйЗапускСервер', 'Первый запуск (сервер)', COMMON_MODULE)
    constant(out, 'ПервыйЗапускОсуществлен', 'Первый запуск осуществлён',
             '<v8:Type>xs:boolean</v8:Type>')
    common_form(out, 'ФормаПервогоЗапуска', 'Форма первого запуска')
    d = os.path.join(out, 'Ext')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'ManagedApplicationModule.bsl'), 'w', encoding='utf-8-sig') as f:
        f.write(APP_MODULE)
