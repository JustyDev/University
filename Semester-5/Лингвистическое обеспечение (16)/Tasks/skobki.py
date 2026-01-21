# - S -> SS
# - S -> (S)
# - S -> ε

def check_brackets(sequence):
    stack = []
    brackets = {')': '('}

    for char in sequence:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack or stack[-1] != brackets[char]:
                return False
            stack.pop()

    return not stack


# Пример использования:
sequence = "(())()()"
if check_brackets(sequence):
    print("Скобки расставлены правильно.")
else:
    print("Скобки расставлены неправильно.")
