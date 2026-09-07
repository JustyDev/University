# -*- coding: utf-8 -*-
"""Генерация XML-исходников конфигурации «Простой склад» (пособие Семёнова, часть 1)."""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mdxml import HDR, u, syn, named, gentypes, type_ref, type_string, type_number, attribute, write
import dcs
import forms
import gen_obrabotki
import gen_pervyzapusk

CAT_CATS  = ['Object', 'Ref', 'Selection', 'List', 'Manager']
DOC_CATS  = ['Object', 'Ref', 'Selection', 'List', 'Manager']
REG_CATS  = ['Selection', 'List', 'Manager', 'RecordSet', 'RecordKey', 'Record']
REP_CATS  = ['Object', 'Manager']


CFG_CLASS_IDS = [
    '9cd510cd-abfc-11d4-9434-004095e12fc7',
    '9fcd25a0-4822-11d4-9414-008048da11f9',
    'e3687481-0a87-462c-a166-9f34594f9bba',
    '9de14907-ec23-4a07-96f0-85521cb6b53b',
    '51f2d5d8-ea4d-4064-8892-82951750031e',
    'e68182ea-4237-4383-967f-90c1e3370bc7',
    'fb282519-d103-4dd3-bc12-cb271d631dfc',
]


def cfg_internal_info():
    out = ['\t\t<InternalInfo>']
    for cid in CFG_CLASS_IDS:
        out.append('\t\t\t<xr:ContainedObject>')
        out.append('\t\t\t\t<xr:ClassId>%s</xr:ClassId>' % cid)
        out.append('\t\t\t\t<xr:ObjectId>%s</xr:ObjectId>' % u())
        out.append('\t\t\t</xr:ContainedObject>')
    out.append('\t\t</InternalInfo>')
    return '\n'.join(out)


def catalog(out, name, synonym, obj_pres='', list_pres='', hierarchical=False,
            code_len=9, descr_len=25, attrs=()):
    body = [
        '\t<Catalog uuid="%s">' % u(),
        '\t\t<InternalInfo>',
        gentypes('Catalog', name, CAT_CATS, 3),
        '\t\t</InternalInfo>',
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<Hierarchical>%s</Hierarchical>' % ('true' if hierarchical else 'false'),
        '\t\t\t<HierarchyType>HierarchyFoldersAndItems</HierarchyType>',
        '\t\t\t<FoldersOnTop>true</FoldersOnTop>',
        '\t\t\t<CodeLength>%d</CodeLength>' % code_len,
        '\t\t\t<DescriptionLength>%d</DescriptionLength>' % descr_len,
        '\t\t\t<CodeType>String</CodeType>',
        '\t\t\t<CodeAllowedLength>Variable</CodeAllowedLength>',
        '\t\t\t<CodeSeries>WholeCatalog</CodeSeries>',
        '\t\t\t<CheckUnique>true</CheckUnique>',
        '\t\t\t<Autonumbering>true</Autonumbering>',
        '\t\t\t<DefaultPresentation>AsDescription</DefaultPresentation>',
        named('ObjectPresentation', obj_pres),
        named('ListPresentation', list_pres),
        '\t\t</Properties>',
    ]
    if attrs:
        body.append('\t\t<ChildObjects>')
        body.extend(attrs)
        body.append('\t\t</ChildObjects>')
    else:
        body.append('\t\t<ChildObjects/>')
    body.append('\t</Catalog>')
    write(os.path.join(out, 'Catalogs', name + '.xml'), '\n'.join(body))


def accum_register(out, name, synonym, dims, ress, reg_type='Balance'):
    body = [
        '\t<AccumulationRegister uuid="%s">' % u(),
        '\t\t<InternalInfo>',
        gentypes('AccumulationRegister', name, REG_CATS, 3),
        '\t\t</InternalInfo>',
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<UseStandardCommands>true</UseStandardCommands>',
        '\t\t\t<RegisterType>%s</RegisterType>' % reg_type,
        '\t\t\t<EnableTotalsSplitting>true</EnableTotalsSplitting>',
        '\t\t</Properties>',
        '\t\t<ChildObjects>',
    ]
    body.extend(dims)
    body.extend(ress)
    body.append('\t\t</ChildObjects>')
    body.append('\t</AccumulationRegister>')
    write(os.path.join(out, 'AccumulationRegisters', name + '.xml'), '\n'.join(body))



