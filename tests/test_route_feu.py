import sys
from pathlib import Path

# Prioritiser les modules du dépôt sur ceux installés
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from importlib.machinery import SourceFileLoader

# Charger directement les implémentations locales pour éviter
# les collisions avec un package installé nommé "models".
_route_mod = SourceFileLoader(
    "_route",
    str(Path(__file__).resolve().parents[1] / "models/route/route.py"),
).load_module()
_feu_mod = SourceFileLoader(
    "_feu_rouge",
    str(Path(__file__).resolve().parents[1] / "models/route/feu_rouge.py"),
).load_module()
_veh_mod = SourceFileLoader(
    "_vehicule",
    str(Path(__file__).resolve().parents[1] / "models/vehicule/vehicule.py"),
).load_module()

Route = _route_mod.Route
FeuRouge = _feu_mod.FeuRouge
Vehicule = _veh_mod.Vehicule


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
