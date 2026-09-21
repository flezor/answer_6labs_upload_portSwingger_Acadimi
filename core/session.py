import requests
from .common import build_url, extract_csrf, parse_cookie_header, redact_cookie_header

def create_authenticated_session(config, logger):
    session = requests.Session()
    session.headers.update({"User-Agent": config.USER_AGENT})
    cookie_header = config.SESSION_COOKIE.strip()
    if not cookie_header and config.PROMPT_FOR_SESSION_COOKIE:
        cookie_header = input("Paste Cookie header from the authenticated browser/Burp session: ").strip()
    if not cookie_header:
        raise RuntimeError("No session cookie supplied.")
    cookies = parse_cookie_header(cookie_header)
    if not cookies:
        raise RuntimeError("Could not parse SESSION_COOKIE.")
    for name, value in cookies.items():
        session.cookies.set(name, value)
    logger.info(f"Using manual session cookie: {redact_cookie_header(cookie_header)}")
    url = build_url(config.TARGET, config.ACCOUNT_URL)
    response = session.get(url, timeout=config.TIMEOUT, verify=config.VERIFY_TLS,
                           allow_redirects=config.FOLLOW_REDIRECTS)
    logger.info(f"Authentication check: HTTP {response.status_code} {response.url}")
    if "/login" in response.url:
        raise RuntimeError("Session appears unauthenticated or expired.")
    csrf = extract_csrf(response.text)
    logger.info("CSRF token extracted." if csrf else "No CSRF token found.")
    return session, csrf
