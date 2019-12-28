def findterminal(terminals: list, name: str) -> dict:
    for i in range(0, len(terminals)):
        current = terminals[i]
        if current["name"] == name:
            return terminals[i]
    return None