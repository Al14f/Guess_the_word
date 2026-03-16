import pygame
import time
import random
import sys

# --- Inizializzazione Pygame ---
pygame.init()

# --- Costanti e Colori ---
WIDTH, HEIGHT = 600, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guess the word")

BG_COLOR = (18, 18, 19)
TEXT_COLOR = (255, 255, 255)
BOX_BG = (18, 18, 19)
BOX_BORDER = (58, 58, 60)

# Colori per i tentativi
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
GRAY = (58, 58, 60)

# Font
FONT_TITLE = pygame.font.SysFont("arial", 40, bold=True)
FONT_TEXT = pygame.font.SysFont("arial", 24)
FONT_BOX = pygame.font.SysFont("arial", 45, bold=True)

# Vocabolario limitato
VOCABOLARIO = ["GATTO", "TRENO", "PORTA", "SEDIA", "FIORE", "LUOGO", "NOTTE", "CARTA"]

# --- Funzioni di Logica ---
def scegli_parola(vocabolario):
    return random.choice(vocabolario)

def valuta_tentativo_gui(tentativo, parola_segreta):
    colori = [GRAY] * len(parola_segreta)
    lettere_disponibili = list(parola_segreta)
    
    for i in range(len(tentativo)):
        if tentativo[i] == parola_segreta[i]:
            colori[i] = GREEN
            lettere_disponibili.remove(tentativo[i])
            
    for i in range(len(tentativo)):
        if colori[i] != GREEN and tentativo[i] in lettere_disponibili:
            colori[i] = YELLOW
            lettere_disponibili.remove(tentativo[i])
            
    return colori

def imposta_difficolta(modalita, difficolta):
    limiti = {
        "tempo": {"F": 180, "M": 120, "D": 60},
        "tentativi": {"F": 5, "M": 4, "D": 3}
    }
    return limiti.get(modalita, {}).get(difficolta, 0)

def disegna_testo(testo, font, colore, y, x="center"):
    surf = font.render(testo, True, colore)
    rect = surf.get_rect()
    if x == "center":
        rect.centerx = WIDTH // 2
    else:
        rect.x = x
    rect.y = y
    SCREEN.blit(surf, rect)

# --- Nuove Funzioni per il Ritorno al Menu ---
def ritorna_al_menu():
    """Funzione per ritornare al menu principale e resettare le variabili di gioco"""
    return "MENU_MODO", "", "", 0, "", [], "", 0, 0

def disegna_hint_ritorno_menu(y, stato):
    """Funzione per disegnare il messaggio di aiuto per tornare al menu"""
    if stato == "MENU_DIFF":
        disegna_testo("Premi ESC per tornare al menu principale", FONT_TEXT, GRAY, y)
    elif stato == "GIOCO":
        disegna_testo("Premi ESC per tornare al menu principale", FONT_TEXT, GRAY, y)

def disegna_conferma_abbandono():
    """Funzione per disegnare la schermata di conferma abbandono"""
    disegna_testo("Sei sicuro di voler", FONT_TITLE, YELLOW, 220)
    disegna_testo("abbandonare?", FONT_TITLE, YELLOW, 280)
    disegna_testo("Premi 'S' per Si", FONT_TEXT, TEXT_COLOR, 380)
    disegna_testo("Premi 'N' per No", FONT_TEXT, TEXT_COLOR, 430)

