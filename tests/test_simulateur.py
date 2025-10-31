import pytest

from models.reseau import ReseauRoutier
from models.route import Route
from models.vehicule import Vehicule


@pytest.fixture
def route_simple():
    return Route("A1", longueur=1000, limite_vitesse=30)


@pytest.fixture
def vehicule_exemple(route_simple):
    vehicule = Vehicule("V1", vitesse=10, route_actuelle=route_simple)
    route_simple.ajouter_vehicule(vehicule)
    return vehicule


@pytest.fixture
def reseau_simple(route_simple, vehicule_exemple):
    reseau = ReseauRoutier()
    reseau.ajouter_route(route_simple)
    reseau.ajouter_vehicule(vehicule_exemple)
    return reseau


def test_route_ajoute_vehicules_sans_doublon(route_simple, vehicule_exemple):
    route_simple.ajouter_vehicule(vehicule_exemple)
    assert route_simple.vehicules_presents.count(vehicule_exemple) == 1

    nouveau = Vehicule("V2", vitesse=20, route_actuelle=route_simple)
    route_simple.ajouter_vehicule(nouveau)
    assert len(route_simple.vehicules_presents) == 2


def test_route_met_a_jour_vehicules(route_simple, vehicule_exemple):
    position_initiale = vehicule_exemple.position

    route_simple.mettre_a_jour_vehicules()

    assert vehicule_exemple.position == position_initiale + vehicule_exemple.vitesse


def test_vehicule_ne_bouge_pas_sans_route():
    vehicule = Vehicule("V3", vitesse=15)
    vehicule.avancer()

    assert vehicule.position == 0


def test_changer_de_route_reinitialise_position(route_simple):
    nouvelle_route = Route("B1", longueur=500, limite_vitesse=50)
    vehicule = Vehicule("V4", position=100, vitesse=25, route_actuelle=route_simple)

    vehicule.changer_de_route(nouvelle_route)

    assert vehicule.route_actuelle is nouvelle_route
    assert vehicule.position == 0


def test_reseau_met_a_jour_reseau(reseau_simple, vehicule_exemple):
    position_initiale = vehicule_exemple.position

    reseau_simple.mettre_a_jour_reseau()

    assert vehicule_exemple.position == position_initiale + vehicule_exemple.vitesse


def test_reseau_etat_compte_elements(reseau_simple):
    reseau_simple.ajouter_intersection({"id": "I1"})

    etat = reseau_simple.obtenir_etat_reseau()

    assert etat["nombre_routes"] == 1
    assert etat["nombre_intersections"] == 1
    assert etat["nombre_vehicules"] == 1
