class Vehicule:
    
    def __init__(self, identifiant, position=0, vitesse=50, route_actuelle=None):
        self.identifiant = identifiant
        self.position = position
        self.vitesse = vitesse
        self.route_actuelle = route_actuelle
        
    def avancer(self):
        if self.route_actuelle is not None:
            self.position += self.vitesse
    
    def changer_de_route(self, nouvelle_route):
        self.route_actuelle = nouvelle_route
        self.position = 0
