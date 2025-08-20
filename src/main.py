# src/main.py
from __future__ import annotations
import argparse
import importlib
import pkgutil
import sys
from pathlib import Path

PKG_NAME = "aulas"  # pacote base onde estão as aulas
DEFAULT_ENTRY = "app"  # módulo dentro da aula
DEFAULT_FUNC = "run"   # função a ser chamada

def list_lessons() -> list[str]:
    """Lista subpacotes de 'aulas' que são aulas (têm __init__.py)."""
    import aulas  # type: ignore
    pkg_path = Path(aulas.__file__).parent
    lessons = []
    for mod in pkgutil.iter_modules([str(pkg_path)]):
        # apenas pacotes (is_pkg=True) como aula01, aula02...
        if mod.is_pkg:
            lessons.append(mod.name)
    return sorted(lessons)

def import_entry(lesson: str):
    """
    Importa dinamicamente aulas.<lesson>.app e retorna a função run.
    Espera encontrar: src/aulas/<lesson>/app.py com def run(args: list[str]) -> None
    """
    full_module = f"{PKG_NAME}.{lesson}.{DEFAULT_ENTRY}"
    try:
        mod = importlib.import_module(full_module)
    except ModuleNotFoundError as e:
        raise SystemExit(f"Não encontrei o módulo '{full_module}'. Detalhe: {e}")

    func = getattr(mod, DEFAULT_FUNC, None)
    if func is None or not callable(func):
        raise SystemExit(
            f"O módulo '{full_module}' não possui a função '{DEFAULT_FUNC}(args)'."
        )
    return func

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python src/main.py",
        description="Executor de aulas: python src/main.py <aula> [-- args-da-aula]"
    )
    parser.add_argument(
        "aula",
        nargs="?",
        help="nome da aula (ex.: aula01). Se omitido, lista as aulas disponíveis."
    )
    parser.add_argument(
        "aula_args",
        nargs=argparse.REMAINDER,
        help="argumentos a repassar para a aula (use após '--')."
    )
    return parser.parse_args(argv)

def main(argv: list[str] | None = None) -> None:
    ns = parse_args(sys.argv[1:] if argv is None else argv)
    if not ns.aula:
        lessons = list_lessons()
        if not lessons:
            print("Nenhuma aula encontrada em 'src/aulas/'.")
            raise SystemExit(1)
        print("Aulas disponíveis:")
        for name in lessons:
            print(f"  - {name}")
        print("\nExemplo: python src/main.py aula01 -- --foo 123")
        return

    # Permite chamar como: python src/main.py aula01 -- <args>
    # ns.aula_args inclui o '--' como primeiro elemento em algumas shells; vamos filtrar
    forward = [a for a in ns.aula_args if a != "--"]

    run = import_entry(ns.aula)
    run(forward)

if __name__ == "__main__":
    main()