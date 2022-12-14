CREATE TABLE "potwory"(
    "id" INTEGER NOT NULL,
    "nazwa" VARCHAR(255) NOT NULL,
    "opis" VARCHAR(255) NOT NULL,
    "poziom_trudnosci" INTEGER NOT NULL,
    "id_rasa" INTEGER NOT NULL
);
CREATE INDEX "potwory_nazwa_index" ON
    "potwory"("nazwa");
CREATE INDEX "potwory_poziom_trudnosci_index" ON
    "potwory"("poziom_trudnosci");
ALTER TABLE
    "potwory" ADD PRIMARY KEY("id");
CREATE TABLE "tereny"(
    "id" INTEGER NOT NULL,
    "nazwa" VARCHAR(255) NOT NULL,
    "opis" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "tereny" ADD PRIMARY KEY("id");
CREATE TABLE "potyczki"(
    "id" INTEGER NOT NULL,
    "tytul" VARCHAR(255) NOT NULL,
    "opis" VARCHAR(255) NOT NULL,
    "id_lokacja" INTEGER NOT NULL,
    "poziom_trudnosci" INTEGER NOT NULL,
    "id_tworca" INTEGER NOT NULL
);
CREATE INDEX "potyczki_id_tworca_index" ON
    "potyczki"("id_tworca");
CREATE INDEX "potyczki_tytul_index" ON
    "potyczki"("tytul");
ALTER TABLE
    "potyczki" ADD PRIMARY KEY("id");
CREATE TABLE "skarby"(
    "id" INTEGER NOT NULL,
    "nazwa" INTEGER NOT NULL,
    "opis" VARCHAR(255) NOT NULL,
    "rzadkosc" INTEGER NOT NULL,
    "wartosc" INTEGER NOT NULL
);
CREATE INDEX "skarby_rzadkosc_index" ON
    "skarby"("rzadkosc");
CREATE INDEX "skarby_nazwa_index" ON
    "skarby"("nazwa");
ALTER TABLE
    "skarby" ADD PRIMARY KEY("id");
CREATE TABLE "rasy"(
    "id" INTEGER NOT NULL,
    "nazwa" VARCHAR(255) NOT NULL,
    "opis" VARCHAR(255) NOT NULL,
    "id_teren" INTEGER NOT NULL
);
ALTER TABLE
    "rasy" ADD PRIMARY KEY("id");
CREATE TABLE "potwor_potyczka"(
    "id" INTEGER NOT NULL,
    "id_potyczka" INTEGER NOT NULL,
    "id_potwor" INTEGER NOT NULL
);
ALTER TABLE
    "potwor_potyczka" ADD PRIMARY KEY("id");
CREATE TABLE "lokacje"(
    "id" INTEGER NOT NULL,
    "nazwa" INTEGER NOT NULL,
    "opis" VARCHAR(255) NOT NULL,
    "id_teren" INTEGER NOT NULL
);
ALTER TABLE
    "lokacje" ADD PRIMARY KEY("id");
CREATE TABLE "skarb_potyczka"(
    "id" INTEGER NOT NULL,
    "id_potyczka" INTEGER NOT NULL,
    "id_skarb" INTEGER NOT NULL
);
ALTER TABLE
    "skarb_potyczka" ADD PRIMARY KEY("id");
CREATE TABLE "pułapki"(
    "id" INTEGER NOT NULL,
    "nazwa" VARCHAR(255) NOT NULL,
    "opis" VARCHAR(255) NOT NULL,
    "poziom_trudnosci" INTEGER NOT NULL
);
ALTER TABLE
    "pułapki" ADD PRIMARY KEY("id");
CREATE TABLE "pułapka_potyczka"(
    "id" INTEGER NOT NULL,
    "id_potyczka" INTEGER NOT NULL,
    "id_pułapka" INTEGER NOT NULL
);
ALTER TABLE
    "pułapka_potyczka" ADD PRIMARY KEY("id");
CREATE TABLE "osoby"(
    "id" INTEGER NOT NULL,
    "nazwa" VARCHAR(255) NOT NULL,
    "login" VARCHAR(255) NOT NULL,
    "haslo" VARCHAR(255) NOT NULL
);
CREATE INDEX "osoby_nazwa_index" ON
    "osoby"("nazwa");
CREATE INDEX "osoby_login_index" ON
    "osoby"("login");
ALTER TABLE
    "osoby" ADD PRIMARY KEY("id");
CREATE TABLE "rasa_teren"(
    "id" INTEGER NOT NULL,
    "id_rasa" INTEGER NOT NULL,
    "id_teren" INTEGER NOT NULL
);
ALTER TABLE
    "rasa_teren" ADD PRIMARY KEY("id");
CREATE TABLE "uprawnienia"(
    "id" INTEGER NOT NULL,
    "nazwa" VARCHAR(255) NOT NULL,
    "typ" VARCHAR(255) NOT NULL
);
CREATE INDEX "uprawnienia_typ_index" ON
    "uprawnienia"("typ");
ALTER TABLE
    "uprawnienia" ADD PRIMARY KEY("id");
CREATE TABLE "uprawnienia_osoby"(
    "id" INTEGER NOT NULL,
    "id_uprawniennie" INTEGER NOT NULL,
    "id_osoba" INTEGER NOT NULL
);
ALTER TABLE
    "uprawnienia_osoby" ADD PRIMARY KEY("id");
ALTER TABLE
    "potwory" ADD CONSTRAINT "potwory_id_rasa_foreign" FOREIGN KEY("id_rasa") REFERENCES "rasy"("id");
ALTER TABLE
    "potwor_potyczka" ADD CONSTRAINT "potwor_potyczka_id_potyczka_foreign" FOREIGN KEY("id_potyczka") REFERENCES "potyczki"("id");
ALTER TABLE
    "skarb_potyczka" ADD CONSTRAINT "skarb_potyczka_id_potyczka_foreign" FOREIGN KEY("id_potyczka") REFERENCES "potyczki"("id");
ALTER TABLE
    "pułapka_potyczka" ADD CONSTRAINT "pułapka_potyczka_id_potyczka_foreign" FOREIGN KEY("id_potyczka") REFERENCES "potyczki"("id");
ALTER TABLE
    "potyczki" ADD CONSTRAINT "potyczki_id_lokacja_foreign" FOREIGN KEY("id_lokacja") REFERENCES "lokacje"("id");
ALTER TABLE
    "skarb_potyczka" ADD CONSTRAINT "skarb_potyczka_id_skarb_foreign" FOREIGN KEY("id_skarb") REFERENCES "skarby"("id");
ALTER TABLE
    "potwor_potyczka" ADD CONSTRAINT "potwor_potyczka_id_potwor_foreign" FOREIGN KEY("id_potwor") REFERENCES "potwory"("id");
ALTER TABLE
    "lokacje" ADD CONSTRAINT "lokacje_id_teren_foreign" FOREIGN KEY("id_teren") REFERENCES "tereny"("id");
ALTER TABLE
    "pułapka_potyczka" ADD CONSTRAINT "pułapka_potyczka_id_pułapka_foreign" FOREIGN KEY("id_pułapka") REFERENCES "pułapki"("id");
ALTER TABLE
    "potyczki" ADD CONSTRAINT "potyczki_id_tworca_foreign" FOREIGN KEY("id_tworca") REFERENCES "osoby"("id");
ALTER TABLE
    "uprawnienia_osoby" ADD CONSTRAINT "uprawnienia_osoby_id_uprawniennie_foreign" FOREIGN KEY("id_uprawniennie") REFERENCES "uprawnienia"("id");
ALTER TABLE
    "uprawnienia_osoby" ADD CONSTRAINT "uprawnienia_osoby_id_osoba_foreign" FOREIGN KEY("id_osoba") REFERENCES "osoby"("id");
ALTER TABLE
    "rasa_teren" ADD CONSTRAINT "rasa_teren_id_rasa_foreign" FOREIGN KEY("id_rasa") REFERENCES "rasy"("id");
ALTER TABLE
    "rasa_teren" ADD CONSTRAINT "rasa_teren_id_teren_foreign" FOREIGN KEY("id_teren") REFERENCES "tereny"("id");