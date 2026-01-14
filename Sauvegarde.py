import json
from pathlib import Path
from threading import Lock

_LOCK = Lock()
_FILE = Path(__file__).resolve().parent / "sauvegarde.json"
_DEFAULT = {"victoires": 0, "defaites": 0}


def _load():
    if not _FILE.exists():
        return _DEFAULT.copy()
    try:
        with _FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return {"victoires": int(data.get("victoires", 0)), "defaites": int(data.get("defaites", 0))}
    except Exception:
        return _DEFAULT.copy()


def _save(data: dict):
    with _LOCK:
        
        _FILE.parent.mkdir(parents=True, exist_ok=True)
        with _FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def get_counts():
    """Retourne un dict {"victoires": int, "defaites": int}."""
    return _load()


def incr_victoire(n: int = 1):
    """Incrémente le nombre de victoires de `n` (par défaut 1) et retourne le nouveau dict."""
    data = _load()
    data["victoires"] = data.get("victoires", 0) + int(n)
    _save(data)
    return data


def incr_defaite(n: int = 1):
    """Incrémente le nombre de défaites de `n` (par défaut 1) et retourne le nouveau dict."""
    data = _load()
    data["defaites"] = data.get("defaites", 0) + int(n)
    _save(data)
    return data


def reset_counts():
    """Remet les compteurs à zéro et retourne le dict par défaut."""
    _save(_DEFAULT.copy())
    return _DEFAULT.copy()


__all__ = ["get_counts", "incr_victoire", "incr_defaite", "reset_counts"]
