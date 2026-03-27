import pytest
import pygame
import time
from unittest.mock import Mock, patch
from game import (
    scegli_parola, valuta_tentativo_gui, imposta_difficolta, gestisci_tentativo,
    calcola_tempo_rimasto, calcola_dimensioni_griglia, calcola_righe_visualizzabili,
    valida_input_carattere, disegna_testo, disegna_hint_ritorno_menu,
    inizializza_stato, reset_game_state, processa_evento_menu_modo,
    processa_evento_menu_crediti, processa_evento_menu_diff, processa_evento_gioco,
    processa_evento_fine, processa_evento_conferma_abbandono, processa_evento,
    GREEN, YELLOW, GRAY, disegna_conferma_abbandono, disegna_griglia_gioco,
    disegna_gioco_state, disegna_schermo
)

# ============== SCEGLI_PAROLA ==============
def test_scegli_parola_file_not_found():
    with patch('builtins.open', side_effect=FileNotFoundError):
        assert scegli_parola("F") == "GIOCO"

def test_scegli_parola_empty():
    with patch('builtins.open', create=True) as m:
        m.return_value.__enter__.return_value = []
        assert scegli_parola("F") == "PYTHON"

def test_scegli_parola_returns_string():
    with patch('builtins.open', create=True) as m:
        m.return_value.__enter__.return_value = ["CIAO", "CAVALLO"]
        assert isinstance(scegli_parola("F"), str)

@pytest.mark.parametrize("diff,parole,expected", [
    ("F", ["CAT", "ELEPHANT", "DOG"], ["CAT", "DOG"]),
    ("M", ["CAT", "PYTHON", "ELEPHANT"], ["PYTHON"]),
    ("D", ["CAT", "INFORMATION"], ["INFORMATION"]),
    ("X", ["HELLO"], ["HELLO"]),
])
def test_scegli_parola_by_difficulty(diff, parole, expected):
    with patch('builtins.open', create=True) as m:
        m.return_value.__enter__.return_value = parole
        with patch('random.choice', side_effect=lambda x: x[0]):
            assert scegli_parola(diff) in expected

def test_scegli_parola_no_match():
    with patch('builtins.open', create=True) as m:
        m.return_value.__enter__.return_value = ["CAT"]
        assert scegli_parola("D") == "PYTHON"

# ============== VALUTA_TENTATIVO_GUI ==============
@pytest.mark.parametrize("tentativo,parola,idx_check,colore", [
    ("HELLO", "HELLO", 0, GREEN),
    ("ABCDE", "HELLO", 4, YELLOW),
    ("OLLEH", "HELLO", 0, YELLOW),
])
def test_valuta_tentativo(tentativo, parola, idx_check, colore):
    colori = valuta_tentativo_gui(tentativo, parola)
    assert colori[idx_check] == colore

# ============== IMPOSTA_DIFFICOLTA ==============
@pytest.mark.parametrize("modalita,diff,expected", [
    ("tempo", "F", 300), ("tempo", "M", 275), ("tempo", "D", 250),
    ("tentativi", "F", 20), ("tentativi", "M", 15), ("tentativi", "D", 10),
    ("invalid", "F", 0),
])
def test_imposta_difficolta(modalita, diff, expected):
    assert imposta_difficolta(modalita, diff) == expected

# ============== GESTISCI_TENTATIVO ==============
def test_gestisci_tentativo_corretto():
    assert gestisci_tentativo("HELLO", "HELLO", "tempo", 300, []) == ("FINE", "COMPLIMENTI!")

def test_gestisci_tentativo_sbagliato():
    assert gestisci_tentativo("WORLD", "HELLO", "tempo", 300, []) == ("GIOCO", "")

def test_gestisci_tentativo_incompleto():
    assert gestisci_tentativo("HEL", "HELLO", "tempo", 300, []) == ("GIOCO", "")

