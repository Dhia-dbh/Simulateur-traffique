from simulateur_trafic.models.route import FeuRouge, Route
from simulateur_trafic.models.vehicule import Vehicule


def test_arret_au_feu_rouge():
    # créer une route, un feu et un véhicule
    route = Route("A2", longueur=500, limite_vitesse=50, capacite_max=5)
    feu = FeuRouge(cycle=2)  # chaque état dure 2 unités
    route.ajouter_feu_rouge(feu, position=100)

    vehicule = Vehicule("V10", position=90, vitesse=20, route_actuelle=route)
    route.ajouter_vehicule(vehicule)

    # vérifier que le véhicule s'arrête devant le feu rouge
    # update fait avancer le feu puis la route; avec cycle=2, après dt=1 => toujours rouge
    route.update(dt=1.0)
    assert vehicule.position == 90  # n'a pas franchi le feu

    # Après un second pas, le feu passe au vert; le véhicule peut avancer
    route.update(dt=1.0)
    assert vehicule.position == 110
