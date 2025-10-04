"""Définition d'une route utilisée dans le réseau simulé."""

from __future__ import annotations

from typing import List


class Route:
    """Représente un tronçon de route sur lequel circulent des véhicules."""

    def __init__(self, nom: str, longueur: float, limite_vitesse: float) -> None:
        """Construit une route avec ses caractéristiques principales."""
        self.nom = nom
        self.longueur = longueur
        self.limite_vitesse = limite_vitesse
        self.vehicules_presents: List["Vehicule"] = []

    def ajouter_vehicule(self, vehicule: "Vehicule") -> None:
        """Ajoute un véhicule à la route si celui-ci n'est pas déjà présent."""
        if vehicule not in self.vehicules_presents:
            self.vehicules_presents.append(vehicule)

    def mettre_a_jour_vehicules(self) -> None:
        """Demande à chaque véhicule présent de mettre à jour sa position."""
        for vehicule in self.vehicules_presents:
            vehicule.avancer()
