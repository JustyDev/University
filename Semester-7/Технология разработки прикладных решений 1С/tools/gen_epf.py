# -*- coding: utf-8 -*-
"""Сборка внешней обработки (.epf) из XML-исходников.

Структура каталога, которую ждёт /LoadExternalDataProcessorOrReportFromFiles:

    <корень>/<Имя>.xml
    <корень>/<Имя>/Forms/<Форма>.xml
    <корень>/<Имя>/Forms/<Форма>/Ext/Form.xml
    <корень>/<Имя>/Forms/<Форма>/Ext/Form/Module.bsl
"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdxml import HDR, u, syn, gentypes, write
import forms

STR1000 = ('<v8:Type>xs:string</v8:Type>\n\t\t\t\t<v8:StringQualifiers>'
           '\n\t\t\t\t\t<v8:Length>1000</v8:Length>'
           '\n\t\t\t\t\t<v8:AllowedLength>Variable</v8:AllowedLength>'
           '\n\t\t\t\t</v8:StringQualifiers>')


def build(root, name, synonym, module, autoclose=True):
    """Пишет исходники внешней обработки с одной формой, выполняющей module."""
    if os.path.isdir(root):
        shutil.rmtree(root)
    os.makedirs(root)

    body = [
        '\t<ExternalDataProcessor uuid="%s">' % u(),
        '\t\t<InternalInfo>',
        gentypes('ExternalDataProcessor', name, ['Object'], 3),
        '\t\t</InternalInfo>',
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<DefaultForm>ExternalDataProcessor.%s.Form.Форма</DefaultForm>' % name,
        '\t\t</Properties>',
        '\t\t<ChildObjects>',
        '\t\t\t<Form>Форма</Form>',
        '\t\t</ChildObjects>',
        '\t</ExternalDataProcessor>',
    ]
    write(os.path.join(root, name + '.xml'), '\n'.join(body))

    ids = forms.Ids(1)
    items = [forms.label_field('ИтогНадпись', 'Итог', ids, title='Результат')]
    attrs = [
        forms.attribute('Объект', '<v8:Type>cfg:ExternalDataProcessorObject.%s</v8:Type>' % name,
                        main=True, aid=1),
        forms.attribute('Итог', STR1000, title='Результат', aid=80),
    ]
    xml = forms.form_xml(items, attrs)
    # После выполнения работы форма не открывается и система закрывается —
    # иначе процесс 1С висит в ожидании пользователя и блокирует пакетный прогон.
    autoclose_code = '''

&НаКлиенте
Процедура ПриОткрытии(Отказ)

\tОтказ = Истина;
\tЗавершитьРаботуСистемы(Ложь);

КонецПроцедуры
'''
    forms.write_form(os.path.join(root, name), 'Форма', 'Форма', xml,
                     module=module + (autoclose_code if autoclose else ''))
