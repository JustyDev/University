import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

// Переменные для хранения учетных данных
String savedLogin = 'user123';
String savedPassword = 'Pass123!';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Авторизация',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const MainScreen(),
    );
  }
}

class MainScreen extends StatelessWidget {
  const MainScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Главная'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              'Выберите действие',
              style: TextStyle(fontSize: 24),
            ),
            const SizedBox(height: 40),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const LoginScreen()),
                );
              },
              child: const Text('Вход'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const RegisterScreen()),
                );
              },
              child: const Text('Регистрация'),
            ),
          ],
        ),
      ),
    );
  }
}

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final loginController = TextEditingController();
  final passwordController = TextEditingController();
  bool hidePassword = true;

  void checkLogin() {
    if (loginController.text == savedLogin && 
        passwordController.text == savedPassword) {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Успешно'),
          content: const Text('Вход выполнен'),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('ОК'),
            ),
          ],
        ),
      );
    } else {
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Ошибка'),
          content: const Text('Неверный логин или пароль'),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('ОК'),
            ),
          ],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Вход'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: loginController,
              decoration: const InputDecoration(
                labelText: 'Логин',
                hintText: 'Введите логин',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 20),
            TextField(
              controller: passwordController,
              obscureText: hidePassword,
              decoration: InputDecoration(
                labelText: 'Пароль',
                hintText: 'Введите пароль',
                border: const OutlineInputBorder(),
                suffixIcon: IconButton(
                  icon: Icon(hidePassword ? Icons.visibility : Icons.visibility_off),
                  onPressed: () {
                    setState(() {
                      hidePassword = !hidePassword;
                    });
                  },
                ),
              ),
            ),
            const SizedBox(height: 30),
            ElevatedButton(
              onPressed: checkLogin,
              child: const Text('Войти'),
            ),
          ],
        ),
      ),
    );
  }
}

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final loginController = TextEditingController();
  final passwordController = TextEditingController();
  final confirmPasswordController = TextEditingController();
  bool hidePassword = true;
  bool hideConfirmPassword = true;

  String? validatePassword(String password) {
    if (password.isEmpty) {
      return 'Поле не может быть пустым';
    }
    if (password.length < 8) {
      return 'Пароль должен быть не менее 8 символов';
    }
    
    // Проверка на наличие цифры
    if (!RegExp(r'\d').hasMatch(password)) {
      return 'Пароль должен содержать хотя бы 1 цифру';
    }
    
    // Проверка на наличие спецсимвола
    if (!RegExp(r'[!@#$%^&*(),.?":{}|<>]').hasMatch(password)) {
      return 'Пароль должен содержать хотя бы 1 спецсимвол';
    }
    
    return null;
  }

  void registerUser() {
    // Проверка что все поля заполнены
    if (loginController.text.isEmpty) {
      showError('Заполните поле Логин');
      return;
    }
    if (passwordController.text.isEmpty) {
      showError('Заполните поле Пароль');
      return;
    }
    if (confirmPasswordController.text.isEmpty) {
      showError('Заполните поле Подтверждение пароля');
      return;
    }

    // Валидация пароля
    String? passwordError = validatePassword(passwordController.text);
    if (passwordError != null) {
      showError(passwordError);
      return;
    }

    // Проверка совпадения паролей
    if (passwordController.text != confirmPasswordController.text) {
      showError('Пароли не совпадают');
      return;
    }

    // Сохраняем данные пользователя
    savedLogin = loginController.text;
    savedPassword = passwordController.text;

    // Если все проверки прошли
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Успешно'),
        content: const Text('Регистрация завершена'),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              Navigator.pop(context);
            },
            child: const Text('ОК'),
          ),
        ],
      ),
    );
  }

  void showError(String message) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Ошибка'),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('ОК'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Регистрация'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            TextField(
              controller: loginController,
              decoration: const InputDecoration(
                labelText: 'Логин',
                hintText: 'Введите логин',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 15),
            TextField(
              controller: passwordController,
              obscureText: hidePassword,
              decoration: InputDecoration(
                labelText: 'Пароль',
                hintText: 'Минимум 8 символов, 1 цифра, 1 спецсимвол',
                border: const OutlineInputBorder(),
                suffixIcon: IconButton(
                  icon: Icon(hidePassword ? Icons.visibility : Icons.visibility_off),
                  onPressed: () {
                    setState(() {
                      hidePassword = !hidePassword;
                    });
                  },
                ),
              ),
            ),
            const SizedBox(height: 15),
            TextField(
              controller: confirmPasswordController,
              obscureText: hideConfirmPassword,
              decoration: InputDecoration(
                labelText: 'Подтверждение пароля',
                hintText: 'Повторите пароль',
                border: const OutlineInputBorder(),
                suffixIcon: IconButton(
                  icon: Icon(hideConfirmPassword ? Icons.visibility : Icons.visibility_off),
                  onPressed: () {
                    setState(() {
                      hideConfirmPassword = !hideConfirmPassword;
                    });
                  },
                ),
              ),
            ),
            const SizedBox(height: 30),
            ElevatedButton(
              onPressed: registerUser,
              child: const Text('Зарегистрироваться'),
            ),
          ],
        ),
      ),
    );
  }
}
