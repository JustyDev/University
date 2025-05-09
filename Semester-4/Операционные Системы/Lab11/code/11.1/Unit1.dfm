object Form1: TForm1
  Left = 0
  Top = 0
  BorderStyle = bsSingle
  Caption = 'Lab11'
  ClientHeight = 389
  ClientWidth = 486
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = 'Segoe UI'
  Font.Style = []
  OnCreate = FormCreate
  OnDestroy = FormDestroy
  TextHeight = 15
  object Button1: TButton
    Left = 8
    Top = 352
    Width = 113
    Height = 25
    Caption = #1057#1074#1077#1088#1085#1091#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 0
    OnClick = Button1Click
  end
  object Button2: TButton
    Left = 136
    Top = 352
    Width = 113
    Height = 25
    Caption = #1047#1074#1077#1088#1096#1080#1090#1100
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clWindowText
    Font.Height = -16
    Font.Name = 'Segoe UI'
    Font.Style = []
    ParentFont = False
    TabOrder = 1
    OnClick = Button2Click
  end
  object ListBox1: TListBox
    Left = 8
    Top = 16
    Width = 470
    Height = 321
    ItemHeight = 15
    TabOrder = 2
  end
  object Timer1: TTimer
    Left = 280
    Top = 344
  end
end
