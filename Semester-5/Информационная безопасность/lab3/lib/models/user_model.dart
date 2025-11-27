class UserModel {
  final String id;
  final String login;
  final String? firstName;
  final String? lastName;
  final String? displayName;
  final String? email;
  final String? avatarUrl;

  UserModel({
    required this.id,
    required this.login,
    this.firstName,
    this.lastName,
    this.displayName,
    this.email,
    this.avatarUrl,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'].toString(),
      login: json['login'] ?? '',
      firstName: json['first_name'],
      lastName: json['last_name'],
      displayName: json['display_name'] ?? json['real_name'],
      email: json['default_email'],
      avatarUrl: json['default_avatar_id'] != null
          ? 'https://avatars.yandex.net/get-yapic/${json['default_avatar_id']}/islands-200'
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'login': login,
      'first_name': firstName,
      'last_name': lastName,
      'display_name': displayName,
      'default_email': email,
      'avatar_url': avatarUrl,
    };
  }

  String get fullName {
    if (firstName != null && lastName != null) {
      return '$firstName $lastName';
    }
    return displayName ?? login;
  }
}
