def test_phrase_length():

    s = str(input("Введите фразу менее 15 символов - "))
    assert len(s) < 15, "Фраза больше или равна 15 символов"