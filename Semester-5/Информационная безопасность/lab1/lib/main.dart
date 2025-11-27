import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Шифр Атбаш',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const AtbashCipherPage(),
    );
  }
}

class AtbashCipherPage extends StatefulWidget {
  const AtbashCipherPage({super.key});

  @override
  State<AtbashCipherPage> createState() => _AtbashCipherPageState();
}

class _AtbashCipherPageState extends State<AtbashCipherPage> {
  final TextEditingController _inputController = TextEditingController();
  String _output = '';
  String _selectedAlphabet = 'russian'; // 'russian' or 'english'

  // Русский алфавит
  static const String _russianLower = 'абвгдежзийклмнопрстуфхцчшщъыьэюя';
  static const String _russianUpper = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';

  // Английский алфавит
  static const String _englishLower = 'abcdefghijklmnopqrstuvwxyz';
  static const String _englishUpper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

  String _applyAtbashCipher(String text) {
    if (text.isEmpty) return '';

    StringBuffer result = StringBuffer();

    for (int i = 0; i < text.length; i++) {
      String char = text[i];
      String? encrypted = _encryptChar(char);
      result.write(encrypted ?? char);
    }

    return result.toString();
  }

  String? _encryptChar(String char) {
    if (_selectedAlphabet == 'russian') {
      // Проверяем строчные русские буквы
      int index = _russianLower.indexOf(char);
      if (index != -1) {
        return _russianLower[_russianLower.length - 1 - index];
      }

      // Проверяем заглавные русские буквы
      index = _russianUpper.indexOf(char);
      if (index != -1) {
        return _russianUpper[_russianUpper.length - 1 - index];
      }
    } else {
      // Проверяем строчные английские буквы
      int index = _englishLower.indexOf(char);
      if (index != -1) {
        return _englishLower[_englishLower.length - 1 - index];
      }

      // Проверяем заглавные английские буквы
      index = _englishUpper.indexOf(char);
      if (index != -1) {
        return _englishUpper[_englishUpper.length - 1 - index];
      }
    }

    return null; // Возвращаем null для символов, которые не нужно шифровать
  }

  void _encrypt() {
    setState(() {
      _output = _applyAtbashCipher(_inputController.text);
    });
  }

  void _clear() {
    setState(() {
      _inputController.clear();
      _output = '';
    });
  }

  @override
  void dispose() {
    _inputController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('Шифр Атбаш'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Описание
            Card(
              child: Padding(
                padding: const EdgeInsets.all(12.0),
                child: Text(
                  'Шифр Атбаш: первая буква алфавита заменяется на последнюю, '
                  'вторая – на предпоследнюю и так далее.',
                  style: Theme.of(context).textTheme.bodyMedium,
                  textAlign: TextAlign.center,
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Выбор алфавита
            Text(
              'Выберите алфавит:',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: RadioListTile<String>(
                    title: const Text('Русский'),
                    value: 'russian',
                    groupValue: _selectedAlphabet,
                    onChanged: (value) {
                      setState(() {
                        _selectedAlphabet = value!;
                        if (_inputController.text.isNotEmpty) {
                          _encrypt();
                        }
                      });
                    },
                  ),
                ),
                Expanded(
                  child: RadioListTile<String>(
                    title: const Text('Английский'),
                    value: 'english',
                    groupValue: _selectedAlphabet,
                    onChanged: (value) {
                      setState(() {
                        _selectedAlphabet = value!;
                        if (_inputController.text.isNotEmpty) {
                          _encrypt();
                        }
                      });
                    },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),

            // Поле ввода
            Text(
              'Введите текст для шифрования:',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            TextField(
              controller: _inputController,
              maxLines: 5,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Введите текст...',
              ),
            ),
            const SizedBox(height: 20),

            // Кнопки
            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    onPressed: _encrypt,
                    icon: const Icon(Icons.lock),
                    label: const Text('Зашифровать'),
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: _clear,
                    icon: const Icon(Icons.clear),
                    label: const Text('Очистить'),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),

            // Поле вывода
            Text(
              'Результат:',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey),
                borderRadius: BorderRadius.circular(4),
                color: Colors.grey[100],
              ),
              constraints: const BoxConstraints(minHeight: 120),
              child: SelectableText(
                _output.isEmpty ? 'Зашифрованный текст появится здесь...' : _output,
                style: TextStyle(
                  fontSize: 16,
                  color: _output.isEmpty ? Colors.grey[600] : Colors.black,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
