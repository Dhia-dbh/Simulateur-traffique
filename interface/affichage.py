class Affichage:
    
    def __init__(self, reseau):
        self.reseau = reseau
        
    def afficher_console(self):
        print("=== État du Réseau ===")
        print(f"Routes: {len(self.reseau.routes)}")
        print(f"Véhicules: {len(self.reseau.vehicules)}")
        
        for route in self.reseau.routes:
            print(f"Route {route.nom}: {len(route.vehicules_presents)} véhicules")
            
    def afficher_vehicules(self):
        print("=== Véhicules ===")
        for vehicule in self.reseau.vehicules:
            route_nom = vehicule.route_actuelle.nom if vehicule.route_actuelle else "Aucune"
            print(f"{vehicule.identifiant}: {vehicule.vitesse}km/h, position {vehicule.position}, route {route_nom}")
            
    def creer_graphique(self):
        try:
            import matplotlib.pyplot as plt
            
            vitesses = [v.vitesse for v in self.reseau.vehicules]
            plt.figure(figsize=(8, 6))
            plt.hist(vitesses, bins=10, edgecolor='black')
            plt.title('Distribution des Vitesses')
            plt.xlabel('Vitesse (km/h)')
            plt.ylabel('Nombre de Véhicules')
            plt.show()
            
        except ImportError:
            print("Matplotlib non disponible - pas de graphique")
