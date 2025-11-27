import 'package:flutter/material.dart';
import 'dart:async';
import 'package:uni_links/uni_links.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';
import 'services/yandex_auth_service.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Yandex Auth Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const SplashScreen(),
      routes: {
        '/login': (context) => const LoginScreen(),
        '/home': (context) => const HomeScreen(),
      },
    );
  }
}

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  final YandexAuthService _authService = YandexAuthService();
  StreamSubscription? _linkSubscription;

  @override
  void initState() {
    super.initState();
    _initializeApp();
    _initDeepLinks();
  }

  Future<void> _initializeApp() async {
    await Future.delayed(const Duration(seconds: 1));
    
    final isLoggedIn = await _authService.isLoggedIn();
    
    if (mounted) {
      if (isLoggedIn) {
        Navigator.of(context).pushReplacementNamed('/home');
      } else {
        Navigator.of(context).pushReplacementNamed('/login');
      }
    }
  }

  void _initDeepLinks() {
    // Обработка начального deep link (когда приложение открывается из ссылки)
    _handleInitialLink();
    
    // Подписка на входящие deep links (когда приложение уже открыто)
    _linkSubscription = uriLinkStream.listen((Uri? uri) {
      if (uri != null) {
        _handleDeepLink(uri);
      }
    }, onError: (err) {
      debugPrint('Deep link error: $err');
    });
  }

  Future<void> _handleInitialLink() async {
    try {
      final initialUri = await getInitialUri();
      if (initialUri != null) {
        _handleDeepLink(initialUri);
      }
    } catch (e) {
      debugPrint('Error handling initial link: $e');
    }
  }

  Future<void> _handleDeepLink(Uri uri) async {
    if (uri.scheme == 'lab3app' && uri.host == 'oauth') {
      final code = uri.queryParameters['code'];
      
      if (code != null) {
        try {
          // Показываем индикатор загрузки
          if (mounted) {
            showDialog(
              context: context,
              barrierDismissible: false,
              builder: (context) => const Center(
                child: CircularProgressIndicator(),
              ),
            );
          }

          // Обмениваем код на токен и получаем данные пользователя
          await _authService.handleAuthorizationCode(code);

          if (mounted) {
            // Закрываем индикатор загрузки
            Navigator.of(context).pop();
            
            // Переходим на главный экран
            Navigator.of(context).pushReplacementNamed('/home');
          }
        } catch (e) {
          if (mounted) {
            // Закрываем индикатор загрузки
            Navigator.of(context).pop();
            
            // Показываем ошибку
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Ошибка авторизации: $e'),
                backgroundColor: Colors.red,
              ),
            );
          }
        }
      }
    }
  }

  @override
  void dispose() {
    _linkSubscription?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Colors.blue.shade400,
              Colors.blue.shade800,
            ],
          ),
        ),
        child: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.lock_outline,
                size: 80,
                color: Colors.white,
              ),
              SizedBox(height: 24),
              CircularProgressIndicator(
                color: Colors.white,
              ),
              SizedBox(height: 16),
              Text(
                'Загрузка...',
                style: TextStyle(
                  fontSize: 18,
                  color: Colors.white,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
