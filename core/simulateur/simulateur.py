"""Simulation logic for loading a traffic network and running it."""

from __future__ import annotations

import json
from typing import Any, Dict, Iterable, Optional

from models.reseau import ReseauRoutier
from models.route import Route
from models.vehicule import Vehicule


class Simulateur:
    """Pilote la simulation d'un réseau routier et centralise les statistiques."""

    def __init__(self, fichier_config: Optional[str] = None) -> None:
        """Crée un simulateur et charge éventuellement une configuration initiale.

        Parameters
        ----------
        fichier_config: Optional[str]
            Chemin vers un fichier JSON décrivant les routes et les véhicules
            à instancier avant de démarrer la simulation. Si ``None`` est
            fourni, le réseau reste vide.
        """
        self.reseau = ReseauRoutier()
        self.statistiques: list[Dict[str, Any]] = []
        self.tour_actuel = 0

        if fichier_config:
            self.charger_config(fichier_config)

    def charger_config(self, fichier_config: str) -> None:
        """Initialise le réseau routier à partir d'un fichier de configuration.

        Le fichier doit contenir deux listes ``routes`` et ``vehicules`` décrivant
        respectivement les tronçons routiers et les véhicules à ajouter.
        """
        with open(fichier_config, "r", encoding="utf-8") as fichier:
            config: Dict[str, Iterable[Dict[str, Any]]] = json.load(fichier)

        for route_data in config["routes"]:
            route = Route(
                route_data["nom"],
                route_data["longueur"],
                route_data["limite_vitesse"],
            )
            self.reseau.ajouter_route(route)

        for vehicule_data in config["vehicules"]:
            vehicule = Vehicule(
                vehicule_data["identifiant"],
                vehicule_data["position"],
                vehicule_data["vitesse"],
            )
            route = next(
                troncon
                for troncon in self.reseau.routes
                if troncon.nom == vehicule_data["route"]
            )
            vehicule.changer_de_route(route)
            self.reseau.ajouter_vehicule(vehicule)

    def lancer_simulation(self, n_tours: int, delta_t: int) -> None:
        """Exécute la simulation sur un nombre de tours fixé.

        Parameters
        ----------
        n_tours: int
            Nombre d'itérations à exécuter.
        delta_t: int
            Pas de temps utilisé pour chaque itération (réservé pour de
            potentielles évolutions du modèle).
        """
        for tour in range(n_tours):
            self.tour_actuel = tour

            self.reseau.mettre_a_jour_reseau()

            statistiques_tour = {"tour": tour, "vehicules": len(self.reseau.vehicules)}
            self.statistiques.append(statistiques_tour)

            print(f"Tour {tour}: {len(self.reseau.vehicules)} véhicules")