MOD_PRIHOD = """Процедура ОбработкаПроведения(Отказ, Режим)
	//{{__КОНСТРУКТОР_ДВИЖЕНИЙ_РЕГИСТРОВ
	// Данный фрагмент построен конструктором.
	// При повторном использовании конструктора, внесенные вручную изменения будут утеряны!!!

	// регистр ОстаткиТоваров Приход
	Движения.ОстаткиТоваров.Записывать = Истина;
	Для Каждого ТекСтрокаСписокТоваров Из СписокТоваров Цикл
		Движение = Движения.ОстаткиТоваров.Добавить();
		Движение.ВидДвижения = ВидДвиженияНакопления.Приход;
		Движение.Период = Дата;
		Движение.Товар = ТекСтрокаСписокТоваров.Товар;
		Движение.Склад = Склад;
		Движение.Количество = ТекСтрокаСписокТоваров.Количество;
	КонецЦикла;

	//}}__КОНСТРУКТОР_ДВИЖЕНИЙ_РЕГИСТРОВ
КонецПроцедуры
"""

MOD_RASHOD = """Процедура ОбработкаПроведения(Отказ, Режим)
	// регистр ОстаткиТоваров Расход
	Движения.ОстаткиТоваров.Записывать = Истина;
	Для Каждого ТекСтрокаСписокТоваров Из СписокТоваров Цикл
		Движение = Движения.ОстаткиТоваров.Добавить();
		Движение.ВидДвижения = ВидДвиженияНакопления.Расход;
		Движение.Период = Дата;
		Движение.Склад = Склад;
		Движение.Товар = ТекСтрокаСписокТоваров.Товар;
		Движение.Количество = ТекСтрокаСписокТоваров.Количество;
	КонецЦикла;
	Движения.Записать();

	// Контроль отрицательных остатков: расход не должен уводить остаток в минус.
	Запрос = Новый Запрос;
	Запрос.Текст =
		"ВЫБРАТЬ
		|	ОстаткиТоваровОстатки.Товар,
		|	ОстаткиТоваровОстатки.КоличествоОстаток
		|ИЗ
		|	РегистрНакопления.ОстаткиТоваров.Остатки КАК ОстаткиТоваровОстатки
		|ГДЕ
		|	ОстаткиТоваровОстатки.КоличествоОстаток < 0";

	РезультатЗапроса = Запрос.Выполнить();

	Если НЕ РезультатЗапроса.Пустой() Тогда
		Отказ = Истина;
		ВыборкаДетальныеЗаписи = РезультатЗапроса.Выбрать();
		Пока ВыборкаДетальныеЗаписи.Следующий() Цикл
			Сообщить("Не хватает кол-ва для товара " + ВыборкаДетальныеЗаписи.Товар
				+ ", нужно еще " + ВыборкаДетальныеЗаписи.КоличествоОстаток);
		КонецЦикла;
	КонецЕсли;
КонецПроцедуры
"""


