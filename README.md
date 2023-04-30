# Coordinates transformation
Program służy do implementacji współrzędnych wybranych przez użytkownika.
Coordinates transformation posiada możliwość implementacji wybranych współrzędnych za pomocą poniższych metod:
  xyz2blh, blh2xyz, xyz2neu, blelip2xy2000 oraz blelip2xy1992.
 # xyz2blh
  metoda zmiany współrzędnych prostokątnych (xyz) na współrzędne geodezyjne (blh)
 # blh2xyz
  metoda zmiany współrzędnych geodezyjnych (blh) na współrzędne prostokątne (xyz)
 # xyz2neu
  metoda zmiany współrzędnych protokątnych (xyz) na współrzędne topocentryczne (neu)
 # blelip2xy2000
  metoda zmiany współrzędnych z układy o wybranej elipsoidzie na współrzędne w układzie 2000
 # blelip2xy1992
  metoda zmiany współrzędnych z układy o wybranej elipsoidzie na współrzędne w układzie 1992
# Używanie programu
  ## 1.- Program można wywołać za pomocą konsoli cmd w pasku wyszukiwania, obok przycisku windows. 
  ## 2.- Po włączeniu konsoli pojawi się czarne okno, w którym należy wpisać: cd {ścieżka do folderu z projektem} - można ją skopiować z explorera plików 
  (przykładowa komenda będzie wyglądać następująco: cd C:\Users\INF\Documents\Python_projects\INF_S_4\Coordinates_transformation). 
  ## 3.- Następnie użtkownik musi wpisać komendy (wybraną przez niegotransformację) wymienione powyżej. Aby dowiedzieć się więcej na temat udostępnionych metod,
  użytkownik może wypisać help. 
  ## 4.- Użytkownik będzie miał możliwość wyboru w jaki sposób chce wgrać dane do programu. Wpisując komendę -data użytkownik decyduje się na ręczne wpisanie danych do transformacji (dane będą musiały być ułożone w określonym schemacie, patrz punkt 4.1, 4.2 oraz 4.3).
  Aby wgrać dane z pliku .txt trzeba znać lokalizację pliku tekstowego, którą należy wpisać do programu poprzedzając ją klauzulą
  -file_path {lokalizacja pliku z danymi\nazwa pliku z danymi}(przykładowa komenda będzie wyglądała następująco: -file_path C:\Users\INF\Documents\ENTRY_DATA.txt).
  W pliku tym, dane muszą być posegregowane zgodnie z poniższymi schematami:
  ### 4.1.- Dla funkcji przyjmujących 3 zmienne (xyz2blh oraz blh2xyz), dane powinny być oddzielone symbolem ';' oraz enterem co 3 wartości
        PRZYKŁAD: 1000.0;2000.0;3000.0; (pierwsza wartość oznaczać będzie współrzędną X bądź Fi, druga wartość - Y lub Lambda,a  trzecia Z lub h)
                  4000.0;5000.0;6000.0;
                  ...                   (reszta danych analogicznie)
  ### 4.2.- Dla funkcji przyjmujących 2 zmienne (blelip2xy2000 oraz blelip2xy1992), dane powinny być zapisane w ten sam sposób, lecz ze skokiem co 2
        PRZYKŁAD: 1000.0;2000.0; (pierwsza wartość oznacza Fi, a druga Lambda)
                  3000.0;4000.0;
                  ...            (reszta danych analogicznie)
  ### 4.3.- Dla funkcji xyz2neu użytkownik będzie musiał wpisać 6 wartości w każdej linijce pliku .txt (przyporządkowane konkretnym punktom)
        PRZYKŁAD: 1000.0;1000.0;1000.0;2000.0;2000.0;2000.0; (wartości 1000.0 oraz 3000.0 odpowiadają kolejno współrzędnym X, Y oraz Z zadanego punktu)
                  3000.0;3000.0;3000.0;4000.0;4000.0;4000.0; (wartości 2000.0 oraz 4000.0 odpowiadją PASSSSSSSSSSSSSSSSSSSSSSSSSSSS)
  ## 5.- Następnie użytkownik musi wybrać dla jakiej elipsoidy będą wykonywane obliczenia, aby wybrać model elipsoidy należy wpisać -model GRS80/WGS84 lub Krasowski
      (przykładowa komenda będzie wyglądać następująco: -model GRS80). Klauzula -help udostępni wiersz pomocy użytkownikowi.
  ## 6.- Po wgraniu wszystkich danych, użytkownik potwierdza przeliczenie współrzędnych wybraną transformacją przyciskiem ENTER. Wyniki transformacji zostaną zapisane w pliku tekstowym o nazwie results.txt na dysku w komputerze w tej samej lokalizacji co program. Posegregowane będą zgodnie z kolejnością i schematami wymienionymi powyżej.
               
