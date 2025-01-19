from machine import Pin, SoftI2C
import sh1106
import time
import machine
import onewire
import ds18x20

# Konfigurácia pinov pre I2C a OneWire
dat = machine.Pin(4)       # Teplotný senzor pripojený na GPIO4
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)  # Inicializácia I2C pre OLED display

# Inicializácia OLED displeja
lcd = sh1106.SH1106_I2C(128, 64, i2c)  # Vytvorenie objektu pre LCD s rozmermi 128x64

# Inicializácia teplotného senzora DS18B20
ds = ds18x20.DS18X20(onewire.OneWire(dat))  # Vytvorenie OneWire objektu pre DS18B20
roms = ds.scan()  # Vyhľadanie zariadení na zbernici

# Unikátne adresy senzorov (získané skenovaním zbernice)
T1_address = b'\x28\x7B\x65\x36\x00\x00\x00\xFC'  # adresa senzora 287B6536000000FC
T2_address = b'\x28\x43\xAC\x37\x00\x00\x00\xEE'  # adresa senzora 2843AC37000000EE

# Inicializácia LED na GPIO23 ako výstup
led = Pin(23, Pin.OUT)

# Premenná pre sledovanie stavu LED (či už bola zapnutá)
led_on = False

# Overenie, či sú pripojené oba senzory
#if T1_address not in roms:
#    print("Senzor T1 nie je pripojený!")
#if T2_address not in roms:
#    print("Senzor T2 nie je pripojený!")

# Hlavná slučka programu
try:
    while True:
        ds.convert_temp()  # Spustenie merania teploty
        time.sleep_ms(750)  # Čas potrebný na zmeranie teploty (min. 750 ms)

        # Čítanie teplôt pre pevne priradené senzory T1 a T2
        try:
            T1_temp = ds.read_temp(T1_address)
        except Exception as e:
            T1_temp = None

        try:
            T2_temp = ds.read_temp(T2_address)
        except Exception as e:
            T2_temp = None

        # Vyčistenie displeja
        lcd.fill(0)

        # Zobrazenie teploty z oboch senzorov
        if T1_temp is not None:
            lcd.text(f"Temp 1: {T1_temp:.2f} C", 10, 4)
        else:
            lcd.text("Temp 1: ERROR", 10, 4)

        if T2_temp is not None:
            lcd.text(f"Temp 2: {T2_temp:.2f} C", 10, 20)
        else:
            lcd.text("Temp 2: ERROR", 10, 20)

        # Výpočet rozdielu teplôt (delta temp) a jeho zobrazenie
        delta_temp = None
        if T1_temp is not None and T2_temp is not None:
            delta_temp = T1_temp - T2_temp
            lcd.text(f"Delta: {delta_temp:.2f} C", 10, 36)
        else:
            lcd.text("Delta: ERROR", 10, 36)

        # Logika pre LED a text na displeji
        led_state = "OFF"
        if delta_temp is not None:
            if abs(delta_temp) > 3:  # Ak delta je väčšia ako 3°C
                if not led_on:  # Ak LED ešte nie je zapnutá
                    led.value(1)  # Zapnúť LED
                    led_on = True  # Uložiť stav LED ako zapnutý
                led_state = "ON"
            elif abs(delta_temp) < 1:  # Ak delta klesne pod 1°C
                if led_on:  # LED sa už zapla predtým
                    led.value(0)  # Zhasnúť LED
                    led_on = False  # Uložiť stav LED ako vypnutý
                led_state = "OFF"
            else:
                led_state = "ON" if led_on else "OFF"  # Zobrazenie aktuálneho stavu LED
        # Zobrazenie stavu LED na displeji
        lcd.text(f"LED: {led_state}", 10, 56)

        # Aktualizácia displeja
        lcd.show()
        time.sleep(2)  # Krátka pauza pred ďalším cyklom

except KeyboardInterrupt:
    led.value(0)  # Zhasnutie LED pri prerušení
