class Letter():
    BASE_LETTER = """
        Благодарим Ви, че се регистрирахте за Балкан Ултра. Очакваме ви на 06.08 2022.\n
        \n
        Име: {f}\n
        Фамилия: {l}\n
        Поща: {m}
    """

    ULTRA_LETTER = BASE_LETTER + """
        \n
        Линк 1: {fl}\n
        Линк 2: {sl}
    """

    SKY_LETTER = BASE_LETTER