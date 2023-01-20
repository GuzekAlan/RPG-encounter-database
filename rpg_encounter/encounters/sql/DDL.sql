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
    "nazwa" VARCHAR(100) UNIQUE NOT NULL,
    "opis" VARCHAR(1000) NOT NULL,
    "id_lokacja" INTEGER NOT NULL,
    "id_tworca" INTEGER
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
    "nazwa" VARCHAR(100) UNIQUE NOT NULL,
    "opis" VARCHAR(1000) NOT NULL,
    "poziom_trudnosci" INTEGER NOT NULL
);
-- Osoby
CREATE TABLE encounters.osoby(
    "id" SERIAL PRIMARY KEY,
    "nazwa" VARCHAR(100) UNIQUE NOT NULL,
    "login" VARCHAR(50) UNIQUE NOT NULL,
    "haslo" VARCHAR(50) NOT NULL
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
-- Potwór - Potyczka
CREATE TABLE encounters.potwor_potyczka(
    "id_potyczka" INTEGER NOT NULL,
    "id_potwor" INTEGER NOT NULL
);

-- Klucze obce
ALTER TABLE encounters.potwory
    ADD CONSTRAINT "potwory_id_rasa_foreign"
        FOREIGN KEY("id_rasa")
        REFERENCES encounters.rasy("id")
        ON DELETE CASCADE
        NOT DEFERRABLE;
ALTER TABLE encounters.potyczki 
    ADD CONSTRAINT "potyczki_id_lokacja_foreign"
        FOREIGN KEY("id_lokacja")
        REFERENCES encounters.lokacje("id")
        ON DELETE CASCADE
        NOT DEFERRABLE,
    ADD CONSTRAINT "potyczki_id_tworca_foreign"
        FOREIGN KEY("id_tworca")
        REFERENCES encounters.osoby("id")
        ON DELETE CASCADE
        NOT DEFERRABLE;
ALTER TABLE encounters.lokacje 
    ADD CONSTRAINT "lokacje_id_teren_foreign"
        FOREIGN KEY("id_teren")
        REFERENCES encounters.tereny("id")
        ON DELETE CASCADE
        NOT DEFERRABLE;
ALTER TABLE encounters.potwor_potyczka 
    ADD CONSTRAINT "potwor_potyczka_id_potyczka_foreign"
        FOREIGN KEY("id_potyczka")
        REFERENCES encounters.potyczki("id")
        ON DELETE CASCADE
        NOT DEFERRABLE,
    ADD CONSTRAINT "potwor_potyczka_id_potwor_foreign"
        FOREIGN KEY("id_potwor")
        REFERENCES encounters.potwory("id")
        ON DELETE CASCADE
        NOT DEFERRABLE;
ALTER TABLE encounters.skarb_potyczka 
    ADD CONSTRAINT "skarb_potyczka_id_potyczka_foreign"
        FOREIGN KEY("id_potyczka")
        REFERENCES encounters.potyczki("id")
        ON DELETE CASCADE
        NOT DEFERRABLE,
    ADD CONSTRAINT "skarb_potyczka_id_skarb_foreign"
        FOREIGN KEY("id_skarb")
        REFERENCES encounters.skarby("id")
        ON DELETE CASCADE
        NOT DEFERRABLE;
ALTER TABLE encounters.pulapka_potyczka 
    ADD CONSTRAINT "pulapka_potyczka_id_potyczka_foreign"
        FOREIGN KEY("id_potyczka")
        REFERENCES encounters.potyczki("id")
        ON DELETE CASCADE
        NOT DEFERRABLE,
    ADD CONSTRAINT "pulapka_potyczka_id_pulapka_foreign"
        FOREIGN KEY("id_pulapka")
        REFERENCES encounters.pulapki("id")
        ON DELETE CASCADE
        NOT DEFERRABLE;
ALTER TABLE encounters.rasa_teren
    ADD CONSTRAINT "rasa_teren_id_rasa_foreign"
        FOREIGN KEY("id_rasa")
        REFERENCES encounters.rasy("id")
        ON DELETE CASCADE
        NOT DEFERRABLE,
    ADD CONSTRAINT "rasa_teren_id_teren_foreign"
        FOREIGN KEY("id_teren")
        REFERENCES encounters.tereny("id")
        ON DELETE CASCADE
        NOT DEFERRABLE;

-- widoki
CREATE OR REPLACE VIEW encounters.tereny_widok AS
    SELECT nazwa, opis 
        FROM encounters.tereny
        ORDER BY 1 ASC;

CREATE OR REPLACE VIEW encounters.skarby_widok AS
    SELECT nazwa, opis, rzadkosc, wartosc 
        FROM encounters.skarby
        ORDER BY 4 DESC, 1 ASC;

CREATE OR REPLACE VIEW encounters.lokacje_widok AS
    SELECT L.nazwa, L.opis, T.nazwa AS "teren"
        FROM encounters.lokacje L JOIN encounters.tereny T ON L.id_teren=T.id
        ORDER BY 1 ASC;

CREATE OR REPLACE VIEW encounters.rasy_widok AS
    SELECT R.nazwa, R.opis, STRING_AGG(T.nazwa, ',') as "tereny"
        FROM encounters.rasy R LEFT JOIN encounters.rasa_teren RT ON RT.id_rasa=R.id
        LEFT JOIN encounters.tereny T ON RT.id_teren=T.id
        GROUP BY R.id
        ORDER BY 1 ASC;

CREATE OR REPLACE VIEW encounters.potwory_widok AS
    SELECT P.nazwa, P.opis, P.poziom_trudnosci, R.nazwa AS "rasa", STRING_AGG(T.nazwa, ',') as "tereny"
        FROM encounters.potwory P JOIN encounters.rasy R ON P.id_rasa=R.id
        LEFT JOIN encounters.rasa_teren RT ON RT.id_rasa=R.id
        LEFT JOIN encounters.tereny T ON RT.id_teren=T.id
        GROUP BY P.id, R.id
        ORDER BY 3 DESC, 1 ASC;

CREATE OR REPLACE VIEW encounters.pulapki_widok AS
    SELECT nazwa, opis, poziom_trudnosci
        FROM encounters.pulapki
        ORDER BY 3 DESC;

CREATE OR REPLACE VIEW encounters.poziom_trudnosci AS
    SELECT P.id, SUM(Pot.poziom_trudnosci + Pul.poziom_trudnosci) AS poziom
        FROM encounters.potyczki P
            LEFT JOIN encounters.potwor_potyczka PotP ON PotP.id_potyczka=P.id
            JOIN encounters.potwory Pot ON Pot.id=PotP.id_potwor
            LEFT JOIN encounters.pulapka_potyczka PulP ON PulP.id_potyczka=P.id
            JOIN encounters.pulapki Pul ON Pul.id=PulP.id_pulapka
        GROUP BY P.id;

CREATE OR REPLACE VIEW encounters.potyczki_pulapki_widok AS
    SELECT P.id, STRING_AGG(Pul.nazwa, ',') AS "pulapki"
        FROM encounters.potyczki P 
            LEFT JOIN encounters.pulapka_potyczka PulP ON PulP.id_potyczka=P.id
            JOIN encounters.pulapki Pul ON Pul.id=PulP.id_pulapka
        GROUP BY P.id;

CREATE OR REPLACE VIEW encounters.potyczki_potwory_widok AS
    SELECT P.id, STRING_AGG(Pot.nazwa, ',') AS "potwory"
        FROM encounters.potyczki P 
            LEFT JOIN encounters.potwor_potyczka PotP ON PotP.id_potyczka=P.id
            JOIN encounters.potwory Pot ON Pot.id=PotP.id_potwor
        GROUP BY P.id;

CREATE OR REPLACE VIEW encounters.potyczki_skarby_widok AS
    SELECT P.id, STRING_AGG(S.nazwa, ',') AS "skarby"
        FROM encounters.potyczki P 
            LEFT JOIN encounters.skarb_potyczka SP ON SP.id_potyczka=P.id
            JOIN encounters.skarby S ON S.id=SP.id_skarb
        GROUP BY P.id;



-- Wyzwalacze
CREATE OR REPLACE FUNCTION rzadkosc_skarbu_funkcja()
    RETURNS TRIGGER
    AS $$
    BEGIN
        NEW.rzadkosc := UPPER(NEW.rzadkosc);
        RETURN NEW;
    END;
    $$ LANGUAGE 'plpgsql';

CREATE TRIGGER rzadkosc_skarbu_wyzwalacz
    BEFORE INSERT OR UPDATE ON encounters.skarby
    FOR EACH ROW 
    EXECUTE PROCEDURE rzadkosc_skarbu_funkcja();

-- Funkcje

CREATE OR REPLACE FUNCTION usun_potyczke(index BIGINT, tworca VARCHAR)
    RETURNS VOID AS
    $$
    BEGIN
            IF tworca = 'ADMIN' OR index IN
                ( SELECT id FROM encounters.potyczki
                          WHERE id_tworca = (SELECT id FROM encounters.osoby WHERE nazwa = tworca) )
            THEN
                DELETE FROM encounters.potyczki WHERE id = index;
            END IF;
    END;
    $$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION encounters.pokaz_potyczki(tworca VARCHAR)
  RETURNS TABLE(nazwa VARCHAR, opis VARCHAR, lokacja VARCHAR, potwory TEXT, pulapki TEXT, skarby TEXT, pt BIGINT, t VARCHAR, id INTEGER) AS
    $$
    BEGIN
            IF tworca = 'ADMIN'
            THEN
                RETURN QUERY
                SELECT P.nazwa, P.opis, L.nazwa AS "lokacja", Pot.potwory, Pul.pulapki, S.skarby, PT.poziom, T.nazwa AS "tworca", P.id
                    FROM encounters.potyczki P
                        LEFT JOIN encounters.lokacje L ON P.id_lokacja=L.id
                        LEFT JOIN encounters.potyczki_potwory_widok Pot ON Pot.id=P.id
                        LEFT JOIN encounters.potyczki_pulapki_widok Pul ON Pul.id=P.id
                        LEFT JOIN encounters.potyczki_skarby_widok S ON S.id=P.id
                        LEFT JOIN encounters.poziom_trudnosci PT ON PT.id=P.id
                        LEFT JOIN encounters.osoby T ON T.id=P.id_tworca
                    ORDER BY 1 ASC ;
            ELSE
                RETURN QUERY
                SELECT P.nazwa, P.opis, L.nazwa AS "lokacja", Pot.potwory, Pul.pulapki, S.skarby, PT.poziom, T.nazwa AS "tworca", P.id
                    FROM encounters.potyczki P
                        LEFT JOIN encounters.lokacje L ON P.id_lokacja=L.id
                        LEFT JOIN encounters.potyczki_potwory_widok Pot ON Pot.id=P.id
                        LEFT JOIN encounters.potyczki_pulapki_widok Pul ON Pul.id=P.id
                        LEFT JOIN encounters.potyczki_skarby_widok S ON S.id=P.id
                        LEFT JOIN encounters.poziom_trudnosci PT ON PT.id=P.id
                        LEFT JOIN encounters.osoby T ON T.id=P.id_tworca
                    WHERE T.nazwa = tworca
                    ORDER BY 1 ASC ;
            END IF;
    END;
    $$ LANGUAGE plpgsql;