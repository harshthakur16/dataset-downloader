import re
from typing import Dict, List

DATE_PATTERNS = [
    re.compile(r"^\d{1,2}[a-zA-Z]{3,9}\d{0,4}$"),     # 2may, 14sep, 14september, 14sep2024
    re.compile(r"^\d{4}-\d{2}-\d{2}$"),               # 2024-09-14
    re.compile(r"^\d{2}-\d{2}-\d{2,4}$"),             # 14-09-24 or 14-09-2024
    re.compile(r"^\d{8}$"),                           # 20240914
]

def looksLikeDate(token: str) -> bool:
    token = token.strip().lower()
    return any(pat.match(token) for pat in DATE_PATTERNS)

def parseAdCreative(value: str) -> Dict[str, str]:
    """
    Splits adCreative into:
      - category
      - scriptName
      - actorName
      - uploadDate
      - formatName
      - otherData
    Preserves original adCreative separately in caller.
    """
    parts: List[str] = [p for p in str(value).split("_") if p != ""]
    out = {
        "category": "",
        "scriptName": "",
        "actorName": "",
        "uploadDate": "",
        "formatName": "",
        "otherData": "",
    }

    if not parts:
        return out

    if len(parts) >= 1: out["category"] = parts[0]
    if len(parts) >= 2: out["scriptName"] = parts[1]
    if len(parts) >= 3: out["actorName"] = parts[2]

    dateIndex = None
    for i, token in enumerate(parts):
        if looksLikeDate(token):
            dateIndex = i
            break

    usedIndexes = set([0, 1, 2]) & set(range(len(parts)))

    if dateIndex is not None:
        out["uploadDate"] = parts[dateIndex]
        usedIndexes.add(dateIndex)
        if dateIndex + 1 < len(parts):
            out["formatName"] = parts[dateIndex + 1]
            usedIndexes.add(dateIndex + 1)
    else:
        if len(parts) >= 4: out["formatName"] = parts[3]
        if len(parts) >= 5: out["uploadDate"] = parts[4]
        usedIndexes.update([3, 4])

    remaining = [parts[i] for i in range(len(parts)) if i not in usedIndexes]
    out["otherData"] = "_".join(remaining)

    return out

def snakeToCamel(name: str) -> str:
    # Convert snake_case to camelCase, keeping already-camel names as-is.
    if "_" not in name:
        # Ensure the very first character is lowercased if it's PascalCase
        return name[0:1].lower() + name[1:] if name else name
    parts = name.split("_")
    return parts[0].lower() + "".join(p.capitalize() or "_" for p in parts[1:])
