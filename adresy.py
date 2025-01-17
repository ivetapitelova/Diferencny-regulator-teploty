from machine import Pin
import time
import onewire
import ds18x20

# Konfigurácia pinu pre OneWire
dat = Pin(4)  # Teplotný senzor pripojený na GPIO4

# Inicializácia teplotného senzora DS18B20
ds = ds18x20.DS18X20(onewire.OneWire(dat))

# Unikátne adresy senzorov (získané skenovaním zbernice)
T1_address = b'\x28\xFF\x4C\x6B\x93\x16\x03\x7C'  # 
T2_address = b'\x28\xFF\x6A\x7C\x93\x16\x01\x23'  # 

# Zoznam všetkých senzorov na zbernici
roms = ds.scan()
print("Nájdené senzory:")
for rom in roms:
    print(''.join(f'{b:02X}' for b in rom))
