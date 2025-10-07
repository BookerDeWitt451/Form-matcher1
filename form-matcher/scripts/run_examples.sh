#!/usr/bin/env bash
set -euo pipefail
python3 app.py get_tpl --f_name1=vasya@pukin.ru --f_name2=27.05.2025
python3 app.py get_tpl --tumba=27.05.2025 --yumba="+7 903 123 45 78"
python3 app.py get_tpl --customer="John Smith" --дата_заказа=27.05.2025 --order_id=AB12 --contact="+7 903 123 45 78"
