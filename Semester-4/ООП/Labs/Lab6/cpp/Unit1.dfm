object Form1: TForm1
  Left = 980
  Top = 607
  Caption = #1060#1086#1088#1084#1072
  ClientHeight = 231
  ClientWidth = 505
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  Position = poDesigned
  TextHeight = 13
  object Label1: TLabel
    Left = 24
    Top = 24
    Width = 81
    Height = 13
    Caption = #1042#1074#1077#1076#1080#1090#1077' '#1089#1090#1088#1086#1082#1091
  end
  object InputEdit: TEdit
    Left = 24
    Top = 48
    Width = 225
    Height = 21
    TabOrder = 0
  end
  object CTDtoATDButton: TButton
    Left = 24
    Top = 88
    Width = 105
    Height = 33
    Caption = 'CTD > ATD'
    TabOrder = 1
    OnClick = CTDtoATDButtonClick
  end
  object ATDtoCTDButton: TButton
    Left = 144
    Top = 88
    Width = 105
    Height = 33
    Caption = 'ATD > CTD'
    TabOrder = 2
    OnClick = ATDtoCTDButtonClick
  end
  object OutputMemo: TMemo
    Left = 272
    Top = 48
    Width = 209
    Height = 161
    TabOrder = 3
  end
end
