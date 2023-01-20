BEGIN;
INSERT INTO encounters.tereny(nazwa, opis) VALUES
    ('Góry', 'Skaliste nieprzetarte szlaki, gdzie nie tylko potwory ale i upadek z wysokości jest śmiertelny'),
    ('Las', 'Mroczne i ponure miejsce, w którym bogata roślinność potrafi przyprawić o zawał'),
    ('Morze', 'Podwodna nieskończona głębia, gdzie brak powietrza nie jest jedynym zmartwieniem');

INSERT INTO encounters.lokacje(nazwa, opis, id_teren) VALUES
    ('Skellige', 'Potężny szczyt w Normandii, gdzie Thondurg stoczył bój z Yeti', 1),
    ('Moria', 'Wielka kopalnia wydrążona w górach, miejsce schronienia krasnoludów', 1),
    ('Loch Ness', 'Pradawny angielski akwen. Uwaga na Kłody', 3),
    ('Sherwood', 'Domek dla zbirów, ale tych dobrych co kradną biednym i bogatym', 2),
    ('Ironwood', 'Bóg wojny w tym lasie swój toporek wystrógał', 2),
    ('Ósme Może', 'Może istnieje a może nie, znajduje się za siedmioma morzami, za siedmioma górami', 3);

INSERT INTO encounters.pulapki(nazwa, opis, poziom_trudnosci) VALUES
    ('Zapadnia', 'Dziura w podłodze, której nie widać gołym okiem', 2),
    ('Strzały', 'Spotykane w zamkniętych pomieszczeniach, lecą ze ścian', 4),
    ('Magiczny portal', 'Teleportuje ofiarę w bardzo odległe miejsce, często bardzo groźne', 8);

INSERT INTO encounters.skarby(nazwa, opis, rzadkosc, wartosc) VALUES
    ('Excalibur', 'Historyczny miecz króla Artura mogący być niewidzialnym', 'Legendarny', 10000),
    ('Mjolnir', 'Młotek boskiego Torusa pozwalający mający tylko jedną stronę', 'Rzadki', 5000),
    ('Skrzynia', 'Wielkie grube pudełko mające duuuużo złota', 'Pospolity', 200),
    ('Buty', 'Popularny średniowieczny środek transportu posiadający skórzaną tapicerkę', 'Pospolity', 3);

INSERT INTO encounters.rasy(nazwa, opis) VALUES 
    ('Ludzie', 'Średniego rozmiaru bestie mówiące po Polsku i Angieslku. Nieprzyjemne typy'),
    ('Syrenki', 'Piękne kobiety od pasa w górę, a od pasa w dół mają duży ogon. Pięknie śpiewają i zjadają marynarzy'),
    ('Smoki', 'Dostojne gady, skrzydlate jak i ogniowładne. Kochają złoto'),
    ('Gobliny', 'Małe stworzenia żyjące w wielkich skupiskach.');

INSERT INTO encounters.rasa_teren VALUES
    (1, 1),
    (1, 2),
    (2, 3),
    (3, 1),
    (4, 1),
    (4, 2);

INSERT INTO encounters.potwory(nazwa, opis, poziom_trudnosci, id_rasa) VALUES 
    ('Hobgoblin', 'Duży goblin. Ma maczugę. UgaUga.', 3, 4),
    ('Wywerna', 'Mały nierozwinięty smok, który nie potrafi zionąć ogniem', 4, 3),
    ('Mała Syrenka', 'W sumie to nie potwór ale księżniczka ale nadal obrażenia zadawać może', 1, 2);


INSERT INTO encounters.osoby(nazwa, login, haslo) VALUES
    ('ADMIN', 'ADMIN', 'ADMIN'),
    ('Alan', 'alan', 'alan'),
    ('GMTomek', 'tomekthebest', 'qwerty');

INSERT INTO encounters.potyczki(nazwa, opis, id_lokacja, id_tworca) VALUES
    ('Potężny bój', 'Wielka bitka z potężnymi wrogami', 1, 2),
    ('Podwodna przygoda', 'Walka na jeziorze a także pod nim', 3, 2);

INSERT INTO encounters.pulapka_potyczka(id_potyczka, id_pulapka) VALUES
    (1, 2),
    (1, 1),
    (2, 3);

INSERT INTO encounters.skarb_potyczka(id_potyczka, id_skarb) VALUES
    (1, 1),
    (1, 2),
    (2, 1);

INSERT INTO encounters.potwor_potyczka(id_potyczka, id_potwor) VALUES
    (1, 3),
    (1, 2),
    (1, 1),
    (2, 1);

COMMIT;