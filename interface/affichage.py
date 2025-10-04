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
            import matplotlib.figure
            import matplotlib.axes
            import matplotlib.pyplot as plt
            
            vitesses = [v.vitesse for v in self.reseau.vehicules]
            fig: matplotlib.figure.Figure
            ax: matplotlib.axes.Axes
            fig, ax = plt.subplots()
            ax.hist(vitesses, bins=10, edgecolor='black')
            ax.set_title('Stats Vitesses')
            ax.set_xlabel('Vitesse (km/h)')
            ax.set_ylabel('Nb Véhicules')
            plt.show()
            
        except ImportError:
            print("Matplotlib non disponible - pas de graphique")
