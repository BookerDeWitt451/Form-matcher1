from core import detect_type, match_template, pretty_inferred_types

def test_detect_type_order():
    assert detect_type("27.05.2025") == "date"
    assert detect_type("2025-05-27") == "date"
    assert detect_type("+7 903 123 45 78") == "phone"
    assert detect_type("user@example.com") == "email"
    assert detect_type("John Smith") == "text"

def test_match_template():
    templates = [
        {"name": "Проба", "f_name1": "email", "f_name2": "date"},
        {"name": "Данные пользователя", "login": "email", "tel": "phone"},
    ]
    provided1 = {"f_name1": "aaa@bbb.ru", "f_name2": "27.05.2025"}
    assert match_template(templates, provided1) == "Проба"

    provided2 = {"login": "vasya", "f_name1": "aaa@bbb.ru", "f_name2": "27.05.2025"}
    assert match_template(templates, provided2) == "Проба"

    provided3 = {"f_name1": "aaa@bbb.ru"}
    assert match_template(templates, provided3) is None

def test_pretty_inferred_types():
    out = pretty_inferred_types({"tumba":"27.05.2025","yumba":"+7 903 123 45 78"})
    assert "{\n  tumba: date,\n  yumba: phone\n}" == out
