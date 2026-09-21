from importlib import import_module
from .models import StrategyResult

STRATEGY_CLASSES = {
    "direct": ("strategies.strategy1_direct", "DirectStrategy"),
    "mime": ("strategies.strategy2_mime", "MimeStrategy"),
    "traversal": ("strategies.strategy3_traversal", "TraversalStrategy"),
    "htaccess": ("strategies.strategy4_htaccess", "HtaccessStrategy"),
    "nullbyte": ("strategies.strategy5_nullbyte", "NullByteStrategy"),
    "polyglot": ("strategies.strategy6_polyglot", "PolyglotStrategy"),
}

class Engine:
    def __init__(self, config, logger):
        self.config, self.logger = config, logger
    def run_one(self, name, session, csrf):
        if name not in STRATEGY_CLASSES:
            return StrategyResult(False, name, "Unknown strategy.")
        module_name, class_name = STRATEGY_CLASSES[name]
        strategy = getattr(import_module(module_name), class_name)()
        try:
            result = strategy.run(session, csrf, self.config, self.logger)
        except Exception as exc:
            self.logger.error(f"Unhandled exception in {name}: {exc}")
            result = StrategyResult(False, name, f"Unhandled exception: {exc}")
        if result.success: self.logger.ok(f"SUCCESS via {result.technique}")
        else: self.logger.warn(f"{result.technique}: {result.message}")
        return result
    def run_all(self, session, csrf):
        results = []
        for name in self.config.STRATEGY_ORDER:
            result = self.run_one(name, session, csrf)
            results.append(result)
            if result.success and self.config.STOP_ON_SUCCESS:
                break
        return results
