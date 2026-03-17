import pygame
import time
import random
import sys

# --- Inizializzazione Pygame ---
pygame.init()

# --- Costanti e Colori ---
WIDTH, HEIGHT = 600, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guess the word - Dynamic Edition")

BG_COLOR = (18, 18, 19)
TEXT_COLOR = (255, 255, 255)
BOX_BG = (18, 18, 19)
BOX_BORDER = (58, 58, 60)

# Colori per i tentativi
GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
GRAY = (58, 58, 60)

# Font base
FONT_TITLE = pygame.font.SysFont("arial", 40, bold=True)
FONT_TEXT = pygame.font.SysFont("arial", 24)

# --- Funzioni di Logica ---
def scegli_parola():
    """Pesca una parola di qualsiasi lunghezza dal file."""
    try:
        with open("parole.txt", "r", encoding="utf-8") as file:
            parole = [linea.strip().upper() for linea in file if linea.strip()]
        
        if not parole:
            return "PYTHON"
            
        return random.choice(parole)
    except FileNotFoundError:
        return "GIOCO"

def valuta_tentativo_gui(tentativo, parola_segreta):
    colori = [GRAY] * len(parola_segreta)
    lettere_disponibili = list(parola_segreta)
    
    # Primo passaggio: corretti al posto giusto (Verde)
    for i in range(len(tentativo)):
        if tentativo[i] == parola_segreta[i]:
            colori[i] = GREEN
            lettere_disponibili.remove(tentativo[i])
            
    # Secondo passaggio: presenti ma posto sbagliato (Giallo)
    for i in range(len(tentativo)):
        if colori[i] != GREEN and tentativo[i] in lettere_disponibili:
            colori[i] = YELLOW
            lettere_disponibili.remove(tentativo[i])
            
    return colori

