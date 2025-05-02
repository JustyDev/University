object Form1: TForm1
  Left = 0
  Top = 0
  Caption = #1057#1086#1088#1090#1080#1088#1086#1074#1082#1080
  ClientHeight = 445
  ClientWidth = 953
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = 'Segoe UI'
  Font.Style = []
  TextHeight = 15
  object GroupBox1: TGroupBox
    Left = 8
    Top = 16
    Width = 185
    Height = 417
    Caption = #1048#1089#1093#1086#1076#1085#1099#1081' '#1084#1072#1089#1089#1080#1074
    TabOrder = 0
    object Memo1: TMemo
      Left = 16
      Top = 32
      Width = 153
      Height = 321
      TabOrder = 0
    end
    object Button1: TButton
      Left = 16
      Top = 376
      Width = 153
      Height = 25
      Caption = #1057#1092#1086#1088#1084#1080#1088#1086#1074#1072#1090#1100
      TabOrder = 1
      OnClick = Button1Click
    end
  end
  object GroupBox2: TGroupBox
    Left = 407
    Top = 16
    Width = 194
    Height = 417
    Caption = #1054#1090#1089#1086#1088#1090#1080#1088#1086#1074#1072#1085#1085#1099#1081' '#1084#1072#1089#1089#1080#1074
    TabOrder = 1
    object Memo2: TMemo
      Left = 16
      Top = 24
      Width = 161
      Height = 329
      TabOrder = 0
    end
    object Button2: TButton
      Left = 14
      Top = 376
      Width = 163
      Height = 25
      Caption = #1054#1090#1089#1086#1088#1090#1080#1088#1086#1074#1072#1090#1100
      TabOrder = 1
      OnClick = Button2Click
    end
  end
  object Memo3: TMemo
    Left = 616
    Top = 20
    Width = 329
    Height = 381
    TabOrder = 2
  end
  object RadioGroup1: TRadioGroup
    Left = 208
    Top = 16
    Width = 185
    Height = 417
    Caption = #1057#1086#1088#1090#1080#1088#1086#1074#1082#1072':'
    Items.Strings = (
      #1055#1091#1079#1099#1088#1100#1082#1086#1074#1072#1103
      #1064#1077#1081#1082#1077#1088#1085#1072#1103
      #1056#1072#1089#1095#1105#1089#1082#1086#1081
      #1042#1089#1090#1072#1074#1082#1072#1084#1080
      #1042#1099#1073#1086#1088#1086#1084
      #1041#1099#1089#1090#1088#1072#1103
      #1057#1083#1080#1103#1085#1080#1077#1084
      #1055#1080#1088#1072#1084#1080#1076#1072#1083#1100#1085#1072#1103)
    TabOrder = 3
  end
  object ProgressBar1: TProgressBar
    Left = 616
    Top = 416
    Width = 329
    Height = 17
    Smooth = True
    TabOrder = 4
  end
end
