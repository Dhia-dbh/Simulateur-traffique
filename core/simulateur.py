"""Module de simulation du trafic routier.

Ce module contient la classe Simulateur qui gère l'exécution
de la simulation du trafic sur un réseau routier.
"""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from models.reseau import ReseauRoutier
from models.route import Route
from models.vehicule import Vehicule


class Simulateur:
    
    def __init__(self, fichier_config: Optional[str] = None) -> None:
        self.reseau: ReseauRoutier = ReseauRoutier()
        self.statistiques: List[Dict[str, Any]] = []
        self.tour_actuel: int = 0
        
        if fichier_config:
            self.charger_config(fichier_config)
    
    def charger_config(self, fichier_config: str) -> None:
        config_path = Path(fichier_config)
        
        with config_path.open('r', encoding='utf-8') as fichier:
            config = json.load(fichier)
        
        self._charger_routes(config.get('routes', []))
        self._charger_vehicules(config.get('vehicules', []))
    
    def _charger_routes(self, routes_data: List[Dict[str, Any]]) -> None:
        for route_data in routes_data:
            route = Route(
                nom=route_data['nom'],
                longueur=route_data['longueur'],
                limite_vitesse=route_data['limite_vitesse']
            )
            self.reseau.ajouter_route(route)
    
    def _charger_vehicules(self, vehicules_data: List[Dict[str, Any]]) -> None:
        for vehicule_data in vehicules_data:
            vehicule = Vehicule(
                identifiant=vehicule_data['identifiant'],
                position=vehicule_data['position'],
                vitesse=vehicule_data['vitesse']
            )
            
            route = self._trouver_route_par_nom(vehicule_data['route'])
            vehicule.changer_de_route(route)
            self.reseau.ajouter_vehicule(vehicule)
    
    def _trouver_route_par_nom(self, nom_route: str) -> Route:
        return next(
            route for route in self.reseau.routes 
            if route.nom == nom_route
        )
    
    def lancer_simulation(self, n_tours: int, delta_t: float) -> None:
        for tour in range(n_tours):
            self._executer_tour(tour)
    
    def _executer_tour(self, tour: int) -> None:
        self.tour_actuel = tour
        
        # Mise à jour de l'état du réseau
        self.reseau.mettre_a_jour_reseau()
        
        # Collecte des statistiques
        stats = self._collecter_statistiques(tour)
        self.statistiques.append(stats)
        
        # Affichage de la progression
        self._afficher_progression(tour, stats)
    
    def _collecter_statistiques(self, tour: int) -> Dict[str, Any]:
        return {
            'tour': tour,
            'vehicules': len(self.reseau.vehicules)
        }
    
    def _afficher_progression(self, tour: int, stats: Dict[str, Any]) -> None:
        print(f"Tour {tour}: {stats['vehicules']} véhicules")
