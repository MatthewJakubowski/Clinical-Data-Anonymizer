# 🛡️ Clinical Data Anonymizer

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Security](https://img.shields.io/badge/Security-SHA--256-green?style=for-the-badge)
![Compliance](https://img.shields.io/badge/Compliance-GDPR%2FRODO-blue?style=for-the-badge)

> **A Python tool for pseudonymizing patient data for Clinical Trials.**
> Ensures privacy compliance by hashing PII (Personally Identifiable Information) while preserving data utility.

---

## 🏥 Context
In Clinical Trials, sharing raw patient data (Names, National IDs/PESEL) with Sponsors or CRA is strictly prohibited by **GDPR (RODO)**.
However, data consistency is key – if "Patient A" returns for a follow-up visit, they must be identified as the same entity without revealing their real identity.

**This tool solves that problem.**

---

## ⚙️ How It Works
The script processes raw CSV files containing sensitive medical data and transforms them into a "Safe Copy" for export.

### Key Algorithms:
1.  **Deterministic Hashing (SHA-256):**
    * Converts `Name + Surname + ID` into a unique alphanumeric string (e.g., `SUBJ-8A2F...`).
    * **Benefit:** The same patient always gets the same code (allowing follow-up tracking) but cannot be reverse-engineered to reveal their identity.
2.  **Smart Age Extraction:**
    * **Removes** the PESEL/National ID number entirely.
    * **Extracts** the birth year from the ID and calculates the current Age.
    * **Fixes Data Quality:** Automatically repairs malformed IDs (e.g., missing leading zeros in Excel exports).

---

## 🚀 Usage

### 1. Input Data (`pacjenci_raw.csv`)
Prepare a CSV file with sensitive data:
```csv
Imie,Nazwisko,PESEL,Wynik_HGB
Jan,Kowalski,85021012345,14.5
Piotr,Wiśniewski,01231205555,15.2
```

### 2. Run the Anonymizer
python main.py

### 3. Output Data (dane_dla_sponsora.csv)
​The script generates a safe file ready for transmission (Clean UTF-8, no BOM):
PATIENT_ID,WIEK,WYNIK
SUBJ-8C50D64...,40,14.5
SUBJ-8D8093F...,24,15.2

---
## 👨‍🔬 About the Author

**Mateusz Jakubowski**
*Medical Analyst (15y exp) ➡️ Aspiring AI Engineer & Python Developer.*

I am building tools that bridge the gap between Medical Diagnostics and IT. This project was developed entirely on a mobile environment (**Samsung DeX** + **Pydroid 3**).

* **Connect with me:** [LinkedIn](https://www.linkedin.com/in/mateuszjakubowski)
* **Portfolio:** #FromPipetteToPython

---
---

### ⚠️ Disclaimer & Legal Notice

* **Educational Purpose Only:** This software is developed as part of a programming portfolio (#FromPipetteToPython) and is intended for educational and demonstration purposes only.
* **Not a Medical Device:** This tool is **not** a validated Laboratory Information System (LIS) or a medical device under MDR/FDA regulations. It has not undergone formal GAMP5 validation for use in GxP environments.
* **GDPR/RODO Responsibility:** While this tool implements standard hashing algorithms (SHA-256), the final responsibility for data privacy and compliance lies with the user. The author is not liable for any data breaches or misuse of this software.
* **Synthetic Data:** All data presented in examples (e.g., in `pacjenci_raw.csv`) is synthetic (fake) and generated for testing purposes. **Never upload real patient data to a public GitHub repository.**

