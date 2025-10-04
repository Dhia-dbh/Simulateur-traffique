"""Point d'entrée de l'application de simulation de trafic."""

from __future__ import annotations

from core import Analyseur, Simulateur
from interface import Affichage, Export


def run() -> None:
    """Initialise les composants et exécute le scénario de simulation par défaut."""
    simulateur = Simulateur(fichier_config="data/config_reseau.json")

    affichage = Affichage(simulateur.reseau)
    export = Export(simulateur.reseau)
    analyseur = Analyseur(simulateur.reseau)

    print("=== État initial ===")
    affichage.afficher_console()
    affichage.afficher_vehicules()

    simulateur.lancer_simulation(n_tours=60, delta_t=60)

    print("\n=== Analyse finale ===")
    print(f"Vitesse moyenne: {analyseur.calculer_vitesses_moyennes():.1f} km/h")
    print(f"Zones congestionnées: {analyseur.detecter_zones_congestion()}")

    print("\n=== Graphiques ===")
    affichage.creer_graphique()

    export.exporter_csv("resultats_vehicules.csv")
    export.exporter_json("resultats_reseau.json")
    export.exporter_statistiques(simulateur.statistiques, "statistiques_simulation.json")


if __name__ == "__main__":
    run()
