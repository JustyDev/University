object Form1: TForm1
  Left = 0
  Top = 0
  Caption = #1040#1074#1090#1086#1076#1086#1088#1086#1075#1072' '#1082#1072#1082#1072#1103'-'#1090#1086
  ClientHeight = 551
  ClientWidth = 576
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = 'Segoe UI'
  Font.Style = []
  OnCreate = FormCreate
  OnPaint = FormPaint
  TextHeight = 15
  object GroupBox1: TGroupBox
    Left = 24
    Top = 32
    Width = 185
    Height = 191
    Caption = #1053#1072#1083#1080#1095#1085#1099#1077' '#1087#1083#1072#1090#1077#1078#1080
    TabOrder = 0
    object Button3: TButton
      Left = 24
      Top = 141
      Width = 137
      Height = 25
      Caption = #1042#1099#1088#1091#1095#1082#1072
      TabOrder = 0
      OnClick = Button3Click
    end
    object LabeledEdit1: TLabeledEdit
      Left = 24
      Top = 50
      Width = 137
      Height = 23
      EditLabel.Width = 97
      EditLabel.Height = 15
      EditLabel.Caption = #1055#1088#1086#1077#1093#1072#1083#1086' '#1084#1072#1096#1080#1085
      TabOrder = 1
      Text = ''
    end
  end
  object GroupBox2: TGroupBox
    Left = 232
    Top = 32
    Width = 177
    Height = 191
    Caption = #1041#1077#1079#1085#1072#1083#1080#1095#1085#1099#1077' '#1087#1083#1072#1090#1077#1078#1080
    TabOrder = 1
    object Button4: TButton
      Left = 24
      Top = 141
      Width = 129
      Height = 25
      Caption = #1042#1099#1088#1091#1095#1082#1072
      TabOrder = 0
      OnClick = Button4Click
    end
    object LabeledEdit2: TLabeledEdit
      Left = 24
      Top = 50
      Width = 129
      Height = 23
      EditLabel.Width = 97
      EditLabel.Height = 15
      EditLabel.Caption = #1055#1088#1086#1077#1093#1072#1083#1086' '#1084#1072#1096#1080#1085
      TabOrder = 1
      Text = ''
    end
  end
  object Button5: TButton
    Left = 24
    Top = 280
    Width = 385
    Height = 25
    Caption = #1055#1086#1089#1084#1086#1090#1088#1077#1090#1100' '#1086#1073#1097#1091#1102' '#1074#1099#1088#1091#1095#1082#1091
    TabOrder = 2
    OnClick = Button5Click
  end
  object RandomButton: TButton
    Left = 24
    Top = 240
    Width = 385
    Height = 25
    Caption = #1053#1072#1095#1072#1090#1100' '#1089#1080#1084#1091#1083#1103#1094#1080#1102
    TabOrder = 3
    OnClick = RandomButtonClick
  end
  object AnimationTimer: TTimer
    Enabled = False
    Interval = 30
    OnTimer = AnimationTimerTimer
    Left = 448
    Top = 24
  end
  object RandomCarTimer: TTimer
    Enabled = False
    OnTimer = RandomCarTimerTimer
    Left = 528
    Top = 24
  end
end
