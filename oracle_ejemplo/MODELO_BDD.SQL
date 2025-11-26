/*
-- Nombre
-- Atributos: TIPO DE DATO (SQL) (CONSTRAINT)
PERSONAS
EMPLEADO
DEPARTAMENTO
*/

CREATE TABLE PARTICIPANTES (
    id_participante INTEGER PRIMARY KEY,
    nombre VARCHAR(64),
    edad INTEGER,
    num_inscripcion INTEGER
)

CREATE TABLE ATLETA (
    id_atleta INTEGER PRIMARY KEY,
    disciplina VARCHAR(64),
    marca FLOAT,
    FOREIGN KEY (id_participante) REFERENCES PARTICIPANTES(id)
)

CREATE TABLE ENTRENADOR (
    id_entrenador INTEGER PRIMARY KEY,
    equipo VARCHAR2(100),
    FOREIGN KEY (id_entrenador) REFERENCES PARTICIPANTES(id_participante)
)

CREATE TABLE JUEZ (
    id_juez INTEGER PRIMARY KEY,
    especialidad VARCHAR2(100),
    FOREIGN KEY (id_juez) REFERENCES PARTICIPANTES(id_participante)
)