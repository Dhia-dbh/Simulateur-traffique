from core.simulateur import Simulateur
from core.analyseur import Analyseur
from interface.affichage import Affichage
from interface.export import Export

simu = Simulateur(fichier_config="data/config_reseau.json")

affichage = Affichage(simu.reseau)
export = Export(simu.reseau)
analyseur = Analyseur(simu.reseau)

print("/---/ État initial \\---\\")
affichage.afficher_console()
affichage.afficher_vehicules()

simu.lancer_simulation(n_tours=60, delta_t=60)

print("\n/---/ Etat \\---\\")
print(f"Vitesse moyenne: {analyseur.calculer_vitesses_moyennes():.1f} km/h")
print(f"Zones congestionnées: {analyseur.detecter_zones_congestion()}")

print("\n/---/ Graphiques \\---\\")
affichage.creer_graphique()

print("\n/---/ Sauvgarde des Résultats \\---\\")
export.exporter_csv("resultats_vehicules.csv")
export.exporter_json("resultats_reseau.json")
export.exporter_statistiques(simu.statistiques, "statistiques_simulation.json")
