"""Définition d'une route utilisée dans le réseau simulé."""

from __future__ import annotations

from typing import List, Optional

from core.exceptions import (
    InvalidSimulationParameterError,
    RouteCapacityError,
    VehicleAlreadyPresentError,
)
from core.optimisation.cython_ext import update_positions


class Route:
    """Représente un tronçon de route sur lequel circulent des véhicules."""

    def __init__(
        self,
        nom: str,
        longueur: float,
        limite_vitesse: float,
        capacite_max: Optional[int] = None,
    ) -> None:
        """Construit une route avec ses caractéristiques principales."""
        if longueur <= 0:
            raise InvalidSimulationParameterError(
                f"Longueur négative ou nulle ({longueur}) pour la route {nom}."
            )
        if limite_vitesse <= 0:
            raise InvalidSimulationParameterError(
                f"Limite de vitesse négative ou nulle ({limite_vitesse}) pour la route {nom}."
            )
        if capacite_max is not None and capacite_max <= 0:
            raise InvalidSimulationParameterError(
                f"Capacité maximale invalide ({capacite_max}) pour la route {nom}."
            )

        self.nom = nom
        self.longueur = longueur
        self.limite_vitesse = limite_vitesse
        self.capacite_max = capacite_max
        self.vehicules_presents: List["Vehicule"] = []

    def ajouter_vehicule(self, vehicule: "Vehicule") -> None:
        """Ajoute un véhicule à la route si celui-ci n'est pas déjà présent."""
        if vehicule in self.vehicules_presents:
            raise VehicleAlreadyPresentError(
                f"Le véhicule {vehicule.identifiant} circule déjà sur la route {self.nom}."
            )

        if self.capacite_max is not None and len(self.vehicules_presents) >= self.capacite_max:
            raise RouteCapacityError(
                f"La route {self.nom} a atteint sa capacité maximale ({self.capacite_max})."
            )

        if vehicule.route_actuelle is not self:
            vehicule.changer_de_route(self)

        self.vehicules_presents.append(vehicule)

    def mettre_a_jour_vehicules(self, delta_t: float = 1.0) -> None:
        """Demande à chaque véhicule présent de mettre à jour sa position."""
        if not self.vehicules_presents:
            return

        vehicules = list(self.vehicules_presents)

        for vehicule in vehicules:
            vehicule.verifier_deplacement(delta_t)

        positions = [vehicule.position for vehicule in vehicules]
        vitesses = [vehicule.vitesse for vehicule in vehicules]
        try:
            nouvelles_positions = update_positions(positions, vitesses, delta_t)
        except Exception:  # pragma: no cover - fallback si extension indispo
            for vehicule in vehicules:
                vehicule.avancer(delta_t)
            return

        for vehicule, nouvelle_position in zip(vehicules, nouvelles_positions):
            vehicule.verifier_position(nouvelle_position)
            vehicule.position = nouvelle_position
