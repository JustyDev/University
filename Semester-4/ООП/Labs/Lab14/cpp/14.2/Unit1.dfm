object Form1: TForm1
  Left = 0
  Top = 0
  BorderStyle = bsSingle
  Caption = #1051#1072#1073#1086#1088#1072#1090#1086#1088#1085#1072#1103' 14'
  ClientHeight = 490
  ClientWidth = 527
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = 'Segoe UI'
  Font.Style = []
  OnCreate = FormCreate
  TextHeight = 15
  object StringGrid1: TStringGrid
    Left = 8
    Top = 145
    Width = 493
    Height = 225
    TabOrder = 0
  end
  object ButtonAdd: TButton
    Left = 8
    Top = 64
    Width = 89
    Height = 25
    Caption = #1044#1086#1073#1072#1074#1080#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -13
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 1
    OnClick = ButtonAddClick
  end
  object ButtonSave: TButton
    Left = 104
    Top = 103
    Width = 89
    Height = 25
    Caption = #1057#1086#1093#1088#1072#1085#1080#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -13
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 2
    OnClick = ButtonSaveClick
  end
  object ButtonLoad: TButton
    Left = 104
    Top = 64
    Width = 89
    Height = 25
    Caption = #1047#1072#1075#1088#1091#1079#1080#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -13
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 3
    OnClick = ButtonLoadClick
  end
  object ButtonSortByName: TButton
    Left = 208
    Top = 64
    Width = 153
    Height = 25
    Caption = #1057#1086#1088#1090#1080#1088#1086#1074#1082#1072' '#1087#1086' '#1088#1077#1081#1089#1091
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -13
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 4
    OnClick = ButtonSortByNameClick
  end
  object ButtonSortByPrice: TButton
    Left = 208
    Top = 103
    Width = 153
    Height = 26
    Caption = #1057#1086#1088#1090#1080#1088#1086#1074#1082#1072' '#1087#1086' '#1094#1077#1085#1077
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -13
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 5
    OnClick = ButtonSortByPriceClick
  end
  object LE_Reis: TLabeledEdit
    Left = 10
    Top = 24
    Width = 183
    Height = 23
    EditLabel.Width = 26
    EditLabel.Height = 15
    EditLabel.Caption = #1056#1077#1081#1089
    TabOrder = 6
    Text = ''
  end
  object LE_Type: TLabeledEdit
    Left = 199
    Top = 24
    Width = 129
    Height = 23
    EditLabel.Width = 76
    EditLabel.Height = 15
    EditLabel.Caption = #1058#1080#1087' '#1089#1072#1084#1086#1083#1077#1090#1072
    TabOrder = 7
    Text = ''
  end
  object LE_Kol: TLabeledEdit
    Left = 334
    Top = 24
    Width = 167
    Height = 23
    EditLabel.Width = 87
    EditLabel.Height = 15
    EditLabel.Caption = #1050#1086#1083'-'#1074#1086' '#1073#1080#1083#1077#1090#1086#1074
    TabOrder = 8
    Text = ''
  end
  object LE_Price: TLabeledEdit
    Left = 380
    Top = 66
    Width = 121
    Height = 23
    EditLabel.Width = 69
    EditLabel.Height = 15
    EditLabel.Caption = #1062#1077#1085#1072' '#1073#1080#1083#1077#1090#1072
    TabOrder = 9
    Text = ''
  end
  object ButtonDeparture: TButton
    Left = 8
    Top = 392
    Width = 169
    Height = 25
    Caption = #1054#1095#1077#1088#1077#1076#1085#1086#1089#1090#1100' '#1074#1099#1083#1077#1090#1086#1074
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -13
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 10
    OnClick = ButtonDepartureClick
  end
  object DateTimePicker1: TDateTimePicker
    Left = 380
    Top = 103
    Width = 121
    Height = 23
    Date = 45768.000000000000000000
    Time = 0.026916736111161300
    TabOrder = 11
  end
  object OpenDialog1: TOpenDialog
    Left = 200
    Top = 392
  end
  object SaveDialog1: TSaveDialog
    Left = 280
    Top = 392
  end
end
