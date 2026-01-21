def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = []
    output = []
    tokens = expression.split()

    for token in tokens:
        if token.isnumeric():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while (stack and stack[-1] != '(' and
                   precedence.get(token, 0) <= precedence.get(stack[-1], 0)):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return ' '.join(output)


def evaluate_postfix(postfix_expression):
    stack = []
    tokens = postfix_expression.split()

    for token in tokens:
        if token.isnumeric():
            stack.append(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                result = a / b
            elif token == '^':
                result = a ** b
            stack.append(result)

    return stack[0]


def main():
    expression = "3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3"
    postfix_expression = infix_to_postfix(expression)
    result = evaluate_postfix(postfix_expression)
    print("Инфиксная запись:", expression)
    print("Постфиксная запись:", postfix_expression)
    print("Результат:", result)


if __name__ == "__main__":
    main()
