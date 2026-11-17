"""Entry point so ``python -m echoprint ...`` works like the CLI."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
