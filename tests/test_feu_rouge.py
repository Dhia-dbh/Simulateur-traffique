import sys
from pathlib import Path

# Prioritiser les modules du dépôt sur ceux installés
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from importlib.machinery import SourceFileLoader

# Charger FeuRouge directement depuis le fichier source pour éviter
# les conflits avec un éventuel package installé nommé "models".
_feu_mod = SourceFileLoader(
    "_feu_rouge",
    str(Path(__file__).resolve().parents[1] / "models/route/feu_rouge.py"),
).load_module()
FeuRouge = _feu_mod.FeuRouge


def test_cycle_du_feu():
    # créer un feu et tester la succession des états
    feu = FeuRouge(cycle=2)

    # Etat initial
    assert feu.etat == "rouge"

    # Après 1 unité de temps: toujours rouge (cycle=2)
    feu.avancer_temps(1)
    assert feu.etat == "rouge"

    # Après 2 unités au total: passe au vert
    feu.avancer_temps(1)
    assert feu.etat == "vert"

    # Encore 2 unités: passe à l'orange
    feu.avancer_temps(2)
    assert feu.etat == "orange"

    # Encore 2 unités: revient au rouge
    feu.avancer_temps(2)
    assert feu.etat == "rouge"
