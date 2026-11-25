"""
Paso 5 - Escribe 3 pruebas para las reglas de negocio

El fixture `cliente` (en conftest.py) te da un cliente HTTP con los datos
reiniciados en cada prueba. Recuerda quién es quién (ver app/datos.py):
    e1, e2, e3 aprobaron IS1      e4 no ha aprobado nada
    IS2 tiene solo 2 cupos y requiere IS1

Sigue el patrón Arrange / Act / Assert del ejemplo.

    pytest tests/test_paso5_mis_pruebas.py -v
"""
import pytest


def test_ejemplo_inscripcion_exitosa(cliente):
    # Arrange: e1 ya aprobó IS1, así que puede ver IS2
    cuerpo = {"estudiante_id": "e1", "curso_codigo": "IS2"}
    # Act
    r = cliente.post("/inscripciones", json=cuerpo)
    # Assert
    assert r.status_code == 201
    assert r.json()["estado"] == "ACTIVA"


def test_no_permite_inscripcion_duplicada(cliente):
    # Arrange: inscribe a e1 en IS1
    cuerpo = {"estudiante_id": "e1", "curso_codigo": "IS1"}
    cliente.post("/inscripciones", json=cuerpo)
    # Act: intenta inscribirlo OTRA VEZ en IS1
    r = cliente.post("/inscripciones", json=cuerpo)
    # Assert: 409 y detail == "DUPLICADA"
    assert r.status_code == 409
    assert r.json()["detail"] == "DUPLICADA"


def test_no_permite_inscribir_sin_prerrequisitos(cliente):
    # TODO(Paso 5)
    # Arrange: e4 no aprobó IS1, así que no puede ver IS2
    cuerpo = {"estudiante_id": "e4", "curso_codigo": "IS2"}
    # Act:     intenta inscribir a e4 en IS2
    r = cliente.post("/inscripciones", json=cuerpo)
    # Assert:  409 y detail == "PRERREQUISITOS_PENDIENTES"
    assert r.status_code == 409
    assert r.json()["detail"] == "PRERREQUISITOS_PENDIENTES"


def test_no_permite_inscribir_sin_cupo(cliente):
    # Arrange: llena los 2 cupos de IS2 (e1 y e2)
    cliente.post("/inscripciones", json={"estudiante_id": "e1", "curso_codigo": "IS2"})
    cliente.post("/inscripciones", json={"estudiante_id": "e2", "curso_codigo": "IS2"})
    # Act: intenta inscribir a e3 en IS2
    r = cliente.post("/inscripciones", json={"estudiante_id": "e3", "curso_codigo": "IS2"})
    # Assert: 409 y detail == "SIN_CUPO"
    assert r.status_code == 409
    assert r.json()["detail"] == "SIN_CUPO"
