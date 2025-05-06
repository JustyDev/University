object Form1: TForm1
  Left = 0
  Top = 0
  Caption = 'Form1'
  ClientHeight = 441
  ClientWidth = 624
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = 'Segoe UI'
  Font.Style = []
  OnCreate = FormCreate
  TextHeight = 15
  object LabeledEdit1: TLabeledEdit
    Left = 8
    Top = 24
    Width = 193
    Height = 23
    EditLabel.Width = 128
    EditLabel.Height = 15
    EditLabel.Caption = #1057#1077#1088#1074#1077#1088' '#1089#1080#1085#1093#1088#1086#1085#1080#1079#1072#1094#1080#1080
    TabOrder = 0
    Text = 'time.nist.gov'
  end
  object Button1: TButton
    Left = 8
    Top = 64
    Width = 193
    Height = 25
    Caption = 'Button1'
    TabOrder = 1
    OnClick = Button1Click
  end
  object LabeledEdit2: TLabeledEdit
    Left = 8
    Top = 144
    Width = 193
    Height = 23
    EditLabel.Width = 25
    EditLabel.Height = 15
    EditLabel.Caption = #1044#1072#1090#1072
    TabOrder = 2
    Text = ''
  end
  object LabeledEdit3: TLabeledEdit
    Left = 8
    Top = 192
    Width = 193
    Height = 23
    EditLabel.Width = 35
    EditLabel.Height = 15
    EditLabel.Caption = #1042#1088#1077#1084#1103
    TabOrder = 3
    Text = ''
  end
  object Button2: TButton
    Left = 8
    Top = 232
    Width = 193
    Height = 25
    Caption = #1057#1080#1085#1093#1088#1086#1085#1080#1079#1080#1088#1086#1074#1072#1090#1100
    TabOrder = 4
    OnClick = Button2Click
  end
  object RichEdit1: TRichEdit
    Left = 431
    Top = 344
    Width = 185
    Height = 89
    Font.Charset = RUSSIAN_CHARSET
    Font.Color = clWindowText
    Font.Height = -12
    Font.Name = 'Segoe UI'
    Font.Style = []
    Lines.Strings = (
      'RichEdit1')
    ParentFont = False
    TabOrder = 5
  end
  object IdTime1: TIdTime
    BaseDate = 2.000000000000000000
    Left = 232
    Top = 24
  end
  object Timer1: TTimer
    OnTimer = Timer1Timer
    Left = 296
    Top = 24
  end
end
