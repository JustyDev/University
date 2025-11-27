import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/user_model.dart';

class YandexAuthService {
  // ВАЖНО: Замените эти значения на ваши реальные данные из Яндекс OAuth
  static const String clientId = 'd76edfd3df6e4af6b6fe970e881c8ecc'; // Получите на https://oauth.yandex.ru
  static const String clientSecret = '360fa873cc944f2eb192393a261c13c2';
  static const String redirectUri = 'lab3app://oauth';
  
  static const String authorizationEndpoint = 'https://oauth.yandex.ru/authorize';
  static const String tokenEndpoint = 'https://oauth.yandex.ru/token';
  static const String userInfoEndpoint = 'https://login.yandex.ru/info';
  
  static const String _accessTokenKey = 'access_token';
  static const String _refreshTokenKey = 'refresh_token';
  static const String _userDataKey = 'user_data';

  Future<void> startAuthorization() async {
    final authUrl = Uri.parse(authorizationEndpoint).replace(queryParameters: {
      'response_type': 'code',
      'client_id': clientId,
      'redirect_uri': redirectUri,
      'force_confirm': 'yes',
    });

    if (await canLaunchUrl(authUrl)) {
      await launchUrl(
        authUrl,
        mode: LaunchMode.externalApplication,
      );
    } else {
      throw Exception('Не удалось открыть страницу авторизации');
    }
  }

  Future<UserModel?> handleAuthorizationCode(String code) async {
    try {
      final response = await http.post(
        Uri.parse(tokenEndpoint),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'grant_type': 'authorization_code',
          'code': code,
          'client_id': clientId,
          'client_secret': clientSecret,
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final accessToken = data['access_token'];
        final refreshToken = data['refresh_token'];

        await _saveTokens(accessToken, refreshToken);

        return await getUserInfo(accessToken);
      } else {
        throw Exception('Ошибка получения токена: ${response.body}');
      }
    } catch (e) {
      throw Exception('Ошибка авторизации: $e');
    }
  }

  Future<UserModel?> getUserInfo(String accessToken) async {
    try {
      final response = await http.get(
        Uri.parse(userInfoEndpoint),
        headers: {
          'Authorization': 'OAuth $accessToken',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(utf8.decode(response.bodyBytes));
        final user = UserModel.fromJson(data);
        await _saveUserData(user);
        return user;
      } else {
        throw Exception('Ошибка получения данных пользователя');
      }
    } catch (e) {
      throw Exception('Ошибка получения информации о пользователе: $e');
    }
  }

  Future<void> _saveTokens(String accessToken, String refreshToken) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_accessTokenKey, accessToken);
    await prefs.setString(_refreshTokenKey, refreshToken);
  }

  Future<void> _saveUserData(UserModel user) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_userDataKey, json.encode(user.toJson()));
  }

  Future<String?> getAccessToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_accessTokenKey);
  }

  Future<UserModel?> getSavedUser() async {
    final prefs = await SharedPreferences.getInstance();
    final userData = prefs.getString(_userDataKey);
    if (userData != null) {
      return UserModel.fromJson(json.decode(userData));
    }
    return null;
  }

  Future<bool> isLoggedIn() async {
    final token = await getAccessToken();
    return token != null;
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_accessTokenKey);
    await prefs.remove(_refreshTokenKey);
    await prefs.remove(_userDataKey);
  }
}
