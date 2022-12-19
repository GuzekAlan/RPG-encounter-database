DROP SCHEMA IF EXISTS encounters CASCADE;
CREATE SCHEMA encounters;
-- Potwory
CREATE TABLE encounters.potwory(
    "id" SERIAL NOT NULL ,
    "nazwa" VARCHAR(100) NOT NULL,
    "opis" VARCHAR(1000) NOT NULL,
    "poziom_trudnosci" INTEGER NOT NULL,
    "id_rasa" INTEGER NOT NULL
);
CREATE INDEX "potwory_nazwa_index" ON
    encounters.potwory("nazwa");
CREATE INDEX "potwory_poziom_trudnosci_index" ON
    encounters.potwory("poziom_trudnosci");
ALTER TABLE
    encounters.potwory ADD PRIMARY KEY("id");
-- Tereny
CREATE TABLE encounters.tereny(
    "id" SERIAL NOT NULL,
    "nazwa" VARCHAR(100) NOT NULL,
    "opis" VARCHAR(1000) NOT NULL
);
ALTER TABLE
    encounters.tereny ADD PRIMARY KEY("id");
-- Potyczki
CREATE TABLE encounters.potyczki(
    "id" SERIAL NOT NULL,
    "tytul" VARCHAR(100) NOT NULL,
    "opis" VARCHAR(1000) NOT NULL,
    "id_lokacja" INTEGER NOT NULL,
    "id_tworca" INTEGER NOT NULL
);
CREATE INDEX "potyczki_id_tworca_index" ON
    encounters.potyczki("id_tworca");
CREATE INDEX "potyczki_tytul_index" ON
    encounters.potyczki("tytul");
ALTER TABLE
    encounters.potyczki ADD PRIMARY KEY("id");
-- Skarby
CREATE TABLE encounters.skarby(
    "id" SERIAL NOT NULL,
    "nazwa" VARCHAR(100) NOT NULL,
    "opis" VARCHAR(1000) NOT NULL,
    "rzadkosc" VARCHAR(100) NOT NULL,
    "wartosc" INTEGER NOT NULL
);
CREATE INDEX "skarby_rzadkosc_index" ON
    encounters.skarby("rzadkosc");
CREATE INDEX "skarby_nazwa_index" ON
    encounters.skarby("nazwa");
ALTER TABLE
    encounters.skarby ADD PRIMARY KEY("id");
-- Rasy
CREATE TABLE encounters.rasy(
    "id" SERIAL NOT NULL,
    "nazwa" VARCHAR(100) NOT NULL,
    "opis" VARCHAR(1000) NOT NULL,
    "id_teren" INTEGER NOT NULL
);
ALTER TABLE
    encounters.rasy ADD PRIMARY KEY("id");
-- Potwór - Potyczka
CREATE TABLE encounters.potwor_potyczka(
    "id" SERIAL NOT NULL,
    "id_potyczka" INTEGER NOT NULL,
    "id_potwor" INTEGER NOT NULL
);
ALTER TABLE
    encounters.potwor_potyczka ADD PRIMARY KEY("id");
-- Lokacje
CREATE TABLE encounters.lokacje(
    "id" SERIAL NOT NULL,
    "nazwa" VARCHAR(100) NOT NULL,
    "opis" VARCHAR(1000) NOT NULL,
    "id_teren" INTEGER NOT NULL
);
ALTER TABLE
    encounters.lokacje ADD PRIMARY KEY("id");
-- Skarb - Potyczka
CREATE TABLE encounters.skarb_potyczka(
    "id" SERIAL NOT NULL,
    "id_potyczka" INTEGER NOT NULL,
    "id_skarb" INTEGER NOT NULL
);
ALTER TABLE
    encounters.skarb_potyczka ADD PRIMARY KEY("id");
-- Pułapki
CREATE TABLE encounters.pulapki(
    "id" SERIAL NOT NULL,
    "nazwa" VARCHAR(100) NOT NULL,
    "opis" VARCHAR(1000) NOT NULL,
    "poziom_trudnosci" INTEGER NOT NULL
);
ALTER TABLE
    encounters.pulapki ADD PRIMARY KEY("id");
-- Pułapka - Potyczka
CREATE TABLE encounters.pulapka_potyczka(
    "id" SERIAL NOT NULL,
    "id_potyczka" INTEGER NOT NULL,
    "id_pulapka" INTEGER NOT NULL
);
ALTER TABLE
    encounters.pulapka_potyczka ADD PRIMARY KEY("id");
