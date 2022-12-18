INSERT INTO encounters.tereny VALUES(nazwa, opis)
    ('Góry', 'Skaliste nieprzetarte szlaki, gdzie nie tylko potwory ale i upadek z wysokości jest śmiertelny'),
    ('Las', 'Mroczne i ponure miejsce, w którym bogata roślinność potrafi przyprawić o zawał')
    ('Morze', 'Podwodna nieskończona głębia, gdzie brak powietrza nie jest jedynym zmartwieniem');

INSERT INTO encounters.lokacje VALUES(nazwa, opis, id_teren)
    ('Skellige', 'Potężny szczyt w Normandii, gdzie Thondurg stoczył bój z Yeti', 0),
    ('Moria', 'Wielka kopalnia wydrążona w górach, miejsce schronienia krasnoludów', 0);
    ('')