def test_gestisci_tentativo_limite():
    tentativi = [("W", [GRAY]*5) for _ in range(19)]
    stato, msg = gestisci_tentativo("X", "Z", "tentativi", 20, tentativi)
    assert stato == "FINE" and "Z" in msg

# ============== CALCOLA_TEMPO ==============
def test_calcola_tempo_valido():
    start = time.time() - 10
    stato, tempo = calcola_tempo_rimasto("tempo", 300, start)
    assert stato == "GIOCO" and 280 <= tempo <= 290

def test_calcola_tempo_scaduto():
    stato, msg = calcola_tempo_rimasto("tempo", 300, time.time() - 400)
    assert stato == "FINE" and "SCADUTO" in msg

def test_calcola_tempo_non_tempo():
    assert calcola_tempo_rimasto("tentativi", 300, time.time()) == ("GIOCO", 0)

# ============== CALCOLA_DIMENSIONI ==============
@pytest.mark.parametrize("parola,num_expected", [
    ("HELLO", 5), ("A", 1), ("A"*20, 20),
])
def test_calcola_dimensioni(parola, num_expected):
    num_L, margin, box_size, _, start_y = calcola_dimensioni_griglia(parola)
    assert num_L == num_expected and margin == 8 and start_y == 150 and box_size > 0

# ============== CALCOLA_RIGHE ==============
@pytest.mark.parametrize("stato,tentativi_count,expect_max_positive", [
    ("GIOCO", 1, False), ("GIOCO", 10, True), ("FINE", 10, True),
])
def test_calcola_righe(stato, tentativi_count, expect_max_positive):
    tentativi = [("T", [GRAY])] * tentativi_count
    righe, max_v = calcola_righe_visualizzabili(stato, tentativi)
    assert righe == 6 and (max_v > 0) == expect_max_positive

# ============== VALIDA_INPUT ==============
@pytest.mark.parametrize("char,expected", [("A", True), ("5", False), ("!", False)])
def test_valida_input(char, expected):
    e = Mock(unicode=char)
    assert valida_input_carattere(e) == expected

# ============== INIZIALIZZA/RESET ==============
def test_inizializza_stato():
    s = inizializza_stato()
    assert s["stato"] == "MENU_MODO" and s["limite"] == 0 and s["tentativi_fatti"] == []

def test_reset_game_state():
    g = {"stato": "FINE", "tentativi_fatti": [("T", [GREEN])]}
    reset_game_state(g)
    assert g["stato"] == "MENU_MODO" and g["tentativi_fatti"] == []

# ============== DISEGNA ==============
@patch('game.SCREEN')
def test_disegna_testo(m):
    disegna_testo("TEST", Mock(), (255, 255, 255), 100)
    assert m.blit.called

@patch('game.SCREEN')
def test_disegna_testo_x_custom(m):
    disegna_testo("TEST", Mock(), (255, 255, 255), 100, x=50)
    assert m.blit.called

@patch('game.disegna_testo')
def test_disegna_hint(m):
    disegna_hint_ritorno_menu(700, "MENU_DIFF")
    assert m.called

@patch('game.disegna_testo')
def test_disegna_hint_no_call(m):
    disegna_hint_ritorno_menu(700, "MENU_MODO")
    assert not m.called

@patch('game.disegna_testo')
def test_disegna_conferma(m):
    disegna_conferma_abbandono()
    assert m.call_count >= 4



@patch('game.disegna_griglia_gioco')
@patch('game.disegna_testo')
def test_disegna_gioco_state_tempo(m1, m2):
    gs = {"modalita": "tempo", "limite": 300, "start_time": time.time() - 50,
          "tentativi_fatti": [], "stato": "GIOCO", "messaggio_fine": "",
          "parola_segreta": "HELLO", "current_guess": "", "view_start_row": 0}
    disegna_gioco_state(gs)
    assert m2.called

@patch('game.disegna_griglia_gioco')
@patch('game.disegna_testo')
def test_disegna_gioco_state_tentativi(m1, m2):
    gs = {"modalita": "tentativi", "limite": 15, "tentativi_fatti": [("T", [GRAY])],
          "stato": "GIOCO", "messaggio_fine": "", "parola_segreta": "HELLO", 
          "current_guess": "", "view_start_row": 0}
    disegna_gioco_state(gs)
    assert m1.called



