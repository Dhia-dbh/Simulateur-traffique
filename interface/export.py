import json
import csv

class Export:
    
    def __init__(self, reseau):
        self.reseau = reseau
        
    def exporter_json(self, nom_fichier):
        data = {
            'routes': [{'nom': r.nom, 'longueur': r.longueur, 'limite_vitesse': r.limite_vitesse} for r in self.reseau.routes],
            'vehicules': [{'id': v.identifiant, 'vitesse': v.vitesse, 'position': v.position} for v in self.reseau.vehicules]
        }
        
        with open(nom_fichier, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Données exportées vers {nom_fichier}")
        
    def exporter_csv(self, nom_fichier):
        with open(nom_fichier, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Vitesse', 'Position', 'Route'])
            
            for vehicule in self.reseau.vehicules:
                route_nom = vehicule.route_actuelle.nom if vehicule.route_actuelle else 'Aucune'
                writer.writerow([vehicule.identifiant, vehicule.vitesse, vehicule.position, route_nom])
                
        print(f"Véhicules exportés vers {nom_fichier}")
        
    def exporter_statistiques(self, statistiques, nom_fichier):
        with open(nom_fichier, 'w') as f:
            json.dump(statistiques, f, indent=2)
        print(f"Statistiques exportées vers {nom_fichier}")
