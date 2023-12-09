import csv
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from forex_python.converter import CurrencyRates, CurrencyCodes

historique_fichier = 'historique_conversions.csv'

currency_rates = CurrencyRates()
currency_codes = CurrencyCodes()

def convert_currency(amount, from_currency, to_currency):
    try:
        rate = currency_rates.get_rate(from_currency, to_currency)
        converted_amount = rate * amount
        symbol = currency_codes.get_symbol(to_currency)
        return converted_amount, f"{amount} {from_currency} = {symbol}{converted_amount:.2f} {to_currency}"
    except Exception as e:
        return None, f"Erreur de conversion: {e}"

def enregistrer_historique(montant, from_currency, to_currency, converted_amount):
    if not os.path.isfile(historique_fichier):
        with open(historique_fichier, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Montant", "Devise d'Origine", "Devise de Destination", "Montant Converti"])
    
    with open(historique_fichier, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([montant, from_currency, to_currency, converted_amount])

def convertir_et_afficher():
    try:
        montant = float(montant_entry.get())
        from_currency = from_currency_entry.get().upper()
        to_currency = to_currency_entry.get().upper()
        converted_amount, message = convert_currency(montant, from_currency, to_currency)
        messagebox.showinfo("Résultat", message)
        if converted_amount is not None:
            enregistrer_historique(montant, from_currency, to_currency, converted_amount)
    except ValueError:
        messagebox.showerror("Erreur", "Entrée invalide. Veuillez entrer un nombre.")

root = tk.Tk()
root.title("Convertisseur de devises")

tk.Label(root, text="Montant:").grid(row=0, column=0)
montant_entry = tk.Entry(root)
montant_entry.grid(row=0, column=1)

tk.Label(root, text="De la devise:").grid(row=1, column=0)
from_currency_entry = tk.Entry(root)
from_currency_entry.grid(row=1, column=1)

tk.Label(root, text="À la devise:").grid(row=2, column=0)
to_currency_entry = tk.Entry(root)
to_currency_entry.grid(row=2, column=1)

convert_button = tk.Button(root, text="Convertir", command=convertir_et_afficher)
convert_button.grid(row=3, column=0, columnspan=2)

root.mainloop()
