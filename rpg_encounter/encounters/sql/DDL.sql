DROP SCHEMA IF EXISTS encounters CASCADE;
CREATE SCHEMA encounters;
-- Potwory
CREATE TABLE encounters.potwory(
    "id" SERIAL PRIMARY KEY ,
    "nazwa" VARCHAR(100) UNIQUE NOT NULL,
    "opis" VARCHAR(1000) NOT NULL,
    "poziom_trudnosci" INTEGER NOT NULL,
    "id_rasa" INTEGER NOT NULL
);
-- Tereny
CREATE TABLE encounters.tereny(
    "id" SERIAL PRIMARY KEY,
    "nazwa" VARCHAR(100) UNIQUE NOT NULL,
    "opis" VARCHAR(1000) NOT NULL
);
-- Potyczki
CREATE TABLE encounters.potyczki(
    "id" SERIAL PRIMARY KEY,
    "tytul" VARCHAR(100) NOT NULL,
    "opis" VARCHAR(1000) NOT NULL,
    "id_lokacja" INTEGER NOT NULL,
    "id_tworca" INTEGER NOT NULL
);
-- Skarby
CREATE TABLE encounters.skarby(
    "id" SERIAL PRIMARY KEY,
    "nazwa" VARCHAR(100)UNIQUE NOT NULL,
    "opis" VARCHAR(1000) NOT NULL,
    "rzadkosc" VARCHAR(100) NOT NULL,
    "wartosc" INTEGER NOT NULL
);
-- Rasy
CREATE TABLE encounters.rasy(
    "id" SERIAL PRIMARY KEY,
    "nazwa" VARCHAR(100) UNIQUE NOT NULL,
    "opis" VARCHAR(1000) NOT NULL
);
-- Lokacje
CREATE TABLE encounters.lokacje(
    "id" SERIAL PRIMARY KEY,
    "nazwa" VARCHAR(100) UNIQUE NOT NULL,
    "opis" VARCHAR(1000) NOT NULL,
    "id_teren" INTEGER NOT NULL
);
-- Pułapki
CREATE TABLE encounters.pulapki(
    "id" SERIAL PRIMARY KEY,
    "nazwa" VARCHAR(100) NOT NULL,
    "opis" VARCHAR(1000) NOT NULL,
    "poziom_trudnosci" INTEGER NOT NULL
);
-- Osoby
CREATE TABLE encounters.osoby(
    "id" SERIAL PRIMARY KEY,
    "nazwa" VARCHAR(100) NOT NULL,
    "login" VARCHAR(50) NOT NULL,
    "haslo" VARCHAR(50) NOT NULL
);
-- Uprawnienia
CREATE TABLE encounters.uprawnienia(
    "id" SERIAL PRIMARY KEY,
    "nazwa" VARCHAR(100) NOT NULL,
    "typ" VARCHAR(100) NOT NULL
);
-- pulapka - Potyczka
CREATE TABLE encounters.pulapka_potyczka(
    "id_potyczka" INTEGER NOT NULL,
    "id_pulapka" INTEGER NOT NULL
);
-- Rasa - Teren
CREATE TABLE encounters.rasa_teren(
    "id_rasa" INTEGER NOT NULL,
    "id_teren" INTEGER NOT NULL
);
-- Skarb - Potyczka
CREATE TABLE encounters.skarb_potyczka(
    "id_potyczka" INTEGER NOT NULL,
    "id_skarb" INTEGER NOT NULL
);
-- Uprawnienia - Osoby
CREATE TABLE encounters.uprawnienia_osoby(
    "id_uprawniennie" INTEGER NOT NULL,
    "id_osoba" INTEGER NOT NULL
);
-- Potwór - Potyczka
CREATE TABLE encounters.potwor_potyczka(
    "id_potyczka" INTEGER NOT NULL,
    "id_potwor" INTEGER NOT NULL
);

-- Klucze obce
ALTER TABLE encounters.potwory 
    ADD CONSTRAINT "potwory_id_rasa_foreign" FOREIGN KEY("id_rasa") REFERENCES encounters.rasy("id");
ALTER TABLE encounters.potyczki 
    ADD CONSTRAINT "potyczki_id_lokacja_foreign" FOREIGN KEY("id_lokacja") REFERENCES encounters.lokacje("id"),
    ADD CONSTRAINT "potyczki_id_tworca_foreign" FOREIGN KEY("id_tworca") REFERENCES encounters.osoby("id");
ALTER TABLE encounters.lokacje 
    ADD CONSTRAINT "lokacje_id_teren_foreign" FOREIGN KEY("id_teren") REFERENCES encounters.tereny("id");
ALTER TABLE encounters.potwor_potyczka 
    ADD CONSTRAINT "potwor_potyczka_id_potyczka_foreign" FOREIGN KEY("id_potyczka") REFERENCES encounters.potyczki("id"),
    ADD CONSTRAINT "potwor_potyczka_id_potwor_foreign" FOREIGN KEY("id_potwor") REFERENCES encounters.potwory("id");
ALTER TABLE encounters.skarb_potyczka 
    ADD CONSTRAINT "skarb_potyczka_id_potyczka_foreign" FOREIGN KEY("id_potyczka") REFERENCES encounters.potyczki("id"),
    ADD CONSTRAINT "skarb_potyczka_id_skarb_foreign" FOREIGN KEY("id_skarb") REFERENCES encounters.skarby("id");
ALTER TABLE encounters.pulapka_potyczka 
    ADD CONSTRAINT "pulapka_potyczka_id_potyczka_foreign" FOREIGN KEY("id_potyczka") REFERENCES encounters.potyczki("id"),
    ADD CONSTRAINT "pulapka_potyczka_id_pulapka_foreign" FOREIGN KEY("id_pulapka") REFERENCES encounters.pulapki("id");
ALTER TABLE encounters.uprawnienia_osoby 
    ADD CONSTRAINT "uprawnienia_osoby_id_uprawniennie_foreign" FOREIGN KEY("id_uprawniennie") REFERENCES encounters.uprawnienia("id"),
    ADD CONSTRAINT "uprawnienia_osoby_id_osoba_foreign" FOREIGN KEY("id_osoba") REFERENCES encounters.osoby("id");
ALTER TABLE encounters.rasa_teren 
    ADD CONSTRAINT "rasa_teren_id_rasa_foreign" FOREIGN KEY("id_rasa") REFERENCES encounters.rasy("id"),
    ADD CONSTRAINT "rasa_teren_id_teren_foreign" FOREIGN KEY("id_teren") REFERENCES encounters.tereny("id");

-- widoki
CREATE OR REPLACE VIEW encounters.tereny_widok AS
    SELECT nazwa, opis FROM encounters.tereny;

CREATE OR REPLACE VIEW encounters.skarby_widok AS
    SELECT nazwa, opis, rzadkosc, wartosc FROM encounters.skarby;

CREATE OR REPLACE VIEW encounters.lokacje_widok AS
    SELECT L.nazwa AS "Nazwa", L.opis AS "Opis", T.nazwa AS "Teren"
        FROM encounters.lokacje L JOIN encounters.tereny T ON L.id_teren=T.id
        ORDER BY 1 ASC;