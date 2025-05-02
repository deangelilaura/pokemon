from flask import Flask, render_template, request
import random
import csv 

app = Flask(__name__) 

def scegli_carta(): 
    rarita = random.choices(
         ['Comune', 'Non Comune', 'Rara', 'Ultra Rara'],
           weights=[0.70, 0.20, 0.09, 0.01],
             k=1
               )[0]
    return rarita 

def apri_pacchetto():
     carte = [scegli_carta() for _ in range(5)]
     return carte 

def calcola_punti(carte):
     punti = 0
     valori = {'Comune': 1, 'Non Comune': 3, 'Rara': 10, 'Ultra Rara': 30}
     for carta in carte:
          punti += valori[carta]
          return punti 

def carica_collezione(nome_file="collezione.csv"):
     collezione_caricata = []
     try:
          with open(nome_file, 'r', newline='') as file_csv:
               reader = csv.reader(file_csv)
               next(reader, None) # Salta l'intestazione
               for riga in reader:
                    if riga:
                         collezione_caricata.append(riga[0])
                         except FileNotFoundError:
                         print("Nessun file di collezione trovato. Inizierai con una collezione vuota.")
                         except Exception as e:
                         print(f"Errore durante il caricamento della collezione: {e}")
                         return collezione_caricata 

def salva_collezione(collezione, nome_file="collezione.csv"): 
     try:
          with open(nome_file, 'w', newline='') as file_csv:
               writer = csv.writer(file_csv)
               writer.writerow(['Carta'])  # Intestazione della colonna
               for carta in collezione:
                    writer.writerow([carta])
                    print(f"Collezione salvata con successo nel file '{nome_file}'.")
    except Exception as e:
        print(f"Errore durante il salvataggio della collezione: {e}") 

punteggio = 100
collezione = carica_collezione() 

@app.route('/')
def index():
     return render_template('index.html', punteggio=punteggio, collezione=collezione) 

@app.route('/apri_pacchetto', methods=['POST'])
def apri_pacchetto_route():
     global punteggio, collezione
     if punteggio >= 10:
          punteggio -= 10
          nuove_carte = apri_pacchetto()
          for carta in nuove_carte:
               collezione.append(carta)
        punti_guadagnati = calcola_punti(nuove_carte)
        punteggio += punti_guadagnati
        return render_template('index.html', punteggio=punteggio, collezione=collezione, nuove_carte=nuove_carte, messaggio=f"Hai trovato {', '.join(nuove_carte)} e guadagnato {punti_guadagnati} punti!")
    else:
        return render_template('index.html', punteggio=punteggio, collezione=collezione, errore="Non hai abbastanza punti per aprire un pacchetto.") 

@app.route('/salva_collezione', methods=['POST'])
def salva_collezione_route():
    global collezione
    salva_collezione(collezione)
    return render_template('index.html', punteggio=punteggio, collezione=collezione, messaggio="Collezione salvata!") 

if __name__ == '__main__':
    app.run(debug=True)