def tabular_section(name, synonym, attrs, owner_kind='Document', owner=''):
    full = '%s.%s' % (owner, name)
    ii = ['\t\t\t\t<InternalInfo>']
    for cat, pref in (('TabularSection', owner_kind + 'TabularSection'),
                      ('TabularSectionRow', owner_kind + 'TabularSectionRow')):
        ii.append('\t\t\t\t\t<xr:GeneratedType name="%s.%s" category="%s">' % (pref, full, cat))
        ii.append('\t\t\t\t\t\t<xr:TypeId>%s</xr:TypeId>' % u())
        ii.append('\t\t\t\t\t\t<xr:ValueId>%s</xr:ValueId>' % u())
        ii.append('\t\t\t\t\t</xr:GeneratedType>')
    ii.append('\t\t\t\t</InternalInfo>')
    body = ['\t\t\t<TabularSection uuid="%s">' % u()] + ii + [
            '\t\t\t\t<Properties>',
            '\t\t\t\t\t<Name>%s</Name>' % name,
            syn(synonym, 5),
            '\t\t\t\t\t<Comment/>',
            '\t\t\t\t</Properties>',
            '\t\t\t\t<ChildObjects>']
    body.extend(attrs)
    body.append('\t\t\t\t</ChildObjects>')
    body.append('\t\t\t</TabularSection>')
    return '\n'.join(body)


def document(out, name, synonym, attrs=(), tabsecs=(), registers=(), module=None, forms_=(), based_on=(), default_forms=None, posting=None):
    body = [
        '\t<Document uuid="%s">' % u(),
        '\t\t<InternalInfo>',
        gentypes('Document', name, DOC_CATS, 3),
        '\t\t</InternalInfo>',
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<UseStandardCommands>true</UseStandardCommands>',
        '\t\t\t<NumberType>String</NumberType>',
        '\t\t\t<NumberLength>9</NumberLength>',
        '\t\t\t<NumberAllowedLength>Variable</NumberAllowedLength>',
        '\t\t\t<NumberPeriodicity>Year</NumberPeriodicity>',
        '\t\t\t<CheckUnique>true</CheckUnique>',
        '\t\t\t<Autonumbering>true</Autonumbering>',
        '\t\t\t<Posting>%s</Posting>' % (posting or ('Allow' if registers else 'Deny')),
        '\t\t\t<RealTimePosting>Allow</RealTimePosting>',
    ]
    if based_on:
        body.append('\t\t\t<BasedOn>')
        for b in based_on:
            body.append('\t\t\t\t<xr:Item xsi:type="xr:MDObjectRef">%s</xr:Item>' % b)
        body.append('\t\t\t</BasedOn>')
    if registers:
        body.append('\t\t\t<RegisterRecords>')
        for r in registers:
            body.append('\t\t\t\t<xr:Item>%s</xr:Item>' % r)
        body.append('\t\t\t</RegisterRecords>')
    df = default_forms if default_forms is not None else ({'object': forms_[0]} if forms_ else {})
    for kind, tag in (('object', 'DefaultObjectForm'), ('list', 'DefaultListForm'),
                      ('choice', 'DefaultChoiceForm')):
        if df.get(kind):
            # только append: insert перед последним элементом попадал внутрь BasedOn/RegisterRecords
            body.append('\t\t\t<%s>Document.%s.Form.%s</%s>' % (tag, name, df[kind], tag))
    body.append('\t\t</Properties>')
    kids = list(attrs) + list(tabsecs) + ['\t\t\t<Form>%s</Form>' % f for f in forms_]
    if kids:
        body.append('\t\t<ChildObjects>')
        body.extend(kids)
        body.append('\t\t</ChildObjects>')
    else:
        body.append('\t\t<ChildObjects/>')
    body.append('\t</Document>')
    write(os.path.join(out, 'Documents', name + '.xml'), '\n'.join(body))
    if module:
        d = os.path.join(out, 'Documents', name, 'Ext')
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'ObjectModule.bsl'), 'w', encoding='utf-8-sig') as f:
            f.write(module)



