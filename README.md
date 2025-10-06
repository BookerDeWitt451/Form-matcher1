# Form Template Matcher (TinyDB, CLI)

## Кратко
CLI-утилита `app.py` ищет подходящий шаблон формы по типам присланных полей.

Типы: email, phone, date, text. Порядок определения: date → phone → email → text.

Телефон: +7 XXX XXX XX XX  |  Дата: DD.MM.YYYY или YYYY-MM-DD.

## Установка
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск
```
python app.py get_tpl --customer="John Smith" --дата_заказа=27.05.2025 --order_id=AB12 --contact="+7 903 123 45 78"
```
Ожидаемый вывод: `Форма заказа`

## Тест
```
pytest -q
```
## Структура
app.py, core.py, db/templates.json, tests/, scripts/run_examples.sh
