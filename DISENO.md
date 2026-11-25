# Diseño de la API de Inscripciones

Grupo: ______________________________

## Paso 1 — Recursos

Un recurso es un **sustantivo** que la API expone con su propia URI.
La fila de *Curso* ya está hecha como ejemplo.

| Recurso     | URI de la colección | Atributos clave                        | Se relaciona con |
|-------------|---------------------|----------------------------------------|------------------|
| Curso       | `/cursos`           | codigo, nombre, cupos, prerrequisitos  | Inscripción      |
| Estudiante  | `/estudiantes`      | id, nombre, aprobados                  | Inscripción      |
| Inscripción | `/inscripciones`    | id, estudiante_id, curso_codigo, estado, creada_en | Estudiante, Curso | 

**Pregunta:** "inscribir" es un verbo. ¿Por qué en REST lo modelamos como el
recurso *Inscripción* y no como una URI `/inscribir`?

> Respuesta:

En REST las URIs identifican recursos (sustantivos) y los métodos HTTP indican las acciones (verbos). Modelarlo como /inscripciones permite crear (POST), consultar (GET) y cambiar su estado (PATCH) usando estándares HTTP, manteniendo un registro con historial en lugar de una acción aislada tipo RPC.

## Paso 2 — Contrato: los 5 endpoints

Completa el código de éxito y los errores posibles de cada endpoint.
Pistas: crear → `201`; no existe → `404`; choca con una regla de negocio → `409`.

| # | Método | URI                                          | Cuerpo que recibe     | Éxito | Errores |
|---|--------|----------------------------------------------|-----------------------|-------|---------|
| 1 | GET    | `/cursos`                                    | —                     | 200   | —       |
| 2 | POST   | `/inscripciones`                             | `InscripcionCrear`    | 201   | 404, 409|
| 3 | GET    | `/inscripciones/{inscripcion_id}`            | —                     | 200   | 404     |
| 4 | GET    | `/estudiantes/{estudiante_id}/inscripciones` | —                     | 200   | 404     |
| 5 | PATCH  | `/inscripciones/{inscripcion_id}`            | `CambioEstado`        | 200   | 404, 409|

## Paso 3 — Estados de una inscripción

```
   POST /inscripciones            PATCH {"estado": "CANCELADA"}
  ─────────────────────▶  ACTIVA  ──────────────────────────────▶  CANCELADA
```

**Pregunta:** ¿Qué debe responder la API si alguien intenta cancelar una
inscripción que ya está CANCELADA? ¿Por qué?

> Respuesta:
Debe responder 409 Conflict con detail: "TRANSICION_INVALIDA", porque la única transición permitida es de ACTIVA a CANCELADA. La petición es sintácticamente válida, pero entra en conflicto con el estado actual del recurso.