def report(out, name, synonym, dcs_xml, template='ОсновнаяСхемаКомпоновкиДанных'):
    body = [
        '\t<Report uuid="%s">' % u(),
        '\t\t<InternalInfo>',
        gentypes('Report', name, REP_CATS, 3),
        '\t\t</InternalInfo>',
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<UseStandardCommands>true</UseStandardCommands>',
        '\t\t\t<MainDataCompositionSchema>Report.%s.Template.%s</MainDataCompositionSchema>' % (name, template),
        '\t\t</Properties>',
        '\t\t<ChildObjects>',
        '\t\t\t<Template>%s</Template>' % template,
        '\t\t</ChildObjects>',
        '\t</Report>',
    ]
    write(os.path.join(out, 'Reports', name + '.xml'), '\n'.join(body))

    tpl = [
        '\t<Template uuid="%s">' % u(),
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % template,
        syn('Основная схема компоновки данных'),
        '\t\t\t<Comment/>',
        '\t\t\t<TemplateType>DataCompositionSchema</TemplateType>',
        '\t\t</Properties>',
        '\t</Template>',
    ]
    write(os.path.join(out, 'Reports', name, 'Templates', template + '.xml'), '\n'.join(tpl))

    d = os.path.join(out, 'Reports', name, 'Templates', template, 'Ext')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'Template.xml'), 'w', encoding='utf-8') as f:
        f.write(dcs_xml)



def subsystem(out, name, synonym, content, include_help=False):
    body = [
        '\t<Subsystem uuid="%s">' % u(),
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<IncludeHelpInContents>false</IncludeHelpInContents>',
        '\t\t\t<IncludeInCommandInterface>true</IncludeInCommandInterface>',
        '\t\t\t<Content>',
    ]
    for c in content:
        body.append('\t\t\t\t<xr:Item>%s</xr:Item>' % c)
    body += [
        '\t\t\t</Content>',
        '\t\t</Properties>',
        '\t\t<ChildObjects/>',
        '\t</Subsystem>',
    ]
    write(os.path.join(out, 'Subsystems', name + '.xml'), '\n'.join(body))



FORM_MODULE_ITOG = """&НаКлиенте
Процедура ПересчитатьИтог()
	Итого = 0;
	Для Каждого Строка Из Объект.СписокТоваров Цикл
		Итого = Итого + Строка.Количество;
	КонецЦикла;
	ИтогоКоличество = Итого;
КонецПроцедуры

&НаСервере
Процедура ПриСозданииНаСервере(Отказ, СтандартнаяОбработка)
	Итого = 0;
	Для Каждого Строка Из Объект.СписокТоваров Цикл
		Итого = Итого + Строка.Количество;
	КонецЦикла;
	ИтогоКоличество = Итого;
КонецПроцедуры

&НаКлиенте
Процедура СписокТоваровКоличествоПриИзменении(Элемент)
	ПересчитатьИтог();
КонецПроцедуры

&НаКлиенте
Процедура СписокТоваровПослеУдаления(Элемент)
	ПересчитатьИтог();
КонецПроцедуры
"""


def doc_form(out, docname):
    """Управляемая форма приходного/расходного документа.

    Цвет и страна тянутся из карточки товара (путь Объект.СписокТоваров.Товар.ЦветТовара),
    в подвале табличной части — итоговое количество.
    """
    ids = forms.Ids(1)
    cols = [
        forms.input_field('СписокТоваровТовар', 'Объект.СписокТоваров.Товар', ids, level=4),
        forms.input_field('СписокТоваровЦветТовара', 'Объект.СписокТоваров.Товар.ЦветТовара', ids, level=4),
        forms.input_field('СписокТоваровСтранаТовара', 'Объект.СписокТоваров.Товар.СтранаТовара', ids, level=4),
        forms.input_field('СписокТоваровКоличество', 'Объект.СписокТоваров.Количество', ids, level=4,
                          footer_path='ИтогоКоличество',
                          extra=['<Events>\n\t\t\t\t\t<Event name="OnChange">СписокТоваровКоличествоПриИзменении</Event>\n\t\t\t\t</Events>']),
    ]
    items = [
        forms.input_field('Номер', 'Объект.Number', ids),
        forms.input_field('Дата', 'Объект.Date', ids),
        forms.input_field('Склад', 'Объект.Склад', ids),
        forms.table('СписокТоваров', 'Объект.СписокТоваров', ids, cols, footer=True),
    ]
    attrs = [
        forms.attribute('Объект', '<v8:Type>cfg:DocumentObject.%s</v8:Type>' % docname, main=True, aid=1),
        forms.attribute('ИтогоКоличество',
                        '<v8:Type>xs:decimal</v8:Type>\n\t\t\t\t<v8:NumberQualifiers>'
                        '\n\t\t\t\t\t<v8:Digits>10</v8:Digits>'
                        '\n\t\t\t\t\t<v8:FractionDigits>0</v8:FractionDigits>'
                        '\n\t\t\t\t\t<v8:AllowedSign>Any</v8:AllowedSign>'
                        '\n\t\t\t\t</v8:NumberQualifiers>',
                        title='Итого количество', aid=90),
    ]
    xml = forms.form_xml(items, attrs, events=[('OnCreateAtServer', 'ПриСозданииНаСервере')])
    forms.write_form(os.path.join(out, 'Documents', docname), 'ФормаДокумента', 'Форма документа',
                     xml, module=FORM_MODULE_ITOG)



