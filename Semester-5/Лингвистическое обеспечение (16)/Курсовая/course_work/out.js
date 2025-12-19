
function __baytik_input(msg) {
    const readline = require('readline-sync');
    if (msg) process.stdout.write(msg + " ");
    let value = readline.question('');
    return value;
}

let x = 0;
console.log("Введите целое число:");
x = parseInt(__baytik_input(), 10);
if (x % 2 == 0) {
console.log("Число чётное");
} else {
console.log("Число нечётное");
}