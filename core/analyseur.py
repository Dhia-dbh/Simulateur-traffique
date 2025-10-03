class Analyseur:
    
    def __init__(self, reseau):
        self.reseau = reseau
        
    def calculer_vitesses_moyennes(self):
        if not self.reseau.vehicules:
            return 0
        total_vitesse = sum(vehicule.vitesse for vehicule in self.reseau.vehicules)
        return total_vitesse / len(self.reseau.vehicules)
        
    def detecter_zones_congestion(self):
        zones_congestionnees = []
        for route in self.reseau.routes:
            if len(route.vehicules_presents) > 5:
                zones_congestionnees.append(route.nom)
        return zones_congestionnees
        
    def calculer_temps_parcours(self, route):
        if route.limite_vitesse == 0:
            return 0
        return route.longueur / route.limite_vitesse 
