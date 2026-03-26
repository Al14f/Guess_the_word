import pygame
import time
import random
import sys

# init pygame
pygame.init()

# screen settings
WIDTH, HEIGHT = 600, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guess the word - Dynamic Edition")

# colors
BG_COLOR = (18, 18, 19)
TEXT_COLOR = (255, 255, 255)
BOX_BG = (18, 18, 19)
BOX_BORDER = (58, 58, 60)

GREEN = (83, 141, 78)
YELLOW = (181, 159, 59)
GRAY = (58, 58, 60)

# fonts
FONT_TITLE = pygame.font.SysFont("arial", 40, bold=True)
FONT_TEXT = pygame.font.SysFont("arial", 24)


# game logic

def scegli_parola(difficolta):
    # get word from file by difficulty
    try:
        with open("parole.txt", "r", encoding="utf-8") as file:
            parole = [linea.strip().upper() for linea in file if linea.strip()]
        
        if not parole:
            return "PYTHON"
        
        # filter by difficulty
        if difficolta == "F":
            parole_filtrate = [p for p in parole if len(p) <= 5]
        elif difficolta == "M":
            parole_filtrate = [p for p in parole if 6 <= len(p) <= 8]
        elif difficolta == "D":
            parole_filtrate = [p for p in parole if len(p) >= 9]
        else:
            parole_filtrate = parole
            
        if not parole_filtrate:
            return "PYTHON"
            
        return random.choice(parole_filtrate)
    except FileNotFoundError:
        return "GIOCO"


def valuta_tentativo_gui(tentativo, parola_segreta):
    # check attempt colors
    colori = [GRAY] * len(parola_segreta)
    lettere_disponibili = list(parola_segreta)
    
    # correct position
    for i in range(len(tentativo)):
        if tentativo[i] == parola_segreta[i]:
            colori[i] = GREEN
            lettere_disponibili.remove(tentativo[i])
            
    # wrong position but in word
    for i in range(len(tentativo)):
        if colori[i] != GREEN and tentativo[i] in lettere_disponibili:
            colori[i] = YELLOW
            lettere_disponibili.remove(tentativo[i])
            
    return colori


def imposta_difficolta(modalita, difficolta):
    # get limit based on mode and difficulty
    limiti = {
        "tempo": {"F": 300, "M": 275, "D": 250},
        "tentativi": {"F": 20, "M": 15, "D": 10}
    }
    return limiti.get(modalita, {}).get(difficolta, 0)


def gestisci_tentativo(tentativo, parola_segreta, modalita, limite, tentativi_fatti):
    # process attempt
    if len(tentativo) == len(parola_segreta):
        colori = valuta_tentativo_gui(tentativo, parola_segreta)
        tentativi_fatti.append((tentativo, colori))
        
        if tentativo == parola_segreta:
            return "FINE", "COMPLIMENTI!"
        elif modalita == "tentativi" and len(tentativi_fatti) >= limite:
            return "FINE", f"PAROLA: {parola_segreta}"
        else:
            return "GIOCO", ""
    return "GIOCO", ""


def calcola_tempo_rimasto(modalita, limite, start_time):
    # check remaining time
    if modalita == "tempo":
        tempo_rimasto = limite - (time.time() - start_time)
        if tempo_rimasto <= 0:
            return "FINE", f"TEMPO SCADUTO! Era: PAROLA"
        else:
            return "GIOCO", int(tempo_rimasto)
    return "GIOCO", 0


