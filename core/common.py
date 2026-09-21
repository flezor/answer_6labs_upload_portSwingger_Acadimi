import re
from urllib.parse import urljoin
from .models import StrategyResult


def build_url(target, path_or_url):
    return urljoin(target.rstrip("/") + "/", path_or_url)


def parse_cookie_header(value):
    value = value.strip()
    if value.lower().startswith("cookie:"):
        value = value.split(":", 1)[1].strip()

    result = {}
    for part in value.split(";"):
        part = part.strip()
        if "=" in part:
            name, val = part.split("=", 1)
            name = name.strip()
            if name:
                result[name] = val.strip()
    return result


def redact_cookie_header(value):
    value = value.strip()
    if value.lower().startswith("cookie:"):
        value = value.split(":", 1)[1].strip()

    out = []
    for part in value.split(";"):
        part = part.strip()
        if "=" in part:
            name, _ = part.split("=", 1)
            out.append(f"{name.strip()}=[REDACTED]")
    return "; ".join(out)


def extract_csrf(html):
    patterns = [
        r'name=["\']csrf["\'][^>]*value=["\']([^"\']+)["\']',
        r'value=["\']([^"\']+)["\'][^>]*name=["\']csrf["\']',
    ]
    for pattern in patterns:
        m = re.search(pattern, html, re.I)
        if m:
            return m.group(1)
    return None


def marker_result(technique, response, verify_url, success_marker, end_marker, filename=None):
    """Require actual execution markers; source-code responses are not success."""
    body = response.content
    start_marker = success_marker.encode("utf-8")
    end_marker_bytes = end_marker.encode("utf-8")

    start = body.find(start_marker)
    end = body.find(end_marker_bytes, start + len(start_marker)) if start >= 0 else -1

    if start < 0:
        return StrategyResult(
            False,
            technique,
            "HTTP response received, but runtime success marker was not detected.",
            verify_url,
            response.status_code,
            filename,
        )

    body_lower = body.lower()
    source_signatures = (b"<?php", b"<?=", b"file_get_contents(")
    if any(sig in body_lower for sig in source_signatures):
        return StrategyResult(
            False,
            technique,
            "PHP source code returned; the file was not executed.",
            verify_url,
            response.status_code,
            filename,
        )

    if end < 0:
        return StrategyResult(
            False,
            technique,
            "Start marker detected, but end marker was not detected.",
            verify_url,
            response.status_code,
            filename,
        )

    secret_bytes = body[start + len(start_marker):end]
    secret = secret_bytes.decode("utf-8", errors="replace").strip()

    return StrategyResult(
        True,
        technique,
        "Success marker detected from executed response.",
        verify_url,
        response.status_code,
        filename,
        secret,
    )


def extract_php_extension(text):
    patterns = [
        r"(?im)^\s*AddType\s+\S*php\S*\s+([.][A-Za-z0-9_-]+)\s*$",
        r"(?im)^\s*AddHandler\s+\S*php\S*\s+([.][A-Za-z0-9_-]+)\s*$",
        r"(?im)^\s*SetHandler\s+\S*php\S*\s+([.][A-Za-z0-9_-]+)\s*$",
    ]
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            return m.group(1)
    for line in text.splitlines():
        if "php" in line.lower():
            m = re.search(r"([.][A-Za-z0-9_-]+)\s*$", line.strip())
            if m:
                return m.group(1)
    return None


def nonempty_lines(path):
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if line and not line.startswith("#"):
                yield line
