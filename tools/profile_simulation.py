"""Script utilitaire pour profiler la simulation avec cProfile."""

from __future__ import annotations

import argparse
import cProfile
import pstats
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core import ConfigurationError, Simulateur, SimulationError


def parser_arguments() -> argparse.Namespace:
    """Construit le parseur de ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Profiler le simulateur de trafic avec cProfile."
    )
    parser.add_argument(
        "-c",
        "--config",
        default="data/config_reseau.json",
        help="Chemin vers le fichier de configuration JSON.",
    )
    parser.add_argument(
        "-n",
        "--tours",
        type=int,
        default=60,
        help="Nombre de tours à simuler.",
    )
    parser.add_argument(
        "-d",
        "--delta",
        type=int,
        default=60,
        help="Pas de temps utilisé lors de la simulation.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Fichier de sortie pour enregistrer les statistiques cProfile.",
    )
    parser.add_argument(
        "-s",
        "--sort",
        default="cumtime",
        help="Critère de tri pour l'affichage des statistiques (par défaut cumtime).",
    )
    parser.add_argument(
        "-l",
        "--lines",
        type=int,
        default=20,
        help="Nombre de lignes à afficher dans le rapport texte.",
    )
    return parser.parse_args()


def profiler_simulation(arguments: argparse.Namespace) -> pstats.Stats:
    """Exécute la simulation sous cProfile et retourne les statistiques."""
    simulateur = Simulateur(fichier_config=arguments.config)
    profileur = cProfile.Profile()
    try:
        profileur.runcall(simulateur.lancer_simulation, arguments.tours, arguments.delta)
    except SimulationError as exc:
        print(f"Simulation interrompue pendant le profilage: {exc}")
    return pstats.Stats(profileur)


def main() -> None:
    """Point d'entrée du script de profilage."""
    arguments = parser_arguments()
    try:
        stats = profiler_simulation(arguments)
    except ConfigurationError as exc:
        print(f"Impossible de profiler la simulation: {exc}")
        return

    stats.sort_stats(arguments.sort)
    if arguments.output:
        stats.dump_stats(str(arguments.output))
        print(f"Statistiques enregistrées dans {arguments.output}")
    stats.print_stats(arguments.lines)


if __name__ == "__main__":
    main()
