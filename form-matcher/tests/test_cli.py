import subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

def run_cli(args):
    cmd = [sys.executable, str(ROOT / "app.py")] + args
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=ROOT)
    return res.returncode, res.stdout.strip(), res.stderr

def test_cli_match_template():
    code, out, err = run_cli(["get_tpl","--db","db/templates.json","--f_name1=vasya@pukin.ru","--f_name2=27.05.2025"])
    assert code == 0
    assert out == "Проба"

def test_cli_no_match_types_printed():
    code, out, err = run_cli(["get_tpl","--db","db/templates.json","--tumba=27.05.2025","--yumba=+7 903 123 45 78"])
    assert code == 0
    assert out == "{\n  tumba: date,\n  yumba: phone\n}"

def test_cli_extra_fields_still_match():
    code, out, err = run_cli(["get_tpl","--db","db/templates.json","--customer=John Smith","--дата_заказа=27.05.2025","--order_id=AB12","--contact=+7 903 123 45 78","--unused=hello"])
    assert code == 0
    assert out == "Форма заказа"