def imposta_difficolta(modalita, difficolta):
    limiti = {
        "tempo": {"F": 180, "M": 120, "D": 60},
        "tentativi": {"F": 6, "M": 5, "D": 4}
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

def ritorna_al_menu():
    return "MENU_MODO", "", "", 0, "", [], "", 0, 0

def disegna_hint_ritorno_menu(y, stato):
    if stato in ["MENU_DIFF", "GIOCO"]:
        disegna_testo("Premi ESC per tornare al menu principale", FONT_TEXT, GRAY, y)

def disegna_conferma_abbandono():
    disegna_testo("Sei sicuro di voler", FONT_TITLE, YELLOW, 220)
    disegna_testo("abbandonare?", FONT_TITLE, YELLOW, 280)
    disegna_testo("Premi 'S' per Si", FONT_TEXT, TEXT_COLOR, 380)
    disegna_testo("Premi 'N' per No", FONT_TEXT, TEXT_COLOR, 430)

# --- Ciclo Principale ---
def main():
    clock = pygame.time.Clock()
    
    stato = "MENU_MODO"
    modalita = ""
    difficolta = ""
    limite = 0
    parola_segreta = ""
    tentativi_fatti = [] 
    current_guess = ""
    start_time = 0
    messaggio_fine = ""
    tempo_pausa = 0
    view_start_row = 0 
    
    credits_button_rect = pygame.Rect(WIDTH // 2 - 100, 450, 200, 50)

    while True:
        SCREEN.fill(BG_COLOR)
        
        # Gestione righe visualizzabili
        righe_totali = limite if modalita == "tentativi" else 6
        if stato == "GIOCO":
            max_view = max(0, len(tentativi_fatti) - righe_totali + 1)
        else:
            max_view = max(0, len(tentativi_fatti) - righe_totali)

        # --- Eventi ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if stato == "MENU_MODO" and event.button == 1:
                    if credits_button_rect.collidepoint(event.pos):
                        stato = "MENU_CREDITI"

            if (stato == "GIOCO" or stato == "FINE") and event.type == pygame.MOUSEWHEEL:
                if event.y > 0: view_start_row = max(0, view_start_row - 1)
                elif event.y < 0: view_start_row = min(max_view, view_start_row + 1)
                
            if event.type == pygame.KEYDOWN:
                if stato == "MENU_MODO":
                    if event.key == pygame.K_t:
                        modalita, stato = "tempo", "MENU_DIFF"
                    elif event.key == pygame.K_c:
                        modalita, stato = "tentativi", "MENU_DIFF"
                
                elif stato == "MENU_CREDITI" and event.key == pygame.K_SPACE:
                    stato = "MENU_MODO"

                elif stato == "MENU_DIFF":
                    if event.key == pygame.K_ESCAPE:
                        stato, modalita, difficolta, limite, parola_segreta, tentativi_fatti, current_guess, start_time, view_start_row = ritorna_al_menu()
                    elif event.key in [pygame.K_f, pygame.K_m, pygame.K_d]:
                        difficolta = event.unicode.upper()
                        limite = imposta_difficolta(modalita, difficolta)
                        parola_segreta = scegli_parola()
                        tentativi_fatti, current_guess, view_start_row = [], "", 0
                        start_time, stato = time.time(), "GIOCO"

                elif stato == "GIOCO":
                    if event.key == pygame.K_ESCAPE:
                        tempo_pausa, stato = time.time(), "CONFERMA_ABBANDONO"
                    elif event.key == pygame.K_BACKSPACE:
                        current_guess = current_guess[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(current_guess) == len(parola_segreta):
                            colori = valuta_tentativo_gui(current_guess, parola_segreta)
                            tentativi_fatti.append((current_guess, colori))
                            if current_guess == parola_segreta:
                                messaggio_fine, stato = "COMPLIMENTI!", "FINE"
                            elif modalita == "tentativi" and len(tentativi_fatti) >= limite:
                                messaggio_fine, stato = f"PAROLA: {parola_segreta}", "FINE"
                            current_guess = ""
                            view_start_row = max(0, len(tentativi_fatti) - righe_totali + (1 if stato == "GIOCO" else 0))
                    elif event.unicode.isalpha() and len(current_guess) < len(parola_segreta):
                        current_guess += event.unicode.upper()

                elif stato == "FINE" and event.key == pygame.K_SPACE:
                    stato, modalita, difficolta, limite, parola_segreta, tentativi_fatti, current_guess, start_time, view_start_row = ritorna_al_menu()

                elif stato == "CONFERMA_ABBANDONO":
                    if event.key == pygame.K_s:
                        stato, modalita, difficolta, limite, parola_segreta, tentativi_fatti, current_guess, start_time, view_start_row = ritorna_al_menu()
                    elif event.key == pygame.K_n:
                        start_time += time.time() - tempo_pausa
                        stato = "GIOCO"

        # --- Disegno ---
        if stato == "MENU_MODO":
            disegna_testo("GUESS THE WORD", FONT_TITLE, GREEN, 150)
            disegna_testo("Premi 'T' per Modalità TEMPO", FONT_TEXT, TEXT_COLOR, 280)
            disegna_testo("Premi 'C' per Modalità TENTATIVI", FONT_TEXT, TEXT_COLOR, 330)
            pygame.draw.rect(SCREEN, BOX_BORDER, credits_button_rect, border_radius=12)
            disegna_testo("CREDITI", FONT_TEXT, TEXT_COLOR, credits_button_rect.y + 10)

        elif stato == "MENU_CREDITI":
            disegna_testo("Developed by:", FONT_TITLE, YELLOW, 200)
            for i, name in enumerate(["Al14f", "CarmeloGit", "santolobianco-x", "Salv0Cosman0"]):
                disegna_testo(name, FONT_TEXT, TEXT_COLOR, 300 + (i*50))
            disegna_testo("Premi SPAZIO per tornare", FONT_TEXT, GRAY, HEIGHT - 100)

        elif stato == "MENU_DIFF":
            disegna_testo("DIFFICOLTÀ", FONT_TITLE, YELLOW, 200)
            disegna_testo("F: Facile | M: Media | D: Difficile", FONT_TEXT, TEXT_COLOR, 350)
            disegna_hint_ritorno_menu(HEIGHT - 80, stato)

        elif stato in ["GIOCO", "FINE"]:
            # Logica Timer/Tentativi
            if stato == "GIOCO" and modalita == "tempo":
                tempo_rimasto = limite - (time.time() - start_time)
                if tempo_rimasto <= 0:
                    messaggio_fine, stato = f"TEMPO SCADUTO! Era: {parola_segreta}", "FINE"
                    view_start_row = max(0, len(tentativi_fatti) - righe_totali)
                else:
                    disegna_testo(f"Tempo: {int(tempo_rimasto)}s", FONT_TEXT, TEXT_COLOR, 30, 20)
            elif modalita == "tentativi":
                disegna_testo(f"Tentativi: {limite - len(tentativi_fatti)}", FONT_TEXT, TEXT_COLOR, 30, 20)

            # --- GRIGLIA DINAMICA ---
            num_L = len(parola_segreta)
            margin = 8
            # Calcolo dimensione box in base alla lunghezza parola
            max_grid_w = WIDTH - 80
            box_size = min(65, (max_grid_w - (margin * (num_L - 1))) // num_L)
            
            start_x = (WIDTH - (num_L * box_size + (num_L - 1) * margin)) // 2
            start_y = 150
            
            # Font dinamico per le lettere
            font_box_dinamico = pygame.font.SysFont("arial", int(box_size * 0.7), bold=True)

            for row in range(righe_totali):
                idx_t = row + view_start_row
                for col in range(num_L):
                    x = start_x + col * (box_size + margin)
                    y = start_y + row * (box_size + margin)
                    rect = pygame.Rect(x, y, box_size, box_size)
                    
                    if idx_t < len(tentativi_fatti):
                        pygame.draw.rect(SCREEN, tentativi_fatti[idx_t][1][col], rect)
                        let_surf = font_box_dinamico.render(tentativi_fatti[idx_t][0][col], True, TEXT_COLOR)
                        SCREEN.blit(let_surf, let_surf.get_rect(center=rect.center))
                    elif idx_t == len(tentativi_fatti) and col < len(current_guess) and stato == "GIOCO":
                        pygame.draw.rect(SCREEN, BOX_BORDER, rect, 2)
                        let_surf = font_box_dinamico.render(current_guess[col], True, TEXT_COLOR)
                        SCREEN.blit(let_surf, let_surf.get_rect(center=rect.center))
                    else:
                        pygame.draw.rect(SCREEN, BOX_BORDER, rect, 2)

            if stato == "FINE":
                disegna_testo(messaggio_fine, FONT_TEXT, YELLOW, 80)
                disegna_testo("Premi SPAZIO per ricominciare", FONT_TEXT, TEXT_COLOR, HEIGHT - 80)
            else:
                disegna_hint_ritorno_menu(HEIGHT - 80, stato)

        elif stato == "CONFERMA_ABBANDONO":
            disegna_conferma_abbandono()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()