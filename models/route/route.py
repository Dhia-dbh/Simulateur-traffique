"""Définition d'une route utilisée dans le réseau simulé."""

from __future__ import annotations

from typing import List, Optional

from core.exceptions import RouteCapacityError, VehicleAlreadyPresentError


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
        self.nom = nom
        self.longueur = longueur
        self.limite_vitesse = limite_vitesse
        self.capacite_max = capacite_max
        self.vehicules_presents: List["Vehicule"] = []
        # Gestion optionnelle d'un feu rouge sur la route
        self.feu_rouge = None
        self.position_feu: Optional[float] = None

    def ajouter_vehicule(self, vehicule: "Vehicule") -> None:
        """Ajoute un véhicule à la route si celui-ci n'est pas déjà présent."""
        if vehicule in self.vehicules_presents:
            raise VehicleAlreadyPresentError(
                f"Le véhicule {vehicule.identifiant} est déjà sur la route {self.nom}."
            )
        if self.capacite_max is not None and len(self.vehicules_presents) >= self.capacite_max:
            raise RouteCapacityError(
                f"La route {self.nom} a atteint sa capacité maximale ({self.capacite_max})."
            )
        self.vehicules_presents.append(vehicule)
        vehicule.route_actuelle = self

    def mettre_a_jour_vehicules(self) -> None:
        """Demande à chaque véhicule présent de mettre à jour sa position."""
        for vehicule in self.vehicules_presents:
            # Si un feu est présent et rouge, empêcher le franchissement
            if (
                self.feu_rouge is not None
                and getattr(self.feu_rouge, "etat", None) == "rouge"
                and self.position_feu is not None
            ):
                prochaine_position = vehicule.position + vehicule.vitesse
                # Le véhicule s'arrête si son prochain déplacement franchirait le feu
                if vehicule.position < self.position_feu <= prochaine_position:
                    continue
            vehicule.avancer()

    # --- Fonctionnalités liées au feu rouge ---
    def ajouter_feu_rouge(self, feu, position: Optional[float] = None) -> None:
        """Ajoute un feu rouge à la route à la position donnée.

        Si ``position`` est omise, le feu est placé au milieu de la route.
        """
        if position is None:
            position = self.longueur / 2
        if position < 0 or position > self.longueur:
            raise ValueError("Position du feu en dehors des bornes de la route.")
        self.feu_rouge = feu
        self.position_feu = position

    def update(self, dt: float = 1.0) -> None:
        """Met à jour le feu et déplace les véhicules pour un pas de temps.

        Le déplacement des véhicules s'effectue avec la logique de
        ``mettre_a_jour_vehicules``; le feu avance de ``dt`` unités.
        """
        if self.feu_rouge is not None:
            # Avance le cycle du feu (si celui-ci implémente ``avancer_temps``)
            avancer = getattr(self.feu_rouge, "avancer_temps", None)
            if callable(avancer):
                avancer(dt)
        self.mettre_a_jour_vehicules()
