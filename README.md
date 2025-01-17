# Diferenčný regulátor teploty

**Tento projekt pozostáva z dvoch kódov a knižnice pre ovládanie displeja.**  

*adresy.py* sa používa na identifikáciu senzorov pripojených k zariadeniu.  
*main.py* vykonáva hlavný program na meranie teplôt, výpočet rozdielu a zobrazenie.  
*sh1106.py* knižnica na ovládanie OLED displeja, ktorý zobrazuje teploty a stav systému.  

# Popis súborov projektu

## 1. `adresy.py`

Tento skript inicializuje teplotné senzory DS18B20 pripojené k zariadeniu cez OneWire protokol. Slúži na identifikáciu senzorov pripojených k zariadeniu.

### Postup:
Inicializuje GPIO4 ako vstup pre teplotné senzory.
Vytvorí DS18B20 objekt a načíta senzory pripojené k zbernici.
Zobrazí adresy senzorov (v hexadecimálnom formáte) pre ďalšie použitie.

---

## 2. `main.py`

Tento skript vykonáva hlavný program, hlavná logika pre spracovanie údajov zo senzorov a vizualizáciu. Číta teploty z dvoch senzorov DS18B20 a zobrazuje ich rozdiel na OLED displeji a takisto riadi LED diódu na základe rozdielu teplôt.

### Postup:
Inicialuzujeme GPIO piny pre senzory, OLED displej a LED a zadáme dve pevne zadané adresy senzorov, ktoré sme zistili s programom adresy.py.  

**Hlavný cyklus:**
  - Meria teploty z dvoch senzorov.
  - Vypočíta rozdiel teplôt a na základe jeho hodnoty a zapína alebo vypína LED (ak rozdiel prekročí 3 °C alebo klesne pod 1 °C).
  - Zobrazuje hodnoty na OLED displeji (teploty, rozdiel, stav LED).

---

## 3. `sh1106.py`

Obsahuje knižnicu pre ovládanie OLED displejov typu SH1106 cez I2C alebo SPI.

---

## Použité knižnice

**machine**		– Na prácu s GPIO pinmi, I2C a hardvérom.  
**Pin**				– Na konfiguráciu GPIO pinov.  
**SoftI2C**		– Na komunikáciu cez I2C (pre OLED displej).  
**sh1106**		– Na prácu s OLED displejom SH1106.  
**time**			– Na časové oneskorenia.  
**onewire**		– Na prácu so zbernicou 1-Wire (pre senzory DS18B20).  
**ds18x20**		– Na meranie teploty cez DS18B20 senzory.

## 
