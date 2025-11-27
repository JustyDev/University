import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Шифр Цезаря',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const CaesarCipherPage(),
    );
  }
}

class CaesarCipherPage extends StatefulWidget {
  const CaesarCipherPage({super.key});

  @override
  State<CaesarCipherPage> createState() => _CaesarCipherPageState();
}

class _CaesarCipherPageState extends State<CaesarCipherPage> {
  final TextEditingController _textController = TextEditingController();
  final TextEditingController _shiftController = TextEditingController();
  String _result = '';

  // Русский алфавит
  static const String _russianLower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя';
  static const String _russianUpper = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';
  
  // Английский алфавит
  static const String _englishLower = 'abcdefghijklmnopqrstuvwxyz';
  static const String _englishUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

  @override
  void dispose() {
    _textController.dispose();
    _shiftController.dispose();
    super.dispose();
  }

  String _caesarCipher(String text, int shift, bool encrypt) {
    if (text.isEmpty) return '';
    
    // Для дешифровки инвертируем сдвиг
    if (!encrypt) {
      shift = -shift;
    }

    StringBuffer result = StringBuffer();

    for (int i = 0; i < text.length; i++) {
      String char = text[i];
      String? shiftedChar = _shiftChar(char, shift);
      
      if (shiftedChar != null) {
        result.write(shiftedChar);
      } else {
        // Если символ не буква, оставляем его без изменений
        result.write(char);
      }
    }

    return result.toString();
  }

  String? _shiftChar(String char, int shift) {
    // Проверяем русские буквы
    if (_russianLower.contains(char)) {
      int index = _russianLower.indexOf(char);
      int newIndex = (index + shift) % _russianLower.length;
      if (newIndex < 0) newIndex += _russianLower.length;
      return _russianLower[newIndex];
    }
    
    if (_russianUpper.contains(char)) {
      int index = _russianUpper.indexOf(char);
      int newIndex = (index + shift) % _russianUpper.length;
      if (newIndex < 0) newIndex += _russianUpper.length;
      return _russianUpper[newIndex];
    }

    // Проверяем английские буквы
    if (_englishLower.contains(char)) {
      int index = _englishLower.indexOf(char);
      int newIndex = (index + shift) % _englishLower.length;
      if (newIndex < 0) newIndex += _englishLower.length;
      return _englishLower[newIndex];
    }
    
    if (_englishUpper.contains(char)) {
      int index = _englishUpper.indexOf(char);
      int newIndex = (index + shift) % _englishUpper.length;
      if (newIndex < 0) newIndex += _englishUpper.length;
      return _englishUpper[newIndex];
    }

    // Символ не является буквой
    return null;
  }

  void _encrypt() {
    final text = _textController.text;
    final shiftText = _shiftController.text;

    if (text.isEmpty) {
      _showError('Введите текст для шифрования');
      return;
    }

    if (shiftText.isEmpty) {
      _showError('Введите значение сдвига');
      return;
    }

    final shift = int.tryParse(shiftText);
    if (shift == null) {
      _showError('Сдвиг должен быть числом');
      return;
    }

    setState(() {
      _result = _caesarCipher(text, shift, true);
    });
  }

  void _decrypt() {
    final text = _textController.text;
    final shiftText = _shiftController.text;

    if (text.isEmpty) {
      _showError('Введите текст для дешифрования');
      return;
    }

    if (shiftText.isEmpty) {
      _showError('Введите значение сдвига');
      return;
    }

    final shift = int.tryParse(shiftText);
    if (shift == null) {
      _showError('Сдвиг должен быть числом');
      return;
    }

    setState(() {
      _result = _caesarCipher(text, shift, false);
    });
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
        duration: const Duration(seconds: 2),
      ),
    );
  }

  void _clear() {
    setState(() {
      _textController.clear();
      _shiftController.clear();
      _result = '';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Шифр Цезаря'),
        elevation: 2,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Введите текст:',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: _textController,
              maxLines: 4,
              decoration: InputDecoration(
                hintText: 'Например: Привет или Hello',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                filled: true,
                fillColor: Colors.grey[100],
              ),
            ),
            const SizedBox(height: 20),
            const Text(
              'Введите сдвиг:',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: _shiftController,
              keyboardType: TextInputType.number,
              inputFormatters: [
                FilteringTextInputFormatter.allow(RegExp(r'^-?\d*')),
              ],
              decoration: InputDecoration(
                hintText: 'Например: 3',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
                filled: true,
                fillColor: Colors.grey[100],
              ),
            ),
            const SizedBox(height: 24),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: _encrypt,
                    icon: const Icon(Icons.lock),
                    label: const Text('Зашифровать'),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      backgroundColor: Colors.deepPurple,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: _decrypt,
                    icon: const Icon(Icons.lock_open),
                    label: const Text('Дешифровать'),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      backgroundColor: Colors.teal,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: _clear,
              icon: const Icon(Icons.clear),
              label: const Text('Очистить'),
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
            ),
            const SizedBox(height: 24),
            const Text(
              'Результат:',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.blue[50],
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.blue[200]!),
              ),
              child: SelectableText(
                _result.isEmpty ? 'Здесь появится результат' : _result,
                style: TextStyle(
                  fontSize: 16,
                  color: _result.isEmpty ? Colors.grey[600] : Colors.black,
                ),
              ),
            ),
            const SizedBox(height: 24),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.amber[50],
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.amber[200]!),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'ℹ️ Информация:',
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    '• Поддерживаются русский и английский алфавиты\n'
                    '• Регистр букв сохраняется\n'
                    '• Пробелы и знаки препинания не изменяются\n'
                    '• Сдвиг может быть отрицательным',
                    style: TextStyle(fontSize: 13),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