def configuration(out, name, synonym, children):
    """Configuration.xml + язык. children — список строк вида '<Catalog>Товары</Catalog>'."""
    cfg = [
        '\t<Configuration uuid="%s">' % u(),
        cfg_internal_info(),
        '\t\t<Properties>',
        '\t\t\t<Name>%s</Name>' % name,
        syn(synonym),
        '\t\t\t<Comment/>',
        '\t\t\t<DefaultRunMode>ManagedApplication</DefaultRunMode>',
        '\t\t\t<ScriptVariant>Russian</ScriptVariant>',
        '\t\t\t<DefaultLanguage>Language.Русский</DefaultLanguage>',
        '\t\t\t<CompatibilityMode>Version8_3_23</CompatibilityMode>',
        '\t\t\t<ConfigurationExtensionCompatibilityMode>Version8_3_23</ConfigurationExtensionCompatibilityMode>',
        '\t\t\t<ModalityUseMode>DontUse</ModalityUseMode>',
        '\t\t\t<SynchronousPlatformExtensionAndAddInCallUseMode>DontUse</SynchronousPlatformExtensionAndAddInCallUseMode>',
        '\t\t\t<InterfaceCompatibilityMode>Taxi</InterfaceCompatibilityMode>',
        '\t\t\t<DataLockControlMode>Managed</DataLockControlMode>',
        '\t\t</Properties>',
        '\t\t<ChildObjects>',
        '\t\t\t<Language>Русский</Language>',
    ] + ['\t\t\t' + c for c in children] + [
        '\t\t</ChildObjects>',
        '\t</Configuration>',
    ]
    write(os.path.join(out, 'Configuration.xml'), '\n'.join(cfg))

    lang = [
        '\t<Language uuid="%s">' % u(),
        '\t\t<Properties>',
        '\t\t\t<Name>Русский</Name>',
        syn('Русский'),
        '\t\t\t<Comment/>',
        '\t\t\t<LanguageCode>ru</LanguageCode>',
        '\t\t</Properties>',
        '\t</Language>',
    ]
    write(os.path.join(out, 'Languages', 'Русский.xml'), '\n'.join(lang))


