class ReseauRoutier:
    
    def __init__(self):
        self.routes = []
        self.intersections = []
        self.vehicules = []
        
    def ajouter_route(self, route):
        self.routes.append(route)
        
    def ajouter_intersection(self, intersection):
        self.intersections.append(intersection)
        
    def ajouter_vehicule(self, vehicule):
        self.vehicules.append(vehicule)
        
    def mettre_a_jour_reseau(self):
        for route in self.routes:
            route.mettre_a_jour_vehicules()
            
    def obtenir_etat_reseau(self):
        return {
            'nombre_routes': len(self.routes),
            'nombre_intersections': len(self.intersections),
            'nombre_vehicules': len(self.vehicules)
        }
