import hashlib
import datetime
import csv
import os

# --- KONFIGURACJA ---
INPUT_FILE = "pacjenci_raw.csv"  # Plik wejściowy (TAJNY)
OUTPUT_FILE = "dane_dla_sponsora.csv" # Plik wyjściowy (BEZPIECZNY)

def generuj_hash(tekst):
    """Tworzy unikalny skrót (Hash) z tekstu."""
    return hashlib.sha256(tekst.encode()).hexdigest()[:8].upper()

def wiek_z_peselu(pesel):
    """Wyciąga rok urodzenia z PESELu i liczy przybliżony wiek."""
    try:
        rok = int(pesel[0:2])
        miesiac = int(pesel[2:4])
        
        if miesiac > 20: 
            rok += 2000
        else:
            rok += 1900
            
        obecny_rok = datetime.date.today().year
        return obecny_rok - rok
    except:
        return "BŁĄD"

def anonimizuj_dane():
    print(f"🔒 ROZPOCZYNAM ANONIMIZACJĘ DANYCH KLINICZNYCH...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Błąd: Brak pliku '{INPUT_FILE}'!")
        return

    # ODCZYT: utf-8-sig (Kluczowe dla polskich znaków w Excelu wejściowym)
    with open(INPUT_FILE, 'r', encoding='utf-8-sig') as f_in:
        reader = csv.reader(f_in)
        headers = next(reader, None) # Pomiń nagłówki
        
        dane_bezpieczne = []
        dane_bezpieczne.append(["PATIENT_ID", "WIEK", "WYNIK"]) 
        
        licznik = 0
        for row in reader:
            if len(row) < 4: continue
            
            imie = row[0].strip()
            nazwisko = row[1].strip()
            
            # --- NAPRAWA PESELU ---
            raw_pesel = row[2].strip()
            pesel = raw_pesel.zfill(11) # Dodaje zera z przodu jeśli brakuje
            # ----------------------

            wynik = row[3].strip()
            
            # 1. Tworzymy unikalne ID
            raw_string = f"{imie}{nazwisko}{pesel}"
            patient_id = "SUBJ-" + generuj_hash(raw_string)
            
            # 2. Wyliczamy wiek
            wiek = wiek_z_peselu(pesel)
            
            dane_bezpieczne.append([patient_id, wiek, wynik])
            licznik += 1
            
            print(f"   ✅ {imie} {nazwisko} -> {patient_id}")

    # ZAPIS: Zwykłe utf-8 (Żeby usunąć krzaczki 'ï»¿' z nagłówka pliku wynikowego)
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.writer(f_out)
        writer.writerows(dane_bezpieczne)
        
    print(f"\n✨ SUKCES! Utworzono plik '{OUTPUT_FILE}' z {licznik} pacjentami.")

# --- START ---
if __name__ == "__main__":
    # 1. Usuwamy stary plik, żeby wygenerować świeży (bez błędów)
    if os.path.exists(INPUT_FILE):
        try:
            os.remove(INPUT_FILE)
            print("🗑️ Usunięto stary plik 'pacjenci_raw.csv'.")
        except:
            pass

    # 2. Tworzymy nowy plik wejściowy (z utf-8-sig dla polskich znaków)
    if not os.path.exists(INPUT_FILE):
        with open(INPUT_FILE, "w", encoding='utf-8-sig') as f:
            f.write("Imie,Nazwisko,PESEL,Wynik_HGB\n")
            f.write("Jan,Kowalski,85021012345,14.5\n")
            f.write("Anna,Nowak,92111509876,12.1\n")
            f.write("Piotr,Wiśniewski,01231205555,15.2\n") 
        print(f"📝 Utworzono świeży plik '{INPUT_FILE}'.")
    
    # 3. Uruchamiamy proces
    anonimizuj_dane()