-- Osoby
CREATE TABLE encounters.osoby(
    "id" SERIAL NOT NULL,
    "nazwa" VARCHAR(100) NOT NULL,
    "login" VARCHAR(50) NOT NULL,
    "haslo" VARCHAR(50) NOT NULL
);
CREATE INDEX "osoby_nazwa_index" ON
    encounters.osoby("nazwa");
CREATE INDEX "osoby_login_index" ON
    encounters.osoby("login");
ALTER TABLE
    encounters.osoby ADD PRIMARY KEY("id");
-- Rasa - Teren
CREATE TABLE encounters.rasa_teren(
    "id" SERIAL NOT NULL,
    "id_rasa" INTEGER NOT NULL,
    "id_teren" INTEGER NOT NULL
);
ALTER TABLE
    encounters.rasa_teren ADD PRIMARY KEY("id");
-- Uprawnienia
CREATE TABLE encounters.uprawnienia(
    "id" SERIAL NOT NULL,
    "nazwa" VARCHAR(100) NOT NULL,
    "typ" VARCHAR(100) NOT NULL
);
ALTER TABLE
    encounters.uprawnienia ADD PRIMARY KEY("id");
-- Uprawnienia - Osoby
CREATE TABLE encounters.uprawnienia_osoby(
    "id" SERIAL NOT NULL,
    "id_uprawniennie" INTEGER NOT NULL,
    "id_osoba" INTEGER NOT NULL
);
ALTER TABLE
    encounters.uprawnienia_osoby ADD PRIMARY KEY("id");
ALTER TABLE
    encounters.potwory ADD CONSTRAINT "potwory_id_rasa_foreign" FOREIGN KEY("id_rasa") REFERENCES encounters.rasy("id");
ALTER TABLE
    encounters.potwor_potyczka ADD CONSTRAINT "potwor_potyczka_id_potyczka_foreign" FOREIGN KEY("id_potyczka") REFERENCES encounters.potyczki("id");
ALTER TABLE
    encounters.skarb_potyczka ADD CONSTRAINT "skarb_potyczka_id_potyczka_foreign" FOREIGN KEY("id_potyczka") REFERENCES encounters.potyczki("id");
ALTER TABLE
    encounters.pulapka_potyczka ADD CONSTRAINT "pułapka_potyczka_id_potyczka_foreign" FOREIGN KEY("id_potyczka") REFERENCES encounters.potyczki("id");
ALTER TABLE
    encounters.potyczki ADD CONSTRAINT "potyczki_id_lokacja_foreign" FOREIGN KEY("id_lokacja") REFERENCES encounters.lokacje("id");
ALTER TABLE
    encounters.skarb_potyczka ADD CONSTRAINT "skarb_potyczka_id_skarb_foreign" FOREIGN KEY("id_skarb") REFERENCES encounters.skarby("id");
ALTER TABLE
    encounters.potwor_potyczka ADD CONSTRAINT "potwor_potyczka_id_potwor_foreign" FOREIGN KEY("id_potwor") REFERENCES encounters.potwory("id");
ALTER TABLE
    encounters.lokacje ADD CONSTRAINT "lokacje_id_teren_foreign" FOREIGN KEY("id_teren") REFERENCES encounters.tereny("id");
ALTER TABLE
    encounters.pulapka_potyczka ADD CONSTRAINT "pułapka_potyczka_id_pułapka_foreign" FOREIGN KEY("id_pulapka") REFERENCES encounters.pulapki("id");
ALTER TABLE
    encounters.potyczki ADD CONSTRAINT "potyczki_id_tworca_foreign" FOREIGN KEY("id_tworca") REFERENCES encounters.osoby("id");
ALTER TABLE
    encounters.uprawnienia_osoby ADD CONSTRAINT "uprawnienia_osoby_id_uprawniennie_foreign" FOREIGN KEY("id_uprawniennie") REFERENCES encounters.uprawnienia("id");
ALTER TABLE
    encounters.uprawnienia_osoby ADD CONSTRAINT "uprawnienia_osoby_id_osoba_foreign" FOREIGN KEY("id_osoba") REFERENCES encounters.osoby("id");
ALTER TABLE
    encounters.rasa_teren ADD CONSTRAINT "rasa_teren_id_rasa_foreign" FOREIGN KEY("id_rasa") REFERENCES encounters.rasy("id");
ALTER TABLE
    encounters.rasa_teren ADD CONSTRAINT "rasa_teren_id_teren_foreign" FOREIGN KEY("id_teren") REFERENCES encounters.tereny("id");