def calcola_dimensioni_griglia(parola_segreta):
    # dynamic grid size
    num_L = len(parola_segreta)
    margin = 8
    max_grid_w = WIDTH - 80
    box_size = min(65, (max_grid_w - (margin * (num_L - 1))) // num_L)
    
    start_x = (WIDTH - (num_L * box_size + (num_L - 1) * margin)) // 2
    start_y = 150
    
    return num_L, margin, box_size, start_x, start_y


def calcola_righe_visualizzabili(stato, tentativi_fatti):
    # visible rows
    righe_totali = 6
    if stato == "GIOCO":
        max_view = max(0, len(tentativi_fatti) - righe_totali + 1)
    else:
        max_view = max(0, len(tentativi_fatti) - righe_totali)
    return righe_totali, max_view


def valida_input_carattere(event):
    # validate alpha char
    if event.unicode.isalpha():
        return True
    return False


# drawing

def disegna_testo(testo, font, colore, y, x="center"):
    # draw text
    surf = font.render(testo, True, colore)
    rect = surf.get_rect()
    if x == "center":
        rect.centerx = WIDTH // 2
    else:
        rect.x = x
    rect.y = y
    SCREEN.blit(surf, rect)


def disegna_hint_ritorno_menu(y, stato):
    # hint text
    if stato in ["MENU_DIFF", "GIOCO"]:
        disegna_testo("Premi ESC per tornare al menu principale", FONT_TEXT, GRAY, y)


def disegna_conferma_abbandono():
    # confirm abandon screen
    disegna_testo("Sei sicuro di voler", FONT_TITLE, YELLOW, 220)
    disegna_testo("abbandonare?", FONT_TITLE, YELLOW, 280)
    disegna_testo("Premi 'S' per Si", FONT_TEXT, TEXT_COLOR, 380)
    disegna_testo("Premi 'N' per No", FONT_TEXT, TEXT_COLOR, 430)


def disegna_griglia_gioco(game_state):
    # draw game grid
    parola_segreta = game_state["parola_segreta"]
    tentativi_fatti = game_state["tentativi_fatti"]
    current_guess = game_state["current_guess"]
    view_start_row = game_state["view_start_row"]
    
    num_L, margin, box_size, start_x, start_y = calcola_dimensioni_griglia(parola_segreta)
    righe_totali = 6
    font_box_dinamico = pygame.font.SysFont("arial", int(box_size * 0.7), bold=True)
    
    for row in range(righe_totali):
        idx_t = row + view_start_row
        for col in range(num_L):
            x = start_x + col * (box_size + margin)
            y = start_y + row * (box_size + margin)
            rect = pygame.Rect(x, y, box_size, box_size)
            
            # past attempts
            if idx_t < len(tentativi_fatti):
                pygame.draw.rect(SCREEN, tentativi_fatti[idx_t][1][col], rect)
                let_surf = font_box_dinamico.render(tentativi_fatti[idx_t][0][col], True, TEXT_COLOR)
                SCREEN.blit(let_surf, let_surf.get_rect(center=rect.center))
            # current input
            elif idx_t == len(tentativi_fatti) and col < len(current_guess):
                pygame.draw.rect(SCREEN, BOX_BORDER, rect, 2)
                let_surf = font_box_dinamico.render(current_guess[col], True, TEXT_COLOR)
                SCREEN.blit(let_surf, let_surf.get_rect(center=rect.center))
            # empty boxes
            else:
                pygame.draw.rect(SCREEN, BOX_BORDER, rect, 2)


def disegna_gioco_state(game_state):
    # draw game/end screen
    if game_state["modalita"] == "tempo":
        tempo_rimasto = game_state["limite"] - (time.time() - game_state["start_time"])
        if tempo_rimasto > 0:
            disegna_testo(f"Tempo: {int(tempo_rimasto)}s", FONT_TEXT, TEXT_COLOR, 30, 20)
    elif game_state["modalita"] == "tentativi":
        disegna_testo(f"Tentativi: {game_state['limite'] - len(game_state['tentativi_fatti'])}", FONT_TEXT, TEXT_COLOR, 30, 20)
    
    disegna_griglia_gioco(game_state)
    
    if game_state["stato"] == "FINE":
        disegna_testo(game_state["messaggio_fine"], FONT_TEXT, YELLOW, 80)
        disegna_testo("Premi SPAZIO per ricominciare", FONT_TEXT, TEXT_COLOR, HEIGHT - 80)
    else:
        disegna_hint_ritorno_menu(HEIGHT - 80, "GIOCO")


def disegna_schermo(game_state, credits_button_rect):
    # draw current screen
    SCREEN.fill(BG_COLOR)
    
    if game_state["stato"] == "MENU_MODO":
        # main menu
        disegna_testo("GUESS THE WORD", FONT_TITLE, GREEN, 150)
        disegna_testo("Premi 'T' per Modalità TEMPO", FONT_TEXT, TEXT_COLOR, 280)
        disegna_testo("Premi 'C' per Modalità TENTATIVI", FONT_TEXT, TEXT_COLOR, 330)
        pygame.draw.rect(SCREEN, BOX_BORDER, credits_button_rect, border_radius=12)
        disegna_testo("CREDITI", FONT_TEXT, TEXT_COLOR, credits_button_rect.y + 10)
    
    elif game_state["stato"] == "MENU_CREDITI":
        # credits menu
        disegna_testo("Developed by:", FONT_TITLE, YELLOW, 200)
        for i, name in enumerate(["Al14f", "CarmeloGit", "santolobianco-x", "Salv0Cosman0"]):
            disegna_testo(name, FONT_TEXT, TEXT_COLOR, 300 + (i*50))
        disegna_testo("Premi ESC per tornare", FONT_TEXT, GRAY, HEIGHT - 100)
    
    elif game_state["stato"] == "MENU_DIFF":
        # difficulty menu
        disegna_testo("DIFFICOLTÀ", FONT_TITLE, YELLOW, 200)
        disegna_testo("F: Facile | M: Media | D: Difficile", FONT_TEXT, TEXT_COLOR, 350)
        disegna_hint_ritorno_menu(HEIGHT - 80, "MENU_DIFF")
    
    elif game_state["stato"] in ["GIOCO", "FINE"]:
        # game screen
        disegna_gioco_state(game_state)
    
    elif game_state["stato"] == "CONFERMA_ABBANDONO":
        # abandon confirm
        disegna_conferma_abbandono()
    
    pygame.display.flip()


# state management

def inizializza_stato():
    # init game state
    return {
        "stato": "MENU_MODO",
        "modalita": "",
        "difficolta": "",
        "limite": 0,
        "parola_segreta": "",
        "tentativi_fatti": [],
        "current_guess": "",
        "start_time": 0,
        "messaggio_fine": "",
        "tempo_pausa": 0,
        "view_start_row": 0
    }


def reset_game_state(game_state):
    # reset to main menu
    game_state["stato"] = "MENU_MODO"
    game_state["modalita"] = ""
    game_state["difficolta"] = ""
    game_state["limite"] = 0
    game_state["parola_segreta"] = ""
    game_state["tentativi_fatti"] = []
    game_state["current_guess"] = ""
    game_state["start_time"] = 0
    game_state["messaggio_fine"] = ""
    game_state["view_start_row"] = 0


# event handling

def processa_evento_menu_modo(event, game_state, credits_button_rect):
    # main menu events
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if credits_button_rect.collidepoint(event.pos):
                game_state["stato"] = "MENU_CREDITI"
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_t:
            game_state["stato"] = "MENU_DIFF"
            game_state["modalita"] = "tempo"
        elif event.key == pygame.K_c:
            game_state["stato"] = "MENU_DIFF"
            game_state["modalita"] = "tentativi"


def processa_evento_menu_crediti(event, game_state):
    # credits menu events
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            game_state["stato"] = "MENU_MODO"


def processa_evento_menu_diff(event, game_state):
    # difficulty menu events
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            reset_game_state(game_state)
        elif event.key in [pygame.K_f, pygame.K_m, pygame.K_d]:
            difficolta = event.unicode.upper()
            game_state["difficolta"] = difficolta
            game_state["limite"] = imposta_difficolta(game_state["modalita"], difficolta)
            game_state["parola_segreta"] = scegli_parola(difficolta)
            game_state["tentativi_fatti"] = []
            game_state["current_guess"] = ""
            game_state["view_start_row"] = 0
            game_state["start_time"] = time.time()
            game_state["stato"] = "GIOCO"


def processa_evento_gioco(event, game_state):
    # game screen events
    if event.type == pygame.MOUSEWHEEL:
        # scroll with mouse
        righe_totali = 6
        max_view = max(0, len(game_state["tentativi_fatti"]) - righe_totali + 1)
        
        if event.y > 0:
            game_state["view_start_row"] = max(0, game_state["view_start_row"] - 1)
        elif event.y < 0:
            game_state["view_start_row"] = min(max_view, game_state["view_start_row"] + 1)
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            game_state["stato"] = "CONFERMA_ABBANDONO"
            game_state["tempo_pausa"] = time.time()
        elif event.key == pygame.K_BACKSPACE:
            game_state["current_guess"] = game_state["current_guess"][:-1]
        elif event.key == pygame.K_RETURN:
            if len(game_state["current_guess"]) == len(game_state["parola_segreta"]):
                colori = valuta_tentativo_gui(game_state["current_guess"], game_state["parola_segreta"])
                game_state["tentativi_fatti"].append((game_state["current_guess"], colori))
                
                # auto scroll
                righe_totali = 6
                max_view = max(0, len(game_state["tentativi_fatti"]) - righe_totali + 1)
                game_state["view_start_row"] = max_view
                
                if game_state["current_guess"] == game_state["parola_segreta"]:
                    game_state["messaggio_fine"] = "COMPLIMENTI!"
                    game_state["stato"] = "FINE"
                elif game_state["modalita"] == "tentativi" and len(game_state["tentativi_fatti"]) >= game_state["limite"]:
                    game_state["messaggio_fine"] = f"PAROLA: {game_state['parola_segreta']}"
                    game_state["stato"] = "FINE"
                
                game_state["current_guess"] = ""
        elif event.unicode.isalpha() and len(game_state["current_guess"]) < len(game_state["parola_segreta"]):
            game_state["current_guess"] += event.unicode.upper()
    
    # time check
    if game_state["modalita"] == "tempo" and time.time() - game_state["start_time"] >= game_state["limite"]:
        game_state["stato"] = "FINE"
        game_state["messaggio_fine"] = f"TEMPO SCADUTO! Era: {game_state['parola_segreta']}"


def processa_evento_fine(event, game_state):
    # end screen events
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            reset_game_state(game_state)


def processa_evento_conferma_abbandono(event, game_state):
    # abandon confirm events
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            reset_game_state(game_state)
        elif event.key == pygame.K_n:
            game_state["stato"] = "GIOCO"
            game_state["start_time"] += time.time() - game_state["tempo_pausa"]


def processa_evento(event, game_state, credits_button_rect):
    # event dispatcher
    if event.type == pygame.QUIT:
        return False
    
    if game_state["stato"] == "MENU_MODO":
        processa_evento_menu_modo(event, game_state, credits_button_rect)
    elif game_state["stato"] == "MENU_CREDITI":
        processa_evento_menu_crediti(event, game_state)
    elif game_state["stato"] == "MENU_DIFF":
        processa_evento_menu_diff(event, game_state)
    elif game_state["stato"] == "GIOCO":
        processa_evento_gioco(event, game_state)
    elif game_state["stato"] == "FINE":
        processa_evento_fine(event, game_state)
    elif game_state["stato"] == "CONFERMA_ABBANDONO":
        processa_evento_conferma_abbandono(event, game_state)
    
    return True


# game loop

def game_loop(clock):
    # main loop
    game_state = inizializza_stato()
    credits_button_rect = pygame.Rect(WIDTH // 2 - 100, 450, 200, 50)
    
    while True:
        for event in pygame.event.get():
            running = processa_evento(event, game_state, credits_button_rect)
            if not running:
                return
        
        disegna_schermo(game_state, credits_button_rect)
        clock.tick(30)


def main():
    # entry point
    clock = pygame.time.Clock()
    game_loop(clock)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
