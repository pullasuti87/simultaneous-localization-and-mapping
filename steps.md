# Visuaalisen odometrian vaiheet ja koodin selitykset

### 1. Kirjastot ja alustus
*   **`import cv2` & `import numpy`**: Työkalut kuvankäsittelyyn ja matriisilaskentaan. Kameran asento ja liikkeet tallennetaan **matriiseina**, ja Numpy on paras työkalu niiden käsittelyyn.
*   **`SCALE` & `OFFSET`**: 
    *   Kameran liike on todellisessa maailmassa pientä (esim. 0.2 yksikköä). Skaala kerrotaan tällä arvolla, jotta se näkyisi ruudulla pikseleinä.
    *   Offset siirtää piirroksen alkupisteen keskelle ikkunaa.

---

### 2. Kameramatriisi `K` (Intrinsic Matrix)
Kameramatriisi on algoritmin "silmälasi-resepti". Se kuvaa kameran sisäisiä ominaisuuksia.

*   **Rakenne (3x3-matriisi):**
    *   **fx, fy (Focal Length):** Polttoväli pikseleinä. Kertoo, kuinka paljon valo taittuu linssin läpi.
    *   **cx, cy (Principal Point):** Kuvan optinen keskipiste.
*   **Miksi se on kriittinen?** Se muuntaa "pikselimaailman" "metrimaailmaksi". Ilman tätä ohjelma ei tiedä, johtuuko pisteen liike ruudulla kameran suuresta liikkeestä vai linssin laajakulmaisuudesta.

---

### 3. Piirteiden etsiminen ja vertailutyökalut
*   **`cv2.ORB_create(nfeatures=1000)`**:
    *   **ORB** etsii kuvasta "mielenkiintoisia" kohtia (nurkkia, tekstuureja).
    *   `nfeatures=1000` rajoittaa pisteiden määrää laskentatehon säästämiseksi.
*   **`cv2.BFMatcher(cv2.NORM_HAMMING)`**:
    *   **Brute Force Matcher** yhdistää kahden eri kuvan pisteet vertaamalla niiden digitaalisia "sormenjälkiä" (descriptors).

---

### 4. Pose-matriisi `v` (Extrinsic Matrix)
Pose-matriisi kertoo kameran tarkan asennon ja sijainnin maailmankoordinaatistossa.

*   **Rakenne (4x4 homogeeninen matriisi):**
    *   **R (Rotation):** Vasen 3x3-osa kertoo, mihin suuntaan kamera on kääntynyt (X, Y, Z -akselit).
    *   **T (Translation):** Oikea sarake (Tx, Ty, Tz) kertoo kameran sijainnin eli liikkeen alkupisteestä.
*   **Kumulatiivisuus:** Aluksi käytetään **identiteettimatriisia** (`numpy.eye(4)`), joka edustaa nollapistettä. Uusi laskettu liike kerrotaan aina edellisellä matriisilla, jolloin kulkureitti "ketjuttuu".

---

### 5. Kuvien esikäsittely ja kohina (Noise)
Tietokonenäössä **kohina** tarkoittaa virheellistä dataa, joka vaikeuttaa liikkeen laskemista.

*   **`cv2.cvtColor(..., cv2.COLOR_BGR2GRAY)`**:
    *   Muuntaa kuvan harmaasävyksi. Värit vaatisivat 3x enemmän laskentatehoa, eivätkä ne auta pisteiden tunnistuksessa. Tämä vähentää laskennallista kohinaa.
*   **Kohinan tyypit:**
    *   **Sensorikohina:** Kennon rakeisuus hämärässä.
    *   **Outliers:** Liikkuvat kohteet (esim. ohi ajava auto), jotka hämäävät algoritmin luulemaan, että kamera liikkuu, vaikka vain kohde liikkuu.
    *   **Drift:** Pienet pyöristysvirheet, jotka kertyvät ja saavat reitin "valumaan" vinoon ajan myötä.

---

### 6. Pisteiden yhdistäminen ja suodatus
*   **`bf.knnMatch(..., k=2)`**: Etsii kaksi parasta ehdokasta jokaiselle pisteelle.
*   **Lowe's Ratio Test (`distance < 0.75 * distance`)**:
    *   Tämä on tärkein **kohinan suodatin**. Jos paras osuma ei ole selvästi parempi kuin toiseksi paras, piste hylätään epävarmana. Vain puhtaat ja selkeät osumat hyväksytään listaan `t`.

---

### 7. Koordinaattien erottelu (`pt1` ja `pt2`)
Tässä siirrytään kuvankäsittelystä geometriaan.
*   **`.pt`**: Poimii pisteen todelliset pikselikoordinaatit (x, y).
*   **`reshape(-1, 1, 2)`**: 
    *   Muuntaa koordinaatit Numpy-taulukoksi, jota OpenCV:n matemaattiset funktiot (kuten asennon laskenta) vaativat. Reshape varmistaa, että matriisilaskenta kohdistuu numeroihin oikeassa järjestyksessä.

---

### 8. Visualisointi (`draw`-funktio)
*   **X- ja Z-akselit**: Poimitaan Pose-matriisista arvot `v[0, 3]` (X = sivuttaissuunta) ja `v[2, 3]` (Z = syvyyssuunta).
*   **Lintuperspektiivi**: Piirtämällä nämä koordinaatit mustalle pohjalle saamme reaaliaikaisen kartan siitä, missä kamera liikkuu suhteessa aloituspisteeseen.

---

### 9. Päivityslogiikka
*   **`gray_frame1 = gray_frame2`**:
    *   Siirtää nykyisen tiedon "vanhaksi" tiedoksi. Tämä mahdollistaa jatkuvan liikkeen seurannan ruudusta toiseen (ketjureaktio).