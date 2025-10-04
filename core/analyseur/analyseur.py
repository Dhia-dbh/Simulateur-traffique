"""Outils d'analyse pour extraire des métriques du réseau simulé."""

from __future__ import annotations

from typing import List, Sequence

from models.route import Route
from models.vehicule import Vehicule


class Analyseur:
    """Fournit des indicateurs de performance du réseau routier."""

    def __init__(self, reseau) -> None:
        """Crée un analyseur lié au réseau simulé."""
        self.reseau = reseau

    def calculer_vitesses_moyennes(self) -> float:
        """Calcule la vitesse moyenne actuelle de l'ensemble des véhicules."""
        vehicules: Sequence[Vehicule] = self.reseau.vehicules
        if not vehicules:
            return 0.0
        total_vitesse = sum(vehicule.vitesse for vehicule in vehicules)
        return total_vitesse / len(vehicules)

    def detecter_zones_congestion(self) -> List[str]:
        """Identifie les routes dont la charge dépasse le seuil de congestion."""
        zones_congestionnees: List[str] = []
        for route in self.reseau.routes:
            if len(route.vehicules_presents) > 5:
                zones_congestionnees.append(route.nom)
        return zones_congestionnees

    def calculer_temps_parcours(self, route: Route) -> float:
        """Estime le temps de parcours d'une route en supposant la vitesse limite."""
        if route.limite_vitesse == 0:
            return 0.0
        return route.longueur / route.limite_vitesse
