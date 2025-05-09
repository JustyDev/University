object Form1: TForm1
  Left = 0
  Top = 0
  Caption = #1057#1080#1085#1093#1088#1086#1085#1080#1079#1072#1094#1080#1103' '#1074#1088#1077#1084#1077#1085#1080
  ClientHeight = 314
  ClientWidth = 343
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = 'Segoe UI'
  Font.Style = []
  TextHeight = 15
  object Image1: TImage
    Left = 8
    Top = 16
    Width = 137
    Height = 135
  end
  object btnConnect: TButton
    Left = 168
    Top = 69
    Width = 161
    Height = 28
    Caption = #1055#1086#1076#1082#1083#1102#1095#1080#1090#1100#1089#1103
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 0
    OnClick = btnConnectClick
  end
  object btnSynchronize: TButton
    Left = 168
    Top = 208
    Width = 161
    Height = 25
    Caption = #1057#1080#1085#1093#1088#1086#1085#1080#1079#1080#1088#1086#1074#1072#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 1
    OnClick = btnSynchronizeClick
  end
  object editNTP: TLabeledEdit
    Left = 168
    Top = 32
    Width = 161
    Height = 23
    EditLabel.Width = 153
    EditLabel.Height = 17
    EditLabel.Caption = #1057#1077#1088#1074#1077#1088' '#1090#1086#1095#1085#1086#1075#1086' '#1074#1088#1077#1084#1077#1085#1080
    EditLabel.Font.Charset = DEFAULT_CHARSET
    EditLabel.Font.Color = clWindowText
    EditLabel.Font.Height = -13
    EditLabel.Font.Name = 'Segoe UI'
    EditLabel.Font.Style = []
    EditLabel.ParentFont = False
    TabOrder = 2
    Text = 'time.nist.gov'
  end
  object editDate: TLabeledEdit
    Left = 168
    Top = 128
    Width = 161
    Height = 23
    EditLabel.Width = 28
    EditLabel.Height = 17
    EditLabel.Caption = #1044#1072#1090#1072
    EditLabel.Font.Charset = DEFAULT_CHARSET
    EditLabel.Font.Color = clWindowText
    EditLabel.Font.Height = -13
    EditLabel.Font.Name = 'Segoe UI'
    EditLabel.Font.Style = []
    EditLabel.ParentFont = False
    TabOrder = 3
    Text = ''
  end
  object editTime: TLabeledEdit
    Left = 168
    Top = 168
    Width = 161
    Height = 23
    EditLabel.Width = 38
    EditLabel.Height = 17
    EditLabel.Caption = #1042#1088#1077#1084#1103
    EditLabel.Font.Charset = DEFAULT_CHARSET
    EditLabel.Font.Color = clWindowText
    EditLabel.Font.Height = -13
    EditLabel.Font.Name = 'Segoe UI'
    EditLabel.Font.Style = []
    EditLabel.ParentFont = False
    TabOrder = 4
    Text = ''
  end
  object IdTime1: TIdTime
    BaseDate = 2.000000000000000000
    Left = 240
    Top = 248
  end
  object Timer1: TTimer
    OnTimer = Timer1Timer
    Left = 176
    Top = 248
  end
end