@patch('game.SCREEN')
@patch('game.disegna_testo')
def test_disegna_schermo_crediti(m1, m2):
    disegna_schermo({"stato": "MENU_CREDITI"}, Mock())
    assert m2.fill.called

@patch('game.SCREEN')
@patch('game.disegna_testo')
def test_disegna_schermo_diff(m1, m2):
    disegna_schermo({"stato": "MENU_DIFF"}, Mock())
    assert m2.fill.called

@patch('game.SCREEN')
@patch('game.disegna_conferma_abbandono')
def test_disegna_schermo_conferma(m1, m2):
    disegna_schermo({"stato": "CONFERMA_ABBANDONO"}, Mock())
    assert m2.fill.called

# ============== EVENT HANDLERS ==============
def test_evento_menu_modo_t():
    g = inizializza_stato()
    e = Mock(type=pygame.KEYDOWN, key=pygame.K_t)
    processa_evento_menu_modo(e, g, Mock())
    assert g["modalita"] == "tempo" and g["stato"] == "MENU_DIFF"

def test_evento_menu_modo_c():
    g = inizializza_stato()
    e = Mock(type=pygame.KEYDOWN, key=pygame.K_c)
    processa_evento_menu_modo(e, g, Mock())
    assert g["modalita"] == "tentativi" and g["stato"] == "MENU_DIFF"

def test_evento_menu_modo_click_crediti():
    g = inizializza_stato()
    rect = pygame.Rect(250, 450, 200, 50)
    e = Mock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(350, 475))
    processa_evento_menu_modo(e, g, rect)
    assert g["stato"] == "MENU_CREDITI"

def test_evento_menu_crediti_esc():
    g = {"stato": "MENU_CREDITI"}
    e = Mock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)
    processa_evento_menu_crediti(e, g)
    assert g["stato"] == "MENU_MODO"

@pytest.mark.parametrize("key,key_attr,expected_diff", [
    (pygame.K_f, "F", "F"), (pygame.K_m, "M", "M"), (pygame.K_d, "D", "D"),
])
def test_evento_menu_diff_difficolta(key, key_attr, expected_diff):
    g = inizializza_stato()
    g["modalita"] = "tempo"
    e = Mock(type=pygame.KEYDOWN, key=key, unicode=key_attr)
    with patch('game.scegli_parola', return_value="HELLO"):
        processa_evento_menu_diff(e, g)
        assert g["difficolta"] == expected_diff and g["stato"] == "GIOCO"

def test_evento_menu_diff_esc():
    g = {"stato": "MENU_DIFF"}
    e = Mock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)
    processa_evento_menu_diff(e, g)
    assert g["stato"] == "MENU_MODO"

def test_evento_gioco_backspace():
    g = {"current_guess": "HEL", "parola_segreta": "HELLO", "tentativi_fatti": [],
         "modalita": "tempo", "start_time": time.time(), "limite": 300, "stato": "GIOCO"}
    e = Mock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE)
    processa_evento_gioco(e, g)
    assert g["current_guess"] == "HE"

def test_evento_gioco_lettera():
    g = {"current_guess": "HE", "parola_segreta": "HELLO", "tentativi_fatti": [],
         "modalita": "tempo", "start_time": time.time(), "limite": 300, "stato": "GIOCO"}
    e = Mock(type=pygame.KEYDOWN, unicode="L")
    processa_evento_gioco(e, g)
    assert g["current_guess"] == "HEL"

@pytest.mark.parametrize("y,expected_row", [(1, 1), (-1, 3)])
def test_evento_gioco_scroll(y, expected_row):
    g = {"view_start_row": 2, "tentativi_fatti": [("T", [GREEN])]*10,
         "modalita": "tempo", "start_time": time.time(), "limite": 300, "stato": "GIOCO"}
    e = Mock(type=pygame.MOUSEWHEEL, y=y)
    processa_evento_gioco(e, g)
    assert g["view_start_row"] == expected_row

