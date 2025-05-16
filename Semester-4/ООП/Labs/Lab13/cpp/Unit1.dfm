object Form1: TForm1
  Left = 0
  Top = 0
  BorderStyle = bsSingle
  Caption = 'Lab13'
  ClientHeight = 582
  ClientWidth = 571
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = 'Segoe UI'
  Font.Style = []
  TextHeight = 15
  object Label1: TLabel
    Left = 24
    Top = 33
    Width = 180
    Height = 20
    Caption = #1044#1072#1090#1072' '#1086#1090#1087#1088#1072#1074#1083#1077#1085#1080#1103' '#1087#1086#1077#1079#1076#1072
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -15
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
  end
  object Label2: TLabel
    Left = 24
    Top = 85
    Width = 193
    Height = 20
    Caption = #1042#1088#1077#1084#1103' '#1086#1090#1087#1088#1072#1074#1083#1077#1085#1080#1103' '#1087#1086#1077#1079#1076#1072
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -15
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
  end
  object Label3: TLabel
    Left = 24
    Top = 141
    Width = 127
    Height = 20
    Caption = #1055#1091#1085#1082#1090' '#1085#1072#1079#1085#1072#1095#1077#1085#1080#1103
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -15
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
  end
  object Label4: TLabel
    Left = 24
    Top = 196
    Width = 166
    Height = 20
    Caption = #1050#1086#1083'-'#1074#1086' '#1089#1074#1086#1073#1086#1076#1085#1099#1093' '#1084#1077#1089#1090
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -15
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
  end
  object StringGrid1: TStringGrid
    Left = 24
    Top = 296
    Width = 537
    Height = 201
    FixedCols = 0
    FixedRows = 0
    TabOrder = 0
  end
  object Button1: TButton
    Left = 24
    Top = 244
    Width = 121
    Height = 25
    Caption = #1044#1086#1073#1072#1074#1080#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -15
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 1
    OnClick = Button1Click
  end
  object Button2: TButton
    Left = 168
    Top = 244
    Width = 121
    Height = 25
    Caption = #1055#1086#1080#1089#1082
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -15
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 2
    OnClick = Button2Click
  end
  object Button3: TButton
    Left = 304
    Top = 244
    Width = 121
    Height = 25
    Caption = #1055#1086#1082#1072#1079#1072#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -15
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 3
    OnClick = Button3Click
  end
  object Button4: TButton
    Left = 440
    Top = 244
    Width = 121
    Height = 25
    Caption = #1054#1095#1080#1089#1090#1080#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -15
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 4
    OnClick = Button4Click
  end
  object Button5: TButton
    Left = 24
    Top = 520
    Width = 113
    Height = 25
    Caption = #1057#1086#1093#1088#1072#1085#1080#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -15
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 5
    OnClick = Button5Click
  end
  object Button6: TButton
    Left = 168
    Top = 520
    Width = 113
    Height = 25
    Caption = #1047#1072#1075#1088#1091#1079#1080#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -15
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 6
    OnClick = Button6Click
  end
  object datetrain: TDateTimePicker
    Left = 248
    Top = 28
    Width = 313
    Height = 23
    Date = 45764.000000000000000000
    Time = 0.887486944448028200
    TabOrder = 7
  end
  object timetrain: TDateTimePicker
    Left = 248
    Top = 82
    Width = 313
    Height = 23
    Date = 45764.000000000000000000
    Time = 0.887638333333598000
    DateMode = dmUpDown
    Kind = dtkTime
    TabOrder = 8
  end
  object Edit1: TEdit
    Left = 248
    Top = 138
    Width = 313
    Height = 23
    TabOrder = 9
  end
  object Edit2: TEdit
    Left = 248
    Top = 193
    Width = 313
    Height = 23
    TabOrder = 10
  end
  object OpenDialog1: TOpenDialog
    Left = 336
    Top = 504
  end
  object SaveDialog1: TSaveDialog
    Left = 456
    Top = 504
  end
end
