# Guess the Word 🎮

Un divertente gioco di parole sviluppato in **Python** con la libreria **Pygame**. L'obiettivo è mettere alla prova le tue abilità e indovinare la parola segreta prima di esaurire il tempo o i tentativi a disposizione!

---

## 🛠 Prerequisiti

Assicurati di avere installato i seguenti strumenti sul tuo sistema:

* **Python 3.10+**
* **Git** (per clonare il repository)

---

## 🚀 Installazione

Segui questi passaggi per configurare il gioco in locale:

1.  **Clona il repository:**
    ```bash
    git clone https://github.com/Al14f/Guess_the_word
    ```

2.  **Entra nella cartella del progetto:**
    ```bash
    cd ~/percorso_cartella_Guess_the_word
    ```

3.  **Installa le dipendenze:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🎮 Come avviare il gioco

Una volta completata l'installazione, puoi lanciare il gioco con il seguente comando:

```bash
python game.py

```


---

## 🧪 Unit Testing

Il progetto include una suite completa di **72 unit test** con **pytest**.

### Esegui i test:
```bash
# Test base
pytest test_game.py -v

# Con coverage report
pytest test_game.py -v --cov

# Coverage dettagliato
pytest test_game.py -v --cov --cov-report=term-missing
```

### Coverage Raggiunto:
- ✅ **89%** (Coverage complessivo)
- ✅ **81%** (game.py)
- ✅ **72 test case**
- ✅ **100% passing**

### Test Structure:
- Unit tests per funzioni singole
- Integration tests per flussi completi
- Edge cases coperti
- Pattern AAA (Arrange, Act, Assert) implementato
