import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'package:dbcrypt/dbcrypt.dart';

class DatabaseHelper {
  static final DatabaseHelper instance = DatabaseHelper._init();
  static Database? _database;

  DatabaseHelper._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('users.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(
      path,
      version: 1,
      onCreate: _createDB,
    );
  }

  Future _createDB(Database db, int version) async {
    await db.execute('''
      CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
      )
    ''');
  }

  Future<bool> registerUser(String login, String password) async {
    final db = await instance.database;

    // Проверка существует ли пользователь
    final existingUser = await db.query(
      'users',
      where: 'login = ?',
      whereArgs: [login],
    );

    if (existingUser.isNotEmpty) {
      return false;
    }

    // Хеширование пароля с помощью bcrypt
    final hashedPassword = DBCrypt().hashpw(password, DBCrypt().gensalt());

    await db.insert('users', {
      'login': login,
      'password': hashedPassword,
    });

    return true;
  }

  Future<bool> loginUser(String login, String password) async {
    final db = await instance.database;

    final result = await db.query(
      'users',
      where: 'login = ?',
      whereArgs: [login],
    );

    if (result.isEmpty) {
      return false;
    }

    final storedPassword = result.first['password'] as String;

    // Проверка пароля с помощью bcrypt
    return DBCrypt().checkpw(password, storedPassword);
  }

  Future close() async {
    final db = await instance.database;
    db.close();
  }
}
