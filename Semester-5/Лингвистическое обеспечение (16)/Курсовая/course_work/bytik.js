const fs = require("fs");
const { spawnSync } = require("child_process");
const path = require("path");

const INPUT_FUNC = '__baytik_input';

function error(msg, line = null) {
    if (line !== null) {
        console.error(`Ошибка компиляции: ${msg} (строка ${line+1})`);
    } else {
        console.error(`Ошибка компиляции: ${msg}`);
    }
    process.exit(1);
}

const TYPES = ['целое', 'вещественное', 'дата'];

const INPUT_JS = `
function ${INPUT_FUNC}(msg) {
    const readline = require('readline-sync');
    if (msg) process.stdout.write(msg + " ");
    let value = readline.question('');
    return value;
}
`;

function tokenize(line) {
    return line.match(/("[^"]*"|\S+)/g) || [];
}

// ------ ФУНКЦИЯ ИЗВЛЕЧЕНИЯ ПЕРЕМЕННЫХ ИЗ ВЫРАЖЕНИЯ ---------
function extractVariables(expr) {
    // Удаляем строковые литералы и всё в кавычках
    let cleaned = expr.replace(/"[^"]*"/g, '');
    // Находим все возможные идентификаторы (буквы, цифры, подчёркивание)
    // Используем (?<![a-zA-Zа-яА-ЯёЁ0-9_]) вместо \b для корректной работы с кириллицей
    let matches = cleaned.match(/(?<![a-zA-Zа-яА-ЯёЁ0-9_])[a-zA-Zа-яА-ЯёЁ_][a-zA-Zа-яА-ЯёЁ0-9_]*(?![a-zA-Zа-яА-ЯёЁ0-9_])/g);
    if (!matches) return [];
    
    // Фильтруем JavaScript ключевые слова и встроенные функции
    const jsKeywords = new Set([
        'if', 'else', 'while', 'for', 'function', 'return', 'var', 'let', 'const',
        'parseInt', 'parseFloat', 'new', 'Date', 'split', 'getTime', 'getDate', 
        'getMonth', 'getFullYear', 'console', 'log', 'true', 'false', 'null', 'undefined'
    ]);
    
    return [...new Set(matches.filter(v => !jsKeywords.has(v)))];
}

// ------ ФУНКЦИЯ ПРОВЕРКИ ПЕРЕМЕННЫХ ---------
function checkVariables(expr, vars, line) {
    const variables = extractVariables(expr);
    for (let varName of variables) {
        if (!vars[varName]) {
            error(`Переменная "${varName}" не объявлена`, line);
        }
    }
}

// ------ ГЛАВНАЯ ФУНКЦИЯ ОБРАБОТКИ УСЛОВИЙ ---------
function parseCondition(cond) {
    // 1. Заменить все "ИЛИ" на || (с пробелами, регистр не важен)
    cond = cond.replace(/\bИЛИ\b/gi, '||');
    // 2. Заменить все "И" на && (всегда после "ИЛИ", чтобы не было совпадения внутри "ИЛИ"!)
    cond = cond.replace(/\bИ\b/gi, '&&');
    // 3. Заменить все "<>" на "!="
    cond = cond.replace(/<>/g, '!=');
    // 4. Заменить все случаи "=", которые не "==" и не "!=" на "=="
    // Для этого заменяем "=" на "==", если оно не предшествуется "!" или "="
    // Работает только если нет другого оператора перед "="
    cond = cond.replace(/([^=!<>])=([^=])/g, '$1==$2');
    // Также обрабатываем случай в начале строки
    cond = cond.replace(/^=([^=])/g, '==$1');
    return cond;
}

function transpile(filename) {
    const src = fs.readFileSync(filename, "utf-8").replace(/\r/g, '').split('\n');
    let jsCode = [INPUT_JS];
    let vars = {};
    let indentStack = [];
    let i = 0;

    while (i < src.length) {
        let raw = src[i];
        let line = raw.trim();

        if (!line || line.startsWith('//')) { i++; continue; }

        let tokens = tokenize(line);
        if (tokens.length === 0) { i++; continue; }

        // Описание переменной
        if (TYPES.includes(tokens[0])) {
            let type = tokens[0];
            let name = tokens[1]?.replace(/;/g, '');
            if (!name) error('Ожидалось имя переменной', i);
            if (!/^\d*([a-zA-Zа-яА-ЯёЁ_][\wа-яА-ЯёЁ]*)$/i.test(name)) error('Некорректное имя переменной', i);
            if (vars[name]) error(`Повторное объявление переменной ${name}`, i);

            let def;
            if (type === 'целое' || type === 'вещественное') def = '0';
            else if (type === 'дата') def = 'null';
            else def = 'undefined';
            vars[name] = type;
            jsCode.push(`let ${name} = ${def};`);
            i++; continue;
        }

        // -- Ввод
        if (tokens[0] === 'ввод') {
            let name = tokens[1]?.replace(/;/g, '');
            if (!vars[name]) error(`Не объявлена переменная ${name}`, i);

            let js = `${name} = ${INPUT_FUNC}();`;
            if (vars[name] === 'целое') js = `${name} = parseInt(${INPUT_FUNC}(), 10);`;
            if (vars[name] === 'вещественное') js = `${name} = parseFloat(${INPUT_FUNC}());`;
            jsCode.push(js);
            i++; continue;
        }

        // -- Вывод (fix ; in print)
        if (tokens[0] === 'вывод') {
            let args = line.slice(6).trim();
            if (args.endsWith(';')) args = args.slice(0, -1).trim();
            checkVariables(args, vars, i);
            jsCode.push(`console.log(${args});`);
            i++; continue;
        }

        // -- Если
        if (tokens[0] === 'если') {
            let cond = line.slice(4).trim();
            if (cond.endsWith(';')) cond = cond.slice(0, -1).trim();
            checkVariables(cond, vars, i);
            cond = parseCondition(cond);
            jsCode.push(`if (${cond}) {`);
            indentStack.push('если');
            i++; continue;
        }
        // -- Иначе
        if (tokens[0] === 'иначе') {
            jsCode.push(`} else {`);
            i++; continue;
        }
        // -- Конецесли
        if (tokens[0] === 'конецесли') {
            jsCode.push(`}`);
            indentStack.pop();
            i++; continue;
        }

        // -- Пока
        if (tokens[0] === 'пока') {
            let cond = line.slice(4).trim();
            if (/делать$/.test(cond)) cond = cond.replace(/делать$/, '').trim();
            if (cond.endsWith(';')) cond = cond.slice(0, -1).trim();
            checkVariables(cond, vars, i);
            cond = parseCondition(cond);
            jsCode.push(`while (${cond}) {`);
            indentStack.push('пока');
            i++;
            // Если следующая строка — только "делать", её пропускаем:
            if (src[i]?.trim() === "делать") i++;
            continue;
        }
        // -- Конецпока
        if (tokens[0] === 'конецпока') {
            jsCode.push(`}`);
            indentStack.pop();
            i++; continue;
        }

        // -- Присваивание
        if (/=/g.test(line)) {
            // просто присваивание, не условие!
            let parts = line.split("=");
            if (parts.length < 2) error('Ошибка присваивания', i);
            let name = parts[0].trim();
            let expr = parts.slice(1).join("=").trim().replace(/;/g, '');
            if (!vars[name]) error(`Не объявлена переменная ${name}`, i);
            checkVariables(expr, vars, i);
            jsCode.push(`${name} = ${expr};`);
            i++; continue;
        }

        error('Неизвестная конструкция: ' + line, i);
    }

    return jsCode.join('\n');
}

// === Главная точка входа ===
if (process.argv.length < 3) {
    console.log("Использование: node baytik.js <имя_файла.бт>");
    process.exit(0);
}
const input = process.argv[2];

try {
    const js = transpile(input);
    fs.writeFileSync('out.js', js, 'utf8');

    // Запускаем out.js 
    console.log("Компиляция успешно завершена. Запуск программы...\n");

    const res = spawnSync('node', [path.resolve('out.js')], { stdio: 'inherit' });

    if (res.error) {
        console.error("Ошибка исполнения программы:");
        console.error(res.error);
    }
    // Опционально: fs.unlinkSync('out.js');
} catch (e) {
    console.error(e.message);
    process.exit(1);
}
