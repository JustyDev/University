
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = []
    output = []
    tokens = expression.split()

    for token in tokens:
        if token.isnumeric():  # Если токен - число, добавляем к выходной строке
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:  # оператор
            while (stack and stack[-1] != '(' and
                   precedence.get(token, 0) <= precedence.get(stack[-1], 0)):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return ' '.join(output)

# Пример использования:
expression = "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3"
postfix_expression = infix_to_postfix(expression)
print("Постфиксная запись:", postfix_expression)
