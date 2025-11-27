import 'package:flutter/material.dart';
import 'dart:async';
import 'package:uni_links/uni_links.dart';
import '../services/yandex_auth_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final YandexAuthService _authService = YandexAuthService();
  StreamSubscription? _linkSubscription;
  bool _isProcessing = false;

  @override
  void initState() {
    super.initState();
    _initDeepLinks();
  }

  void _initDeepLinks() {
    // Обработка начального deep link
    _handleInitialLink();
    
    // Подписка на входящие deep links
    _linkSubscription = uriLinkStream.listen((Uri? uri) {
      if (uri != null && !_isProcessing) {
        _handleDeepLink(uri);
      }
    }, onError: (err) {
      debugPrint('Deep link error: $err');
    });
  }

  Future<void> _handleInitialLink() async {
    try {
      final initialUri = await getInitialUri();
      if (initialUri != null && !_isProcessing) {
        _handleDeepLink(initialUri);
      }
    } catch (e) {
      debugPrint('Error handling initial link: $e');
    }
  }

  Future<void> _handleDeepLink(Uri uri) async {
    debugPrint('Deep link received: $uri');
    
    if (uri.scheme == 'lab3app' && uri.host == 'oauth') {
      final code = uri.queryParameters['code'];
      
      if (code != null && !_isProcessing) {
        setState(() {
          _isProcessing = true;
        });

        try {
          debugPrint('Processing authorization code: $code');
          
          // Показываем индикатор загрузки
          if (mounted) {
            showDialog(
              context: context,
              barrierDismissible: false,
              builder: (context) => const Center(
                child: CircularProgressIndicator(color: Colors.white),
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
          debugPrint('Authorization error: $e');
          
          if (mounted) {
            // Закрываем индикатор загрузки
            Navigator.of(context).pop();
            
            // Показываем ошибку
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text('Ошибка авторизации: $e'),
                backgroundColor: Colors.red,
                duration: const Duration(seconds: 5),
              ),
            );
          }
        } finally {
          if (mounted) {
            setState(() {
              _isProcessing = false;
            });
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
        child: SafeArea(
          child: Center(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Логотип/иконка приложения
                  Container(
                    width: 120,
                    height: 120,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(30),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.2),
                          blurRadius: 20,
                          offset: const Offset(0, 10),
                        ),
                      ],
                    ),
                    child: Icon(
                      Icons.lock_outline,
                      size: 60,
                      color: Colors.blue.shade700,
                    ),
                  ),
                  const SizedBox(height: 40),
                  // Заголовок
                  const Text(
                    'Добро пожаловать',
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 12),
                  const Text(
                    'Войдите для продолжения',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.white70,
                    ),
                  ),
                  const SizedBox(height: 60),
                  // Кнопка входа через Яндекс
                  ElevatedButton(
                    onPressed: () async {
                      try {
                        await _authService.startAuthorization();
                      } catch (e) {
                        if (context.mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text('Ошибка: $e'),
                              backgroundColor: Colors.red,
                            ),
                          );
                        }
                      }
                    },
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      foregroundColor: Colors.black87,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 32,
                        vertical: 16,
                      ),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30),
                      ),
                      elevation: 8,
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Container(
                          width: 24,
                          height: 24,
                          decoration: BoxDecoration(
                            color: Colors.red,
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: const Center(
                            child: Text(
                              'Я',
                              style: TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                                fontSize: 16,
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 12),
                        const Text(
                          'Войти через Яндекс',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 40),
                  // Информационный текст
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Text(
                      'После нажатия на кнопку откроется страница авторизации Яндекс. После успешного входа вы будете автоматически перенаправлены обратно в приложение.',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.white70,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
