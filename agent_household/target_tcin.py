def is_target_tcin(value: object) -> bool:
    """Accept only exact strings containing exactly eight ASCII digits."""
    if type(value) is not str:
        return False
    if len(value) != 8:
        return False
    return all("0" <= character <= "9" for character in value)
