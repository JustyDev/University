# -*- coding: utf-8 -*-
"""Добавляет в сгенерированные исходники временный механизм наполнения демо-данными.

Зачем: запуск внешней обработки (.epf) 1С сопровождает модальным предупреждением
безопасности, которое в пакетном режиме некому подтвердить. Код, лежащий внутри
конфигурации, такого предупреждения не вызывает, поэтому демо-данные наливаются
так:

    1cv8t ENTERPRISE /F<база> /C"ЗаполнитьДемоДанные"

После наполнения в базу загружается чистая конфигурация задания — данные остаются,
а служебный модуль в сдаваемую конфигурацию не попадает.
"""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdxml import u, syn, write

APP_MODULE_CALL = '''	Попытка
		ДемоОбработатьПараметрЗапуска();
	Исключение
		Запись = Новый ЗаписьТекста("D:\\Work\\University\\Semester-7\\Технология разработки прикладных решений 1С\\_build\\demo-err.txt", КодировкаТекста.UTF8);
		Запись.ЗаписатьСтроку(ОписаниеОшибки());
		Запись.Закрыть();
	КонецПопытки;
	Если ПараметрЗапуска <> "" Тогда
		Возврат;
	КонецЕсли;

'''

APP_MODULE_DISPATCH = '''
Процедура ДемоОбработатьПараметрЗапуска()

	Если ПараметрЗапуска = "ЗаполнитьДемоДанные" Тогда
		ДемоДанные.Заполнить();
		ЗавершитьРаботуСистемы(Ложь);
	ИначеЕсли СтрНачинаетсяС(ПараметрЗапуска, "ПроверитьОтчет:") Тогда
		ДемоДанные.СформироватьОтчет(Сред(ПараметрЗапуска, СтрДлина("ПроверитьОтчет:") + 1));
		ЗавершитьРаботуСистемы(Ложь);
	ИначеЕсли СтрНачинаетсяС(ПараметрЗапуска, "ПоказатьОтчет:") Тогда
		// стандартная форма отчёта умеет формировать результат при открытии
		ОткрытьФорму("Отчет." + Сред(ПараметрЗапуска, СтрДлина("ПоказатьОтчет:") + 1) + ".Форма",
			Новый Структура("СформироватьПриОткрытии", Истина));
	ИначеЕсли СтрНачинаетсяС(ПараметрЗапуска, "ПоказатьДокумент:") Тогда
		ИмяДокумента = Сред(ПараметрЗапуска, СтрДлина("ПоказатьДокумент:") + 1);
		ПоказатьЗначение(Неопределено, ДемоДанные.ПервыйДокумент(ИмяДокумента));
	ИначеЕсли СтрНачинаетсяС(ПараметрЗапуска, "ПоказатьФорму:") Тогда
		ОткрытьФорму(Сред(ПараметрЗапуска, СтрДлина("ПоказатьФорму:") + 1));
	КонецЕсли;

КонецПроцедуры
'''

APP_MODULE_NEW = '''Процедура ПриНачалеРаботыСистемы()

''' + APP_MODULE_CALL + '''КонецПроцедуры
'''


APP_MODULE_HELPER = ''


