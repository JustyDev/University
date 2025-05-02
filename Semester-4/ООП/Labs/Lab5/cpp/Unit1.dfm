object Form1: TForm1
  Left = 0
  Top = 0
  Caption = #1055#1077#1088#1077#1075#1088#1091#1079#1086#1095#1082#1080
  ClientHeight = 270
  ClientWidth = 255
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -12
  Font.Name = 'Segoe UI'
  Font.Style = []
  TextHeight = 15
  object LabeledEdit1: TLabeledEdit
    Left = 8
    Top = 32
    Width = 113
    Height = 23
    EditLabel.Width = 57
    EditLabel.Height = 15
    EditLabel.Caption = '1-'#1077' '#1095#1080#1089#1083#1086':'
    TabOrder = 0
    Text = ''
    OnChange = LabeledEdit1Change
  end
  object LabeledEdit2: TLabeledEdit
    Left = 127
    Top = 32
    Width = 118
    Height = 23
    EditLabel.Width = 57
    EditLabel.Height = 15
    EditLabel.Caption = '2-'#1077' '#1095#1080#1089#1083#1086':'
    TabOrder = 1
    Text = ''
    OnChange = LabeledEdit2Change
  end
  object Button1: TButton
    Left = 8
    Top = 72
    Width = 75
    Height = 25
    Caption = '+'
    TabOrder = 2
    OnClick = Button1Click
  end
  object Button2: TButton
    Left = 89
    Top = 72
    Width = 75
    Height = 25
    Caption = '-'
    TabOrder = 3
    OnClick = Button2Click
  end
  object Button3: TButton
    Left = 170
    Top = 72
    Width = 75
    Height = 25
    Caption = '*'
    TabOrder = 4
    OnClick = Button3Click
  end
  object Button4: TButton
    Left = 8
    Top = 103
    Width = 75
    Height = 25
    Caption = '/'
    TabOrder = 5
    OnClick = Button4Click
  end
  object Button5: TButton
    Left = 89
    Top = 103
    Width = 75
    Height = 25
    Caption = '<'
    TabOrder = 6
    OnClick = Button5Click
  end
  object Button6: TButton
    Left = 170
    Top = 103
    Width = 75
    Height = 25
    Caption = '=='
    TabOrder = 7
    OnClick = Button6Click
  end
  object Memo1: TMemo
    Left = 8
    Top = 144
    Width = 237
    Height = 57
    TabOrder = 8
  end
  object Button7: TButton
    Left = 8
    Top = 216
    Width = 237
    Height = 25
    Caption = #1054#1095#1080#1089#1090#1080#1090#1100' '#1074#1099#1074#1086#1076
    TabOrder = 9
    OnClick = Button7Click
  end
end
