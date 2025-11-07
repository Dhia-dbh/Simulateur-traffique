"""Script de validation manuelle des exceptions du simulateur."""

from __future__ import annotations

import os
import sys
import tempfile
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Type

sys.path.append(str(Path(__file__).resolve().parents[1]))

from core.analyseur import Analyseur
from core.exceptions import (
    ConfigurationFileNotFoundError,
    ConfigurationFormatError,
    DivisionByZeroAnalysisError,
    InvalidSimulationParameterError,
    InvalidVehicleStateError,
    MissingDataError,
    RouteCapacityError,
    RouteNotFoundError,
    VehicleAlreadyPresentError,
)
from core.simulateur import Simulateur
from models.reseau import ReseauRoutier
from models.route import Route
from models.vehicule import Vehicule


@dataclass(frozen=True)
class ExceptionTest:
    """Décrit un scénario de validation d'exception."""

    nom: str
    exception_attendue: Type[BaseException]
    declencheur: Callable[[], None]


def scenario_configuration_file_not_found() -> None:
    Simulateur(fichier_config="__fichier_inexistant__.json")


def scenario_configuration_format_error() -> None:
    contenu = """{
        "routes": [
            {"nom": "A1"}
        ],
        "vehicules": []
    }"""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        tmp.write(contenu)
        tmp_path = tmp.name
    try:
        simulateur = Simulateur()
        simulateur.charger_config(tmp_path)
    finally:
        os.remove(tmp_path)


def scenario_invalid_simulation_parameter() -> None:
    simulateur = Simulateur()
    route = Route("TEST", longueur=1000, limite_vitesse=50)
    simulateur.reseau.ajouter_route(route)
    vehicule = Vehicule("V1", vitesse=10, route_actuelle=route)
    simulateur.reseau.ajouter_vehicule(vehicule)
    simulateur.lancer_simulation(n_tours=0, delta_t=60)


def scenario_route_capacity_error() -> None:
    route = Route("CAP", longueur=1000, limite_vitesse=50, capacite_max=1)
    route.ajouter_vehicule(Vehicule("V2", vitesse=10, route_actuelle=route))
    route.ajouter_vehicule(Vehicule("V3", vitesse=10, route_actuelle=route))


def scenario_vehicle_already_present() -> None:
    route = Route("DUP", longueur=1000, limite_vitesse=50)
    vehicule = Vehicule("V4", vitesse=10, route_actuelle=route)
    route.ajouter_vehicule(vehicule)
    route.ajouter_vehicule(vehicule)


def scenario_invalid_vehicle_state() -> None:
    Vehicule("V5", vitesse=-10)


def scenario_route_not_found() -> None:
    reseau = ReseauRoutier()
    route = Route("ABSENTE", longueur=1000, limite_vitesse=50)
    vehicule = Vehicule("V6", vitesse=10, route_actuelle=route)
    reseau.ajouter_vehicule(vehicule)


def scenario_missing_data_analysis() -> None:
    analyseur = Analyseur(ReseauRoutier())
    analyseur.calculer_vitesses_moyennes()


def scenario_division_by_zero_analysis() -> None:
    route = Route("ZERO", longueur=800, limite_vitesse=1)
    route.limite_vitesse = 0
    analyseur = Analyseur(ReseauRoutier())
    analyseur.reseau.routes.append(route)
    analyseur.calculer_temps_parcours(route)


TESTS: tuple[ExceptionTest, ...] = (
    ExceptionTest(
        "Fichier de configuration introuvable",
        ConfigurationFileNotFoundError,
        scenario_configuration_file_not_found,
    ),
    ExceptionTest(
        "Format de configuration invalide",
        ConfigurationFormatError,
        scenario_configuration_format_error,
    ),
    ExceptionTest(
        "Paramètre de simulation invalide",
        InvalidSimulationParameterError,
        scenario_invalid_simulation_parameter,
    ),
    ExceptionTest(
        "Capacité de route dépassée",
        RouteCapacityError,
        scenario_route_capacity_error,
    ),
    ExceptionTest(
        "Véhicule déjà présent sur la route",
        VehicleAlreadyPresentError,
        scenario_vehicle_already_present,
    ),
    ExceptionTest(
        "État du véhicule invalide",
        InvalidVehicleStateError,
        scenario_invalid_vehicle_state,
    ),
    ExceptionTest(
        "Route inexistante dans le réseau",
        RouteNotFoundError,
        scenario_route_not_found,
    ),
    ExceptionTest(
        "Analyse sans données",
        MissingDataError,
        scenario_missing_data_analysis,
    ),
    ExceptionTest(
        "Division par zéro dans une analyse",
        DivisionByZeroAnalysisError,
        scenario_division_by_zero_analysis,
    ),
)


def run_tests() -> int:
    """Exécute tous les scénarios et retourne le nombre d'échecs."""
    echecs = 0
    print("=== Vérification des exceptions du simulateur ===")
    for test in TESTS:
        try:
            test.declencheur()
        except test.exception_attendue as exc:
            print(f"[OK] {test.nom} -> {test.exception_attendue.__name__}: {exc}")
        except Exception as exc:  # pragma: no cover - diagnostic humain
            echecs += 1
            print(f"[ERREUR] {test.nom} -> exception inattendue {type(exc).__name__}: {exc}")
            traceback.print_exc()
        else:
            echecs += 1
            print(f"[ECHEC] {test.nom} -> aucune exception levée.")
    print(f"\nRésultat: {len(TESTS) - echecs}/{len(TESTS)} tests réussis")
    return echecs


if __name__ == "__main__":
    nb_echecs = run_tests()
    sys.exit(1 if nb_echecs else 0)
