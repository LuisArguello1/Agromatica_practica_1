--Creacion de tablas

CREATE TABLE genes (
    id SERIAL PRIMARY KEY,
    especie TEXT,
    nombre TEXT,
    longitud INT
);
CREATE TABLE cultivos (
    id SERIAL PRIMARY KEY,
    cultivo TEXT,
    anio INT,
    produccion NUMERIC,
    rendimiento NUMERIC
);
-- LLenado con datos de ejemplo en ambas tablas
INSERT INTO genes (especie, nombre, longitud) VALUES
('Zea mays', 'Adh1', 3200),
('Oryza sativa', 'Waxy', 3600),
('Arabidopsis thaliana', 'FLC', 6000),
('Solanum lycopersicum', 'Rin', 4500),
('Theobroma cacao', 'TcCHS1', 2800);

INSERT INTO cultivos (cultivo, anio, produccion, rendimiento) VALUES
('Cacao', 2021, 320000, 0.55),
('Cacao', 2022, 340000, 0.58),
('Cacao', 2023, 360000, 0.60),
('Banano', 2021, 6800000, 40.5),
('Banano', 2022, 7000000, 41.2),
('Banano', 2023, 7200000, 42.0),
('Arroz', 2021, 1500000, 4.6),
('Arroz', 2022, 1450000, 4.5),
('Arroz', 2023, 1600000, 4.8),
('Maíz', 2021, 1100000, 5.4),
('Maíz', 2022, 1150000, 5.6),
('Maíz', 2023, 1200000, 5.9),
('Caña de azúcar', 2021, 10000000, 70.0),
('Caña de azúcar', 2022, 10300000, 72.0),
('Caña de azúcar', 2023, 10500000, 73.5);

-- Comprobacion de llenado con selects
SELECT * FROM genes;
SELECT * FROM cultivos;