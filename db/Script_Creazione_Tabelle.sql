CREATE DATABASE IF NOT EXISTS HackaPizza;
USE HackaPizza;

-- Creazione della tabella PIATTI
CREATE TABLE PIATTI (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

-- Creazione della tabella INGREDIENTI
CREATE TABLE INGREDIENTI (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL
);

-- Creazione della tabella TECNICHE
CREATE TABLE TECNICHE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(255) NULL,
    vantaggi TEXT,
    svantaggi TEXT,
    descrizione TEXT
);

-- Creazione della tabella LICENZE
CREATE TABLE LICENZE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    sigla VARCHAR(50) NULL,
    livello VARCHAR(11) NOT NULL,
    descrizione TEXT
);

-- Creazione della tabella RISTORANTE
CREATE TABLE RISTORANTE (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pianeta VARCHAR(255) NOT NULL,
    chef VARCHAR(255) NOT NULL
);


-- Relazione N a N tra PIATTI e INGREDIENTI
CREATE TABLE PIATTI_INGREDIENTI (
    id_piatto INT NOT NULL,
    id_ingrediente INT NOT NULL,
    PRIMARY KEY (id_piatto, id_ingrediente),
    FOREIGN KEY (id_piatto) REFERENCES PIATTI(id) ON DELETE CASCADE,
    FOREIGN KEY (id_ingrediente) REFERENCES INGREDIENTI(id) ON DELETE CASCADE
);

-- Relazione N a N tra PIATTI e TECNICHE
CREATE TABLE PIATTI_TECNICHE (
    id_piatto INT NOT NULL,
    id_tecnica INT NOT NULL,
    PRIMARY KEY (id_piatto, id_tecnica),
    FOREIGN KEY (id_piatto) REFERENCES PIATTI(id) ON DELETE CASCADE,
    FOREIGN KEY (id_tecnica) REFERENCES TECNICHE(id) ON DELETE CASCADE
);

-- Relazione N a N tra RISTORANTE e LICENZE
CREATE TABLE RISTORANTE_LICENZE (
    id_ristorante INT NOT NULL,
    id_licenza INT NOT NULL,
    PRIMARY KEY (id_ristorante, id_licenza),
    FOREIGN KEY (id_ristorante) REFERENCES RISTORANTE(id) ON DELETE CASCADE,
    FOREIGN KEY (id_licenza) REFERENCES LICENZE(id) ON DELETE CASCADE
);

-- Relazione N a N tra RISTORANTE e PIATTI
CREATE TABLE RISTORANTE_PIATTI (
    id_ristorante INT NOT NULL,
    id_piatto INT NOT NULL,
    PRIMARY KEY (id_ristorante, id_piatto),
    FOREIGN KEY (id_ristorante) REFERENCES RISTORANTE(id) ON DELETE CASCADE,
    FOREIGN KEY (id_piatto) REFERENCES PIATTI(id) ON DELETE CASCADE
);

CREATE TABLE PIATTI_SOSTANZE (
    idPiatto INT NOT NULL,
    nomeSostanza1 VARCHAR(255) CHARACTER SET utf8mb4,
    valore1 DECIMAL(5,2),
    nomeSostanza2 VARCHAR(255) CHARACTER SET utf8mb4,
    valore2 DECIMAL(5,2),
    FOREIGN KEY (idPiatto) REFERENCES PIATTI(id)
);

ALTER TABLE RISTORANTE ADD COLUMN nome varchar(255) NULL;