from models.reseau import ReseauRoutier
from models.route import Route
from models.vehicule import Vehicule
import json

class Simulateur:
    
    def __init__(self, fichier_config=None):
        self.reseau = ReseauRoutier()
        self.statistiques = []
        self.tour_actuel = 0
        
        if fichier_config:
            self.charger_config(fichier_config)
            
    def charger_config(self, fichier_config):
        with open(fichier_config, 'r') as f:
            config = json.load(f)
            
        for route_data in config['routes']:
            route = Route(route_data['nom'], route_data['longueur'], route_data['limite_vitesse'])
            self.reseau.ajouter_route(route)
            
        for vehicule_data in config['vehicules']:
            vehicule = Vehicule(vehicule_data['identifiant'], vehicule_data['position'], vehicule_data['vitesse'])
            route = next(r for r in self.reseau.routes if r.nom == vehicule_data['route'])
            vehicule.changer_de_route(route)
            self.reseau.ajouter_vehicule(vehicule)
        
    def lancer_simulation(self, n_tours, delta_t):
        for tour in range(n_tours):
            self.tour_actuel = tour
            
            self.reseau.mettre_a_jour_reseau()
            
            stats = {'tour': tour, 'vehicules': len(self.reseau.vehicules)}
            self.statistiques.append(stats)
            
            print(f"Tour {tour}: {len(self.reseau.vehicules)} véhicules")