def test_evento_gioco_enter_corretto():
    g = {"current_guess": "HELLO", "parola_segreta": "HELLO", "tentativi_fatti": [],
         "modalita": "tempo", "start_time": time.time(), "limite": 300, "stato": "GIOCO",
         "view_start_row": 0, "messaggio_fine": ""}
    e = Mock(type=pygame.KEYDOWN, key=pygame.K_RETURN)
    processa_evento_gioco(e, g)
    assert g["stato"] == "FINE" and "COMPLIMENTI" in g["messaggio_fine"]

def test_evento_gioco_enter_limite():
    g = {"current_guess": "X", "parola_segreta": "Z", "tentativi_fatti": [("W", [GRAY]*5) for _ in range(19)],
         "modalita": "tentativi", "start_time": time.time(), "limite": 20, "stato": "GIOCO",
         "view_start_row": 0}
    e = Mock(type=pygame.KEYDOWN, key=pygame.K_RETURN)
    processa_evento_gioco(e, g)
    assert g["stato"] == "FINE"

def test_evento_gioco_esc():
    g = {"stato": "GIOCO", "modalita": "tempo", "start_time": time.time(), "limite": 300}
    e = Mock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)
    processa_evento_gioco(e, g)
    assert g["stato"] == "CONFERMA_ABBANDONO"

def test_evento_gioco_timeout():
    g = {"stato": "GIOCO", "modalita": "tempo", "start_time": time.time() - 400,
         "limite": 300, "parola_segreta": "HELLO", "messaggio_fine": ""}
    e = Mock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)
    processa_evento_gioco(e, g)
    assert g["stato"] == "FINE"

def test_evento_fine_space():
    g = {"stato": "FINE"}
    e = Mock(type=pygame.KEYDOWN, key=pygame.K_SPACE)
    processa_evento_fine(e, g)
    assert g["stato"] == "MENU_MODO"

def test_evento_conferma_s():
    g = {"stato": "CONFERMA_ABBANDONO"}
    e = Mock(type=pygame.KEYDOWN, key=pygame.K_s)
    processa_evento_conferma_abbandono(e, g)
    assert g["stato"] == "MENU_MODO"

def test_evento_conferma_n():
    g = {"stato": "CONFERMA_ABBANDONO", "start_time": time.time()-50, "tempo_pausa": time.time()-10}
    e = Mock(type=pygame.KEYDOWN, key=pygame.K_n)
    old_t = g["start_time"]
    processa_evento_conferma_abbandono(e, g)
    assert g["stato"] == "GIOCO" and g["start_time"] > old_t

def test_processa_evento_quit():
    g = inizializza_stato()
    e = Mock(type=pygame.QUIT)
    assert processa_evento(e, g, Mock()) == False

def test_processa_evento_dispatch():
    g = {"stato": "MENU_MODO"}
    e = Mock(type=pygame.KEYDOWN, key=pygame.K_t)
    assert processa_evento(e, g, Mock()) == True

# ============== INTEGRATION ==============
def test_integration_vittoria():
    s, msg = gestisci_tentativo("HELLO", "HELLO", "tempo", 300, [])
    assert s == "FINE" and msg == "COMPLIMENTI!"

def test_integration_timeout():
    s, msg = calcola_tempo_rimasto("tempo", 300, time.time() - 400)
    assert s == "FINE" and "SCADUTO" in msg

def test_integration_menu_flow():
    g = inizializza_stato()
    rect = pygame.Rect(250, 450, 200, 50)
    
    e1 = Mock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(350, 475))
    processa_evento_menu_modo(e1, g, rect)
    assert g["stato"] == "MENU_CREDITI"
    
    e2 = Mock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)
    processa_evento_menu_crediti(e2, g)
    assert g["stato"] == "MENU_MODO"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])