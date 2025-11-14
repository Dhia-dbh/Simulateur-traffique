"""Composant FeuRouge pour la simulation routière.

Le feu alterne entre trois états dans l'ordre suivant:
- 'rouge' -> 'vert' -> 'orange' -> 'rouge' -> ...

Chaque état dure ``cycle`` unités de temps. Par défaut, ``cycle=5``.
"""

from __future__ import annotations

from typing import Literal


EtatFeu = Literal["rouge", "vert", "orange"]


class FeuRouge:
    def __init__(self, cycle: int = 5):
        # initialiser le cycle et l'état du feu
        if cycle <= 0:
            raise ValueError("Le cycle du feu doit être strictement positif.")
        self.cycle = int(cycle)
        self._etat_index = 0  # 0: rouge, 1: vert, 2: orange
        self._compteur = 0  # temps écoulé dans l'état courant

    @property
    def etat(self) -> EtatFeu:
        # retourner l'état actuel ('rouge', 'vert', 'orange')
        return ("rouge", "vert", "orange")[self._etat_index]

    def _avancer_etat(self) -> None:
        self._etat_index = (self._etat_index + 1) % 3
        self._compteur = 0

    def avancer_temps(self, dt: float) -> None:
        # faire avancer le temps et changer l'état si nécessaire
        if dt <= 0:
            return
        restant = dt
        while restant > 0:
            temps_restant_etat = self.cycle - self._compteur
            if restant >= temps_restant_etat:
                # on termine l'état courant et on passe au suivant
                self._compteur += temps_restant_etat
                self._avancer_etat()
                restant -= temps_restant_etat
            else:
                self._compteur += restant
                restant = 0

