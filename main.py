import sys
import config
from core.engine import Engine
from core.logger import Logger
from core.preflight import run_preflight
from core.session import create_authenticated_session

def menu():
    print("\n" + "=" * 58)
    print(" PortSwigger Adaptive Upload Automation")
    print("=" * 58)
    print("1 - Run individual technique")
    print("2 - Run all techniques")
    print("3 - Challenge Mode (1 -> 6, stop on success)")
    print("0 - Exit")
    print("=" * 58)

def show(result):
    print(f"\nTechnique : {result.technique}")
    print(f"Success   : {result.success}")
    print(f"Message   : {result.message}")
    if result.status_code is not None: print(f"HTTP      : {result.status_code}")
    if result.verify_url: print(f"Verify URL: {result.verify_url}")
    if result.filename: print(f"Filename  : {result.filename}")
    if result.secret is not None: print(f"Secret    : {result.secret}")

def main():
    logger = Logger(config.LOG_FILE, config.VERBOSE)
    logger.info("Starting project.")
    if not run_preflight(config, logger):
        logger.error("Fix required configuration/files before continuing.")
        return 1
    try:
        session, csrf = create_authenticated_session(config, logger)
    except Exception as exc:
        logger.error(f"Session setup failed: {exc}")
        return 1
    engine = Engine(config, logger)
    while True:
        menu()
        choice = input("Select: ").strip()
        if choice == "0": return 0
        if choice == "1":
            print("\n".join(f"{i}. {n}" for i, n in enumerate(config.STRATEGY_ORDER, 1)))
            try: name = config.STRATEGY_ORDER[int(input("Technique number: ")) - 1]
            except (ValueError, IndexError): print("Invalid technique."); continue
            show(engine.run_one(name, session, csrf))
        elif choice in {"2", "3"}:
            if choice == "3": logger.info("Challenge Mode started.")
            results = engine.run_all(session, csrf)
            print("\nSummary:")
            for r in results: print(f"- {r.technique}: {'SUCCESS' if r.success else 'FAILED'}")
            success = next((r for r in results if r.success), None)
            if success:
                show(success); print("[+] Success found; execution stopped.")
            elif choice == "3": print("[-] No configured technique produced the success marker.")
        else: print("Invalid choice.")

if __name__ == "__main__": sys.exit(main())
