object Form1: TForm1
  Left = 0
  Top = 0
  Caption = #1051#1072#1073#1086#1088#1072#1090#1086#1088#1085#1072#1103' 10'
  ClientHeight = 638
  ClientWidth = 491
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = 'Segoe UI'
  Font.Style = []
  OnCreate = FormCreate
  TextHeight = 15
  object GroupBox1: TGroupBox
    Left = 8
    Top = 24
    Width = 220
    Height = 338
    Caption = #1055#1088#1086#1076#1091#1082#1090#1086#1074#1099#1081' '#1090#1086#1074#1072#1088
    TabOrder = 0
    object Button1: TButton
      Left = 117
      Top = 296
      Width = 93
      Height = 25
      Caption = #1044#1086#1073#1072#1074#1080#1090#1100
      TabOrder = 0
      OnClick = Button1Click
    end
    object LabeledEdit1: TLabeledEdit
      Left = 10
      Top = 48
      Width = 200
      Height = 23
      EditLabel.Width = 83
      EditLabel.Height = 15
      EditLabel.Caption = #1053#1072#1080#1084#1077#1085#1086#1074#1072#1085#1080#1077
      TabOrder = 1
      Text = ''
    end
    object LabeledEdit2: TLabeledEdit
      Left = 10
      Top = 96
      Width = 200
      Height = 23
      EditLabel.Width = 38
      EditLabel.Height = 15
      EditLabel.Caption = #1053#1086#1084#1077#1088
      TabOrder = 2
      Text = ''
    end
    object LabeledEdit3: TLabeledEdit
      Left = 10
      Top = 145
      Width = 200
      Height = 23
      EditLabel.Width = 62
      EditLabel.Height = 15
      EditLabel.Caption = #1062#1077#1085#1072' ('#1088#1091#1073'.)'
      TabOrder = 3
      Text = ''
    end
    object LabeledEdit4: TLabeledEdit
      Left = 10
      Top = 200
      Width = 200
      Height = 23
      EditLabel.Width = 109
      EditLabel.Height = 15
      EditLabel.Caption = #1057#1088#1086#1082' '#1093#1088#1072#1085#1077#1085#1080#1103' ('#1076#1085'.)'
      TabOrder = 4
      Text = ''
    end
    object LabeledEdit5: TLabeledEdit
      Left = 10
      Top = 250
      Width = 200
      Height = 23
      EditLabel.Width = 152
      EditLabel.Height = 15
      EditLabel.Caption = #1058#1077#1084#1087#1077#1088#1072#1090#1091#1088#1072' '#1093#1088#1072#1085#1077#1085#1080#1103' ('#1075#1088'.)'
      TabOrder = 5
      Text = ''
    end
  end
  object GroupBox2: TGroupBox
    Left = 256
    Top = 24
    Width = 220
    Height = 233
    Caption = #1055#1088#1086#1084#1099#1096#1083#1077#1085#1085#1099#1081' '#1090#1086#1074#1072#1088
    TabOrder = 1
    object Button2: TButton
      Left = 116
      Top = 184
      Width = 93
      Height = 25
      Caption = #1044#1086#1073#1072#1074#1080#1090#1100
      TabOrder = 0
      OnClick = Button2Click
    end
    object LabeledEdit6: TLabeledEdit
      Left = 10
      Top = 48
      Width = 200
      Height = 23
      EditLabel.Width = 83
      EditLabel.Height = 15
      EditLabel.Caption = #1053#1072#1080#1084#1077#1085#1086#1074#1072#1085#1080#1077
      TabOrder = 1
      Text = ''
    end
    object LabeledEdit7: TLabeledEdit
      Left = 10
      Top = 96
      Width = 200
      Height = 23
      EditLabel.Width = 38
      EditLabel.Height = 15
      EditLabel.Caption = #1053#1086#1084#1077#1088
      TabOrder = 2
      Text = ''
    end
    object LabeledEdit8: TLabeledEdit
      Left = 10
      Top = 145
      Width = 200
      Height = 23
      EditLabel.Width = 62
      EditLabel.Height = 15
      EditLabel.Caption = #1062#1077#1085#1072' ('#1088#1091#1073'.)'
      TabOrder = 3
      Text = ''
    end
  end
  object StringGrid1: TStringGrid
    Left = 8
    Top = 384
    Width = 468
    Height = 177
    TabOrder = 2
  end
  object Button3: TButton
    Left = 8
    Top = 583
    Width = 169
    Height = 26
    Caption = #1054#1073#1097#1072#1103' '#1089#1090#1086#1080#1084#1086#1089#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 3
    OnClick = Button3Click
  end
  object Button4: TButton
    Left = 196
    Top = 583
    Width = 113
    Height = 26
    Caption = #1057#1086#1093#1088#1072#1085#1080#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 4
    OnClick = Button4Click
  end
  object Button5: TButton
    Left = 328
    Top = 583
    Width = 113
    Height = 26
    Caption = #1047#1072#1075#1088#1091#1079#1080#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 5
    OnClick = Button5Click
  end
  object OpenDialog1: TOpenDialog
    Left = 304
    Top = 304
  end
  object SaveDialog1: TSaveDialog
    Left = 408
    Top = 304
  end
end
