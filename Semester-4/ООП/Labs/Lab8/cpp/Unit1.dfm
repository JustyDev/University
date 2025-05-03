object Form1: TForm1
  Left = 0
  Top = 0
  Caption = 'Form1'
  ClientHeight = 173
  ClientWidth = 333
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = 'Segoe UI'
  Font.Style = []
  TextHeight = 15
  object Button1: TButton
    Left = 152
    Top = 24
    Width = 75
    Height = 25
    Caption = '+'
    TabOrder = 0
    OnClick = Button1Click
  end
  object Button2: TButton
    Left = 248
    Top = 24
    Width = 75
    Height = 25
    Caption = '-'
    TabOrder = 1
    OnClick = Button2Click
  end
  object Button3: TButton
    Left = 152
    Top = 72
    Width = 75
    Height = 25
    Caption = '*'
    TabOrder = 2
    OnClick = Button3Click
  end
  object Button4: TButton
    Left = 248
    Top = 72
    Width = 75
    Height = 25
    Caption = '/'
    TabOrder = 3
    OnClick = Button4Click
  end
  object LabeledEdit1: TLabeledEdit
    Left = 8
    Top = 25
    Width = 121
    Height = 23
    EditLabel.Width = 78
    EditLabel.Height = 15
    EditLabel.Caption = #1055#1077#1088#1074#1086#1077' '#1095#1080#1089#1083#1086
    TabOrder = 4
    Text = ''
  end
  object LabeledEdit2: TLabeledEdit
    Left = 8
    Top = 73
    Width = 121
    Height = 23
    EditLabel.Width = 76
    EditLabel.Height = 15
    EditLabel.Caption = #1042#1090#1086#1088#1086#1077' '#1095#1080#1089#1083#1086
    TabOrder = 5
    Text = ''
  end
  object Panel1: TPanel
    Left = 8
    Top = 120
    Width = 315
    Height = 41
    TabOrder = 6
  end
end
