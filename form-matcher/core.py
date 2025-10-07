from __future__ import annotations
import re
from typing import Dict, List, Optional, Tuple, Any

DATE_PATTERNS = [
    re.compile(r"^(0?[1-9]|[12]\d|3[01])\.(0?[1-9]|1[0-2])\.(19|20)\d{2}$"),
    re.compile(r"^(19|20)\d{2}-(0?[1-9]|1[0-2])-(0?[1-9]|[12]\d|3[01])$"),
]

PHONE_PATTERN = re.compile(r"^\+7\s\d{3}\s\d{3}\s\d{2}\s\d{2}$")

EMAIL_PATTERN = re.compile(
    r"^(?=.{3,254}$)[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$"
)

def detect_type(value: str) -> str:
    v = value.strip()
    for pat in DATE_PATTERNS:
        if pat.match(v):
            return "date"
    if PHONE_PATTERN.match(v):
        return "phone"
    if EMAIL_PATTERN.match(v):
        return "email"
    return "text"


def normalize_template(tpl: Dict[str, Any]) -> Dict[str, Any]:
    if "name" not in tpl or not str(tpl["name"]).strip():
        raise ValueError("Template must contain non-empty 'name'")
    fixed = {}
    for k, v in tpl.items():
        if k == "name":
            fixed[k] = v
        else:
            tv = str(v).strip().lower()
            if tv not in {"email", "phone", "date", "text"}:
                raise ValueError(f"Unknown field type '{v}' in template '{tpl['name']}'")
            fixed[k] = tv
    return fixed


def match_template(templates: List[Dict[str, Any]], provided: Dict[str, str]) -> Optional[str]:
    detected = {k: detect_type(v) for k, v in provided.items()}
    candidates: List[Tuple[int, str]] = []
    for raw_tpl in templates:
        tpl = normalize_template(raw_tpl)
        name = tpl["name"]
        fields = {k: v for k, v in tpl.items() if k != "name"}
        ok = True
        for fk, ftype in fields.items():
            if fk not in detected or detected[fk] != ftype:
                ok = False
                break
        if ok:
            candidates.append((len(fields), name))
    if not candidates:
        return None
    candidates.sort(key=lambda x: (-x[0], x[1]))
    return candidates[0][1]


def pretty_inferred_types(provided: Dict[str, str]) -> str:
    lines = ["{"]
    keys = list(provided.keys())
    for i, k in enumerate(keys):
        t = detect_type(provided[k])
        comma = "," if i < len(keys) - 1 else ""
        lines.append(f"  {k}: {t}{comma}")
    lines.append("}")
    return "\n".join(lines)