def build(out, level=2):
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)

    # --- справочники ---
    catalog(out, 'ЦветаТоваров', 'Цвета товаров', 'Цвет', 'Цвета товаров', descr_len=40)
    catalog(out, 'СтраныТоваров', 'Страны товаров', 'Страна', 'Страны товаров', descr_len=40)
    sklad_attrs = [attribute('АдресСклада', 'Адрес склада', type_string(100), fill='ShowError')]
    if level >= 8:
        # задание 8: дата плановой инвентаризации склада
        from mdxml import type_date
        sklad_attrs.append(attribute('Инвентаризация', 'Инвентаризация', type_date('Date')))
    catalog(out, 'Склады', 'Склады', 'Склад', 'Наши склады', attrs=sklad_attrs)
    catalog(out, 'Товары', 'Товары', 'Товар', 'Наши товары', hierarchical=True, attrs=[
        attribute('ЦветТовара', 'Цвет товара', type_ref('Catalog', 'ЦветаТоваров')),
        attribute('СтранаТовара', 'Страна товара', type_ref('Catalog', 'СтраныТоваров'), fill='ShowError'),
    ])

    # --- регистр накопления ---
    accum_register(out, 'ОстаткиТоваров', 'Остатки товаров',
        dims=[
            attribute('Товар', 'Товар', type_ref('Catalog', 'Товары'), tag='Dimension'),
            attribute('Склад', 'Склад', type_ref('Catalog', 'Склады'), tag='Dimension'),
        ],
        ress=[
            attribute('Количество', 'Количество', type_number(10, 0), tag='Resource'),
        ])

    # --- документы ---
    def tovar_ts(docname):
        return tabular_section('СписокТоваров', 'Список товаров', owner=docname, attrs=[
            attribute('Товар', 'Товар', type_ref('Catalog', 'Товары'), fill='ShowError', indent=5),
            attribute('ЦветТовара', 'Цвет товара', type_ref('Catalog', 'ЦветаТоваров'), indent=5),
            attribute('СтранаТовара', 'Страна товара', type_ref('Catalog', 'СтраныТоваров'), indent=5),
            attribute('Количество', 'Количество', type_number(10, 0, nonneg=True), fill='ShowError', indent=5),
        ])

    document(out, 'ПриходТоваров', 'Приход товаров',
             attrs=[attribute('Склад', 'Склад', type_ref('Catalog', 'Склады'), fill='ShowError')],
             tabsecs=[tovar_ts('ПриходТоваров')],
             registers=['AccumulationRegister.ОстаткиТоваров'],
             module=MOD_PRIHOD, forms_=['ФормаДокумента'])
    doc_form(out, 'ПриходТоваров')

    document(out, 'РасходТоваров', 'Расход товаров',
             attrs=[attribute('Склад', 'Склад', type_ref('Catalog', 'Склады'), fill='ShowError')],
             tabsecs=[tovar_ts('РасходТоваров')],
             registers=['AccumulationRegister.ОстаткиТоваров'],
             module=MOD_RASHOD, forms_=['ФормаДокумента'])
    doc_form(out, 'РасходТоваров')

    # --- отчёт «Остатки товаров» на СКД ---
    q = ("ВЫБРАТЬ\n"
         "\tОстаткиТоваровОстатки.Товар КАК Товар,\n"
         "\tОстаткиТоваровОстатки.Склад КАК Склад,\n"
         "\tОстаткиТоваровОстатки.КоличествоОстаток КАК КоличествоОстаток\n"
         "ИЗ\n"
         "\tРегистрНакопления.ОстаткиТоваров.Остатки КАК ОстаткиТоваровОстатки")
    fields = [
        dcs.field('Товар', 'Товар'),
        dcs.field('Склад', 'Склад'),
        dcs.field('КоличествоОстаток', 'КоличествоОстаток'),
    ]
    variant = dcs.variant_details(
        'Основной', 'Основной',
        ['Товар', 'Склад', 'КоличествоОстаток'],
        filters=[('Склад', 'Equal', u(), 'Склад'),
                 ('Товар.ЦветТовара', 'Equal', u(), 'Цвет товара'),
                 ('Товар.СтранаТовара', 'Equal', u(), 'Страна товара')])
    schema = dcs.schema(q, fields,
                        totals=[('КоличествоОстаток', 'Сумма(КоличествоОстаток)')],
                        variants=[variant])
    report(out, 'ОстаткиТоваров', 'Остатки товаров', schema)

    # --- обработки (задания 3+) ---
    if level >= 3:
        gen_obrabotki.build(out, level)

    # --- первый запуск (задание 8) ---
    if level >= 8:
        gen_pervyzapusk.build(out)

    # --- подсистемы (задание 2) ---
    subsystem(out, 'Справочники', 'Справочники', [
        'Catalog.Товары', 'Catalog.Склады', 'Catalog.ЦветаТоваров', 'Catalog.СтраныТоваров'])
    subsystem(out, 'УчетТоваров', 'Учёт товаров', [
        'Document.ПриходТоваров', 'Document.РасходТоваров', 'AccumulationRegister.ОстаткиТоваров'])
    subsystem(out, 'Отчеты', 'Отчёты', ['Report.ОстаткиТоваров'])
    if level >= 3:
        subsystem(out, 'Сервис', 'Сервис', ['DataProcessor.СервисныеОперации'])

    # --- конфигурация ---
    children = [
        '\t\t\t<Language>Русский</Language>',
        '\t\t\t<Subsystem>Справочники</Subsystem>',
        '\t\t\t<Subsystem>УчетТоваров</Subsystem>',
        '\t\t\t<Subsystem>Отчеты</Subsystem>',
    ] + (['\t\t\t<Subsystem>Сервис</Subsystem>'] if level >= 3 else []) + [
        '\t\t\t<Catalog>ЦветаТоваров</Catalog>',
        '\t\t\t<Catalog>СтраныТоваров</Catalog>',
        '\t\t\t<Catalog>Склады</Catalog>',
        '\t\t\t<Catalog>Товары</Catalog>',
        '\t\t\t<Document>ПриходТоваров</Document>',
        '\t\t\t<Document>РасходТоваров</Document>',
        '\t\t\t<AccumulationRegister>ОстаткиТоваров</AccumulationRegister>',
        '\t\t\t<Report>ОстаткиТоваров</Report>',
    ] + (['\t\t\t<DataProcessor>СервисныеОперации</DataProcessor>'] if level >= 3 else []) + (
        ['\t\t\t<Constant>ПервыйЗапускОсуществлен</Constant>',
         '\t\t\t<CommonModule>ПервыйЗапускСервер</CommonModule>',
         '\t\t\t<CommonForm>ФормаПервогоЗапуска</CommonForm>'] if level >= 8 else []) + [
    ]
    cfg = [
        '\t<Configuration uuid="%s">' % u(),
        cfg_internal_info(),
        '\t\t<Properties>',
        '\t\t\t<Name>ПростойСклад</Name>',
        syn('Простой склад'),
        '\t\t\t<Comment/>',
        '\t\t\t<DefaultRunMode>ManagedApplication</DefaultRunMode>',
        '\t\t\t<ScriptVariant>Russian</ScriptVariant>',
        '\t\t\t<DefaultLanguage>Language.Русский</DefaultLanguage>',
        '\t\t\t<CompatibilityMode>Version8_3_23</CompatibilityMode>',
        '\t\t\t<ConfigurationExtensionCompatibilityMode>Version8_3_23</ConfigurationExtensionCompatibilityMode>',
        '\t\t\t<ModalityUseMode>DontUse</ModalityUseMode>',
        '\t\t\t<SynchronousPlatformExtensionAndAddInCallUseMode>DontUse</SynchronousPlatformExtensionAndAddInCallUseMode>',
        '\t\t\t<InterfaceCompatibilityMode>Taxi</InterfaceCompatibilityMode>',
        '\t\t\t<DataLockControlMode>Managed</DataLockControlMode>',
        '\t\t</Properties>',
        '\t\t<ChildObjects>',
    ] + children + [
        '\t\t</ChildObjects>',
        '\t</Configuration>',
    ]
    write(os.path.join(out, 'Configuration.xml'), '\n'.join(cfg))

    lang = [
        '\t<Language uuid="%s">' % u(),
        '\t\t<Properties>',
        '\t\t\t<Name>Русский</Name>',
        syn('Русский'),
        '\t\t\t<Comment/>',
        '\t\t\t<LanguageCode>ru</LanguageCode>',
        '\t\t</Properties>',
        '\t</Language>',
    ]
    write(os.path.join(out, 'Languages', 'Русский.xml'), '\n'.join(lang))
    print('generated ->', out)


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '_build', 'sklad-src')
    lvl = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    build(target, lvl)
