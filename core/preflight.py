def run_preflight(config, logger, required_strategies=None):
    ok = True
    required = set(required_strategies or config.STRATEGY_ORDER)

    def check(condition, message):
        nonlocal ok
        if condition:
            logger.ok(message)
        else:
            logger.error(message)
            ok = False

    check(config.TARGET.startswith(("http://", "https://")), "Target URL configured.")
    check(bool(config.UPLOAD_URL), "Upload URL configured.")

    if "htaccess" in required:
        check(config.HTACCESS_FILE.exists(), f".htaccess source exists: {config.HTACCESS_FILE}")

    if "nullbyte" in required:
        check(config.NULLBYTE_FILE.exists(), f"Null-byte file exists: {config.NULLBYTE_FILE}")

    if "polyglot" in required:
        check(config.POLYGLOT_FILE.exists(), f"Pre-built polyglot exists: {config.POLYGLOT_FILE}")

    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return ok
