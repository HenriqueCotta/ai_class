# src/aulas/aula01/app.py
from __future__ import annotations
import argparse
import numpy as np

xdata = np.array([1,2,3])
ydata = np.array([1,2,3])

xbar = np.mean(xdata)
ybar = np.mean(ydata)



def run(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(prog="aula01")
    parser.add_argument("--nome", default="Mundo")
    args = parser.parse_args(argv)

    print(f"[aula01] Olá, {args.nome}!")
    # aqui entra o conteúdo da aula 01