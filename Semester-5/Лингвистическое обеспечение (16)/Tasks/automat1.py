def nfa_to_dfa():
    # Определение автоматов: состояний, алфавита, начального и конечного состояний
    states = {'q0', 'q1', 'qf'}
    alphabet = {'(', ')'}
    start_state = 'q0'
    accept_state = {'qf'}

    # Переходы для НКА
    nfa_transitions = {
        ('q0', '('): {'q0'},
        ('q0', ')'): {'q1'},
        ('q1', ''): {'q0', 'qf'},
    }

    # Реализация переходов ДКА
    dfa_transitions = {}
    dfa_states = [frozenset(['q0'])]
    dfa_accept_states = set()

    while dfa_states:
        current_dfa_state = dfa_states.pop()
        if 'qf' in current_dfa_state:
            dfa_accept_states.add(current_dfa_state)

        for symbol in alphabet:
            next_states = set()
            for nfa_state in current_dfa_state:
                if (nfa_state, symbol) in nfa_transitions:
                    next_states.update(nfa_transitions[(nfa_state, symbol)])

            # Epsilon transitions
            epsilon_closures = set(next_states)
            for state in next_states:
                if (state, '') in nfa_transitions:
                    epsilon_closures.update(nfa_transitions[(state, '')])

            next_dfa_state = frozenset(epsilon_closures)
            if not next_dfa_state:
                continue

            dfa_transitions[(current_dfa_state, symbol)] = next_dfa_state
            if next_dfa_state not in dfa_accept_states and next_dfa_state not in dfa_states:
                dfa_states.append(next_dfa_state)

    return dfa_transitions, frozenset(['q0']), dfa_accept_states


def check_brackets_dfa(sequence, dfa_transitions, start_state, accept_states):
    current_state = start_state
    for char in sequence:
        if (current_state, char) in dfa_transitions:
            current_state = dfa_transitions[(current_state, char)]
        else:
            return False
    return current_state in accept_states


# Получаем ДКА
dfa_transitions, start_state, accept_states = nfa_to_dfa()

# Пример использования:
sequence = "(())()"
if check_brackets_dfa(sequence, dfa_transitions, start_state, accept_states):
    print("Скобки расставлены правильно.")
else:
    print("Скобки расставлены неправильно.")