# --- Ciclo Principale del Gioco ---
def main():
    clock = pygame.time.Clock()
    
    # Stati aggiunti: "MENU_CREDITI", "CONFERMA_ABBANDONO"
    stato = "MENU_MODO"
    modalita = ""
    difficolta = ""
    limite = 0
    
    parola_segreta = ""
    tentativi_fatti = [] 
    current_guess = ""
    start_time = 0
    messaggio_fine = ""
    tempo_pausa = 0  # Per bloccare il timer durante la conferma
    
    view_start_row = 0 
    
    # Definizione del bottone crediti
    credits_button_rect = pygame.Rect(WIDTH // 2 - 100, 450, 200, 50)

    while True:
        SCREEN.fill(BG_COLOR)
        
        righe_totali = limite if modalita == "tentativi" else 6
        if stato == "GIOCO":
            max_view = max(0, len(tentativi_fatti) - righe_totali + 1)
        else:
            max_view = max(0, len(tentativi_fatti) - righe_totali)

        # --- Gestione Eventi ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # --- Click del Mouse ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if stato == "MENU_MODO" and event.button == 1: # 1 è il tasto sinistro del mouse
                    if credits_button_rect.collidepoint(event.pos):
                        stato = "MENU_CREDITI"

            # --- Scorrimento Mouse ---
            if (stato == "GIOCO" or stato == "FINE") and modalita == "tempo":
                if event.type == pygame.MOUSEWHEEL:
                    if event.y > 0: 
                        view_start_row = max(0, view_start_row - 1)
                    elif event.y < 0: 
                        view_start_row = min(max_view, view_start_row + 1)
                
            # --- Gestione Tastiera ---
            if event.type == pygame.KEYDOWN:
                if stato == "MENU_MODO":
                    if event.key == pygame.K_t:
                        modalita = "tempo"
                        stato = "MENU_DIFF"
                    elif event.key == pygame.K_c:
                        modalita = "tentativi"
                        stato = "MENU_DIFF"
                        
                elif stato == "MENU_CREDITI":
                    if event.key == pygame.K_SPACE:
                        stato = "MENU_MODO" # Torna indietro
                        
                elif stato == "MENU_DIFF":
                    # Nuova funzionalità: Tasto ESC per tornare al menu principale
                    if event.key == pygame.K_ESCAPE:
                        stato, modalita, difficolta, limite, parola_segreta, tentativi_fatti, current_guess, start_time, view_start_row = ritorna_al_menu()
                    elif event.key in [pygame.K_f, pygame.K_m, pygame.K_d]:
                        if event.key == pygame.K_f: difficolta = "F"
                        if event.key == pygame.K_m: difficolta = "M"
                        if event.key == pygame.K_d: difficolta = "D"
                        
                        limite = imposta_difficolta(modalita, difficolta)
                        parola_segreta = scegli_parola(VOCABOLARIO)
                        tentativi_fatti = []
                        current_guess = ""
                        start_time = time.time()
                        view_start_row = 0
                        stato = "GIOCO"
                        
                elif stato == "GIOCO":
                    # Nuova funzionalità: Tasto ESC per aprire la conferma abbandono
                    if event.key == pygame.K_ESCAPE:
                        tempo_pausa = time.time()  # Salva il tempo quando si apre la conferma
                        stato = "CONFERMA_ABBANDONO"
                    elif event.key == pygame.K_UP:
                        view_start_row = max(0, view_start_row - 1)
                    elif event.key == pygame.K_DOWN:
                        view_start_row = min(max_view, view_start_row + 1)
                        
                    elif event.key == pygame.K_BACKSPACE:
                        current_guess = current_guess[:-1]
                        view_start_row = max_view 
                        
                    elif event.key == pygame.K_RETURN:
                        if len(current_guess) == len(parola_segreta):
                            colori = valuta_tentativo_gui(current_guess, parola_segreta)
                            tentativi_fatti.append((current_guess, colori))
                            
                            if current_guess == parola_segreta:
                                messaggio_fine = "COMPLIMENTI! Hai indovinato!"
                                stato = "FINE"
                            elif modalita == "tentativi" and len(tentativi_fatti) >= limite:
                                messaggio_fine = f"Tentativi esauriti! La parola era {parola_segreta}"
                                stato = "FINE"
                            current_guess = ""
                            
                            max_view = max(0, len(tentativi_fatti) - righe_totali + (1 if stato == "GIOCO" else 0))
                            view_start_row = max_view
                            
                    elif event.unicode.isalpha() and len(current_guess) < len(parola_segreta):
                        current_guess += event.unicode.upper()
                        view_start_row = max_view 
                        
                elif stato == "FINE":
                    if event.key == pygame.K_SPACE:
                        stato = "MENU_MODO" 
                    elif event.key == pygame.K_UP:
                        view_start_row = max(0, view_start_row - 1)
                    elif event.key == pygame.K_DOWN:
                        view_start_row = min(max_view, view_start_row + 1)

                elif stato == "CONFERMA_ABBANDONO":
                    if event.key == pygame.K_s:  # Conferma abbandono
                        stato, modalita, difficolta, limite, parola_segreta, tentativi_fatti, current_guess, start_time, view_start_row = ritorna_al_menu()
                    elif event.key == pygame.K_n:  # Continua a giocare
                        start_time += time.time() - tempo_pausa  # Recupera il tempo perso durante la pausa
                        stato = "GIOCO"

        # --- Aggiornamento e Disegno ---
        if stato == "MENU_MODO":
            disegna_testo("GUESS THE WORD", FONT_TITLE, GREEN, 150)
            disegna_testo("Premi 'T' per la Modalità a TEMPO", FONT_TEXT, TEXT_COLOR, 280)
            disegna_testo("Premi 'C' per la Modalità a TENTATIVI", FONT_TEXT, TEXT_COLOR, 330)
            
            # Disegno del bottone crediti
            pygame.draw.rect(SCREEN, BOX_BORDER, credits_button_rect, border_radius=12)
            # Centriamo il testo verticalmente calcolando y (rect.y + un piccolo margine)
            disegna_testo("CREDITI", FONT_TEXT, TEXT_COLOR, credits_button_rect.y + 10)

        elif stato == "MENU_CREDITI":
            # Nuova schermata Crediti
            disegna_testo("Developed by:", FONT_TITLE, YELLOW, 200)
            disegna_testo("Al14f", FONT_TEXT, TEXT_COLOR, 300)
            disegna_testo("CarmeloGit", FONT_TEXT, TEXT_COLOR, 350)
            disegna_testo("santolobianco-x", FONT_TEXT, TEXT_COLOR, 400)
            disegna_testo("Salv0Cosman0", FONT_TEXT, TEXT_COLOR, 450)
            
            # Tasto per tornare indietro
            disegna_testo("Premi SPAZIO per tornare al menu", FONT_TEXT, GRAY, HEIGHT - 100)
            
        elif stato == "MENU_DIFF":
            disegna_testo("SCEGLI LA DIFFICOLTA'", FONT_TITLE, YELLOW, 200)
            disegna_testo("Premi 'F' per Facile", FONT_TEXT, TEXT_COLOR, 350)
            disegna_testo("Premi 'M' per Media", FONT_TEXT, TEXT_COLOR, 400)
            disegna_testo("Premi 'D' per Difficile", FONT_TEXT, TEXT_COLOR, 450)
            
            # Nuovo: Messaggio per tornare al menu principale
            disegna_hint_ritorno_menu(HEIGHT - 80, stato)
            
        elif stato == "GIOCO" or stato == "FINE":
            if stato == "GIOCO" and modalita == "tempo":
                tempo_trascorso = time.time() - start_time
                tempo_rimasto = limite - tempo_trascorso
                if tempo_rimasto <= 0:
                    messaggio_fine = f"Tempo scaduto! La parola era {parola_segreta}"
                    stato = "FINE"
                    max_view = max(0, len(tentativi_fatti) - righe_totali)
                    view_start_row = max_view
                else:
                    disegna_testo(f"Tempo: {int(tempo_rimasto)}s", FONT_TEXT, TEXT_COLOR, 30, 20)
            
            if modalita == "tentativi":
                rimanenti = limite - len(tentativi_fatti)
                disegna_testo(f"Tentativi: {rimanenti}", FONT_TEXT, TEXT_COLOR, 30, 20)

            box_size = 60
            margin = 10
            start_x = (WIDTH - (5 * box_size + 4 * margin)) // 2
            start_y = 150
            
            if modalita == "tempo" and max_view > 0:
                if view_start_row > 0:
                    disegna_testo("▲", FONT_TEXT, GRAY, start_y - 30)
                if view_start_row < max_view:
                    disegna_testo("▼", FONT_TEXT, GRAY, start_y + (righe_totali * (box_size + margin)))

            for row in range(righe_totali):
                indice_tentativo = row + view_start_row
                
                for col in range(5):
                    x = start_x + col * (box_size + margin)
                    y = start_y + row * (box_size + margin)
                    rect = pygame.Rect(x, y, box_size, box_size)
                    
                    if indice_tentativo < len(tentativi_fatti):
                        colore_box = tentativi_fatti[indice_tentativo][1][col]
                        lettera_txt = tentativi_fatti[indice_tentativo][0][col]
                        pygame.draw.rect(SCREEN, colore_box, rect)
                        lettera = FONT_BOX.render(lettera_txt, True, TEXT_COLOR)
                        SCREEN.blit(lettera, lettera.get_rect(center=rect.center))
                        
                    elif indice_tentativo == len(tentativi_fatti) and col < len(current_guess) and stato == "GIOCO":
                        pygame.draw.rect(SCREEN, BOX_BORDER, rect, 2)
                        lettera = FONT_BOX.render(current_guess[col], True, TEXT_COLOR)
                        SCREEN.blit(lettera, lettera.get_rect(center=rect.center))
                        
                    else:
                        pygame.draw.rect(SCREEN, BOX_BORDER, rect, 2)

            if stato == "FINE":
                disegna_testo(messaggio_fine, FONT_TEXT, YELLOW, 80)
                disegna_testo("Premi SPAZIO per giocare di nuovo", FONT_TEXT, TEXT_COLOR, HEIGHT - 80)
            else:
                # Nuovo: Messaggio per tornare al menu principale durante il gioco
                disegna_hint_ritorno_menu(HEIGHT - 80, stato)

        elif stato == "CONFERMA_ABBANDONO":
            # Nuova schermata di conferma abbandono
            disegna_conferma_abbandono()

        pygame.display.flip()
        clock.tick(30) 

if __name__ == "__main__":
    main()