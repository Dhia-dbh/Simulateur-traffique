class Route:
    
    def __init__(self, nom, longueur, limite_vitesse):
        self.nom = nom
        self.longueur = longueur
        self.limite_vitesse = limite_vitesse
        self.vehicules_presents = []
        
    def ajouter_vehicule(self, vehicule):
        if vehicule not in self.vehicules_presents:
            self.vehicules_presents.append(vehicule)
    
    def mettre_a_jour_vehicules(self):
        for vehicule in self.vehicules_presents:
            vehicule.avancer()