def common_module(out, name, text, server_call=True):
    body = [
        '\t<CommonModule uuid="%s">' % u(),
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn('Демо-данные'),
        '\t\t\t<Comment/>',
        '\t\t\t<Global>false</Global>',
        '\t\t\t<ClientManagedApplication>false</ClientManagedApplication>',
        '\t\t\t<Server>true</Server>',
        '\t\t\t<ExternalConnection>false</ExternalConnection>',
        '\t\t\t<ClientOrdinaryApplication>false</ClientOrdinaryApplication>',
        '\t\t\t<ServerCall>%s</ServerCall>' % ('true' if server_call else 'false'),
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


MODULE_TAIL = """

Функция ПервыйДокумент(ИмяДокумента) Экспорт

	Запрос = Новый Запрос;
	Запрос.Текст = "ВЫБРАТЬ ПЕРВЫЕ 1 Док.Ссылка КАК Ссылка ИЗ Документ."
		+ ИмяДокумента + " КАК Док УПОРЯДОЧИТЬ ПО Док.Дата";
	Выборка = Запрос.Выполнить().Выбрать();
	Если Выборка.Следующий() Тогда
		Возврат Выборка.Ссылка;
	КонецЕсли;
	Возврат Неопределено;

КонецФункции
"""

DEMO_FORM_MODULE = """&НаСервере
Процедура ПриСозданииНаСервере(Отказ, СтандартнаяОбработка)

	Результат = ДемоДанные.СформироватьОтчет(Параметры.ИмяОтчета);
	Заголовок = Метаданные.Отчеты[Параметры.ИмяОтчета].Синоним;

КонецПроцедуры
"""


def demo_report_form(out):
    """Общая форма для показа результата отчёта — нужна только демо-сборке."""
    import forms
    from mdxml import write
    name = 'ДемоОтчет'
    body = [
        '\t<CommonForm uuid="%s">' % u(),
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn('Отчёт'),
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
    items = ['\t\t<SpreadsheetDocumentField name="Результат" id="%d">\n'
             '\t\t\t<DataPath>Результат</DataPath>\n'
             '\t\t\t<Height>25</Height>\n'
             '\t\t\t<AutoMaxHeight>false</AutoMaxHeight>\n'
             '\t\t\t<VerticalStretch>true</VerticalStretch>\n'
             '\t\t\t<HorizontalStretch>true</HorizontalStretch>\n'
             '\t\t</SpreadsheetDocumentField>' % ids.next()]
    attrs = [forms.attribute('Результат', '<v8:Type>v8ui:SpreadsheetDocument</v8:Type>',
                             title='Результат', aid=85)]
    xml = forms.form_xml(items, attrs, events=[('OnCreateAtServer', 'ПриСозданииНаСервере')])
    d = os.path.join(out, 'CommonForms', name, 'Ext')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'Form.xml'), 'w', encoding='utf-8') as f:
        f.write(xml)
    md = os.path.join(d, 'Form')
    os.makedirs(md, exist_ok=True)
    with open(os.path.join(md, 'Module.bsl'), 'w', encoding='utf-8-sig') as f:
        f.write(DEMO_FORM_MODULE)


def inject(out, module_text):
    """module_text — текст общего модуля, обязан содержать Процедура Заполнить() Экспорт."""
    assert 'Процедура Заполнить() Экспорт' in module_text
    common_module(out, 'ДемоДанные', module_text + MODULE_TAIL)
    demo_report_form(out)

    # модуль управляемого приложения
    ext = os.path.join(out, 'Ext')
    os.makedirs(ext, exist_ok=True)
    p = os.path.join(ext, 'ManagedApplicationModule.bsl')
    if os.path.exists(p):
        s = open(p, encoding='utf-8-sig').read()
        m = re.search(r'(Процедура\s+ПриНачалеРаботыСистемы\s*\(\s*\)\s*\n)', s)
        if m:
            s = s[:m.end()] + '\n' + APP_MODULE_CALL + s[m.end():]
        else:
            s = APP_MODULE_NEW + '\n' + s
    else:
        s = APP_MODULE_NEW
    s = s + APP_MODULE_HELPER + APP_MODULE_DISPATCH
    with open(p, 'w', encoding='utf-8-sig') as f:
        f.write(s)

    # регистрация модуля в конфигурации
    cfg = os.path.join(out, 'Configuration.xml')
    s = open(cfg, encoding='utf-8-sig').read()
    if '<CommonModule>ДемоДанные</CommonModule>' not in s:
        s = s.replace('\t\t<ChildObjects>\n',
                      '\t\t<ChildObjects>\n\t\t\t<CommonModule>ДемоДанные</CommonModule>\n', 1)
    if '<CommonForm>ДемоОтчет</CommonForm>' not in s:
        s = s.replace('\t\t<ChildObjects>\n',
                      '\t\t<ChildObjects>\n\t\t\t<CommonForm>ДемоОтчет</CommonForm>\n', 1)
    with open(cfg, 'w', encoding='utf-8') as f:
        f.write(s)
