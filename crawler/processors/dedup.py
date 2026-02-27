import hashlib


def compute_content_hash(title: str) -> str:
    normalized = title.lower().strip()
    for noise in ["[video]", "[article]", "re:", "rt"]:
        normalized = normalized.replace(noise, "")
    return hashlib.md5(normalized.encode()).hexdigest()
