percept = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 0, 8]
]
rules = {
    "UP": "MOVE UP",
    "DOWN": "MOVE DOWN",
    "LEFT": "MOVE LEFT",
    "RIGHT": "MOVE RIGHT"
}
def interpret_input(percept):
    for i in range(3):
        for j in range(3):
            if percept[i][j] == 0:
                return (i, j)
def rule_match(state, rules):
    x, y = state
    if x > 0:
        return "UP"
    elif x < 2:
        return "DOWN"
    elif y > 0:
        return "LEFT"
    else:
        return "RIGHT"
def simple_reflex_agent(percept):
    state = interpret_input(percept)
    rule = rule_match(state, rules)
    action = rules[rule]
    return action
result = simple_reflex_agent(percept)
print(result)