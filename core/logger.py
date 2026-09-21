from datetime import datetime

class Logger:
    def __init__(self, path, verbose=True):
        self.path = path
        self.verbose = verbose
        self.path.parent.mkdir(parents=True, exist_ok=True)
    def _write(self, level, message):
        line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] [{level}] {message}"
        with self.path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
        if self.verbose:
            print(line)
    def info(self, m): self._write("INFO", m)
    def ok(self, m): self._write("OK", m)
    def warn(self, m): self._write("WARN", m)
    def error(self, m): self._write("ERROR", m)
    def debug(self, m): self._write("DEBUG", m)
