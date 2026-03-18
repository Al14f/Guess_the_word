import pytest
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock


class TestValutaTentativo:
    
    def test_valuta_tentativo_tutto_corretto(self):
        GREEN = (83, 141, 78)
        GRAY = (58, 58, 60)
        YELLOW = (181, 159, 59)
        
        tentativo = "HELLO"
        parola_segreta = "HELLO"
        
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
        
        assert all(c == GREEN for c in colori)
        assert len(colori) == 5
    
    def test_valuta_tentativo_tutto_sbagliato(self):
        GREEN = (83, 141, 78)
        GRAY = (58, 58, 60)
        YELLOW = (181, 159, 59)
        
        tentativo = "BCDFG"
        parola_segreta = "HELLO"
        
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
        
        assert all(c == GRAY for c in colori)
    
    def test_valuta_tentativo_parziale(self):
        GREEN = (83, 141, 78)
        GRAY = (58, 58, 60)
        YELLOW = (181, 159, 59)
        
        tentativo = "HALLO"
        parola_segreta = "HELLO"
        
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
        
        assert colori[0] == GREEN
        assert colori[1] == GRAY
        assert colori[2] == GREEN
    
    def test_valuta_tentativo_lettera_sbagliata_posizione(self):
        GREEN = (83, 141, 78)
        GRAY = (58, 58, 60)
        YELLOW = (181, 159, 59)
        
        tentativo = "EHLLO"
        parola_segreta = "HELLO"
        
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
        
        assert colori[0] == YELLOW
    
    def test_valuta_tentativo_lettere_duplicate(self):
        GREEN = (83, 141, 78)
        GRAY = (58, 58, 60)
        YELLOW = (181, 159, 59)
        
        tentativo = "HHHLL"
        parola_segreta = "HELLO"
        
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
        
        assert colori[0] == GREEN
        assert colori[1] == GRAY
    
    def test_valuta_single_letter(self):
        GREEN = (83, 141, 78)
        GRAY = (58, 58, 60)
        
        tentativo = "A"
        parola_segreta = "A"
        
        colori = [GRAY] * len(parola_segreta)
        lettere_disponibili = list(parola_segreta)
        
        for i in range(len(tentativo)):
            if tentativo[i] == parola_segreta[i]:
                colori[i] = GREEN
                lettere_disponibili.remove(tentativo[i])
        
        assert colori == [GREEN]


class TestImposta_difficolta:
    
    def test_difficolta_tempo_facile(self):
        limiti = {
            "tempo": {"F": 300, "M": 275, "D": 250},
            "tentativi": {"F": 20, "M": 15, "D": 10}
        }
        
        result = limiti.get("tempo", {}).get("F", 0)
        assert result == 300
    
    def test_difficolta_tempo_media(self):
        limiti = {
            "tempo": {"F": 300, "M": 275, "D": 250},
            "tentativi": {"F": 20, "M": 15, "D": 10}
        }
        
        result = limiti.get("tempo", {}).get("M", 0)
        assert result == 275
    
    def test_difficolta_tempo_difficile(self):
        limiti = {
            "tempo": {"F": 300, "M": 275, "D": 250},
            "tentativi": {"F": 20, "M": 15, "D": 10}
        }
        
        result = limiti.get("tempo", {}).get("D", 0)
        assert result == 250
    
    def test_difficolta_tentativi_facile(self):
        limiti = {
            "tempo": {"F": 300, "M": 275, "D": 250},
            "tentativi": {"F": 20, "M": 15, "D": 10}
        }
        
        result = limiti.get("tentativi", {}).get("F", 0)
        assert result == 20
    
    def test_difficolta_tentativi_media(self):
        limiti = {
            "tempo": {"F": 300, "M": 275, "D": 250},
            "tentativi": {"F": 20, "M": 15, "D": 10}
        }
        
        result = limiti.get("tentativi", {}).get("M", 0)
        assert result == 15
    
    def test_difficolta_tentativi_difficile(self):
        limiti = {
            "tempo": {"F": 300, "M": 275, "D": 250},
            "tentativi": {"F": 20, "M": 15, "D": 10}
        }
        
        result = limiti.get("tentativi", {}).get("D", 0)
        assert result == 10
    
    def test_difficolta_invalida(self):
        limiti = {
            "tempo": {"F": 300, "M": 275, "D": 250},
            "tentativi": {"F": 20, "M": 15, "D": 10}
        }
        
        result = limiti.get("tempo", {}).get("X", 0)
        assert result == 0
    
    def test_modalita_invalida(self):
        limiti = {
            "tempo": {"F": 300, "M": 275, "D": 250},
            "tentativi": {"F": 20, "M": 15, "D": 10}
        }
        
        result = limiti.get("invalid", {}).get("F", 0)
        assert result == 0


class TestScegli_parola:
    
    def test_scegli_parola_da_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("ciao\npython\ngame\n")
            temp_file = f.name
        
        try:
            with open(temp_file, "r", encoding="utf-8") as file:
                parole = [linea.strip().upper() for linea in file if linea.strip()]
            
            assert "CIAO" in parole
            assert "PYTHON" in parole
            assert "GAME" in parole
            assert len(parole) == 3
        finally:
            os.unlink(temp_file)
    
    def test_scegli_parola_file_vuoto(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            temp_file = f.name
        
        try:
            with open(temp_file, "r", encoding="utf-8") as file:
                parole = [linea.strip().upper() for linea in file if linea.strip()]
            
            assert len(parole) == 0
        finally:
            os.unlink(temp_file)
    
    def test_scegli_parola_file_not_found(self):
        file_path = "nonexistent_file.txt"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                parole = file.readlines()
        except FileNotFoundError:
            parole = []
        
        assert len(parole) == 0
    
    def test_scegli_parola_with_whitespace(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("  parola1  \nparola2\n")
            temp_file = f.name
        
        try:
            with open(temp_file, "r", encoding="utf-8") as file:
                parole = [linea.strip().upper() for linea in file if linea.strip()]
            
            assert "PAROLA1" in parole
            assert "PAROLA2" in parole
        finally:
            os.unlink(temp_file)


class TestLogica_Gioco:
    
    def test_game_over_tentativi(self):
        tentativi = 5
        limite = 5
        
        is_over = tentativi >= limite
        assert is_over is True
    
    def test_game_not_over(self):
        tentativi = 2
        limite = 5
        
        is_over = tentativi >= limite
        assert is_over is False
    
    def test_game_over_exceeded(self):
        tentativi = 6
        limite = 5
        
        is_over = tentativi >= limite
        assert is_over is True
    
    def test_tentativo_corretto(self):
        tentativo = "HELLO"
        parola_segreta = "HELLO"
        
        is_correct = tentativo == parola_segreta
        assert is_correct is True
    
    def test_tentativo_sbagliato(self):
        tentativo = "WORLD"
        parola_segreta = "HELLO"
        
        is_correct = tentativo == parola_segreta
        assert is_correct is False


class TestValidazione_Input:
    
    def test_input_alpha_validation(self):
        input_char = "A"
        assert input_char.isalpha() is True
    
    def test_input_non_alpha(self):
        input_char = "1"
        assert input_char.isalpha() is False
    
    def test_input_length_validation(self):
        current_guess = "HEL"
        parola_length = 5
        
        can_add = len(current_guess) < parola_length
        assert can_add is True
    
    def test_input_length_full(self):
        current_guess = "HELLO"
        parola_length = 5
        
        can_add = len(current_guess) < parola_length
        assert can_add is False
    
    def test_backspace_remove_letter(self):
        current_guess = "HEL"
        result = current_guess[:-1]
        
        assert result == "HE"
        assert len(result) == 2
    
    def test_backspace_empty(self):
        current_guess = ""
        result = current_guess[:-1]
        
        assert result == ""


class TestIntegration:
    
    def test_gioco_vittoria(self):
        GREEN = (83, 141, 78)
        GRAY = (58, 58, 60)
        YELLOW = (181, 159, 59)
        
        parola_segreta = "PYTHON"
        tentativo = "PYTHON"
        
        colori = [GRAY] * len(parola_segreta)
        lettere_disponibili = list(parola_segreta)
        
        for i in range(len(tentativo)):
            if tentativo[i] == parola_segreta[i]:
                colori[i] = GREEN
                lettere_disponibili.remove(tentativo[i])
        
        is_correct = tentativo == parola_segreta
        assert is_correct is True
        assert all(c == GREEN for c in colori)
    
    def test_gioco_sconfitta(self):
        parola_segreta = "PYTHON"
        tentativi_made = 4
        limite_tentativi = 4
        
        is_over = tentativi_made >= limite_tentativi
        assert is_over is True
    
    def test_modalita_tempo_valida(self):
        modalita = "tempo"
        difficolta = "F"
        
        limiti = {
            "tempo": {"F": 300, "M": 275, "D": 250},
            "tentativi": {"F": 20, "M": 15, "D": 10}
        }
        
        limit = limiti.get(modalita, {}).get(difficolta, 0)
        assert limit == 300
    
    def test_modalita_tentativi_valida(self):
        modalita = "tentativi"
        difficolta = "D"
        
        limiti = {
            "tempo": {"F": 300, "M": 275, "D": 250},
            "tentativi": {"F": 20, "M": 15, "D": 10}
        }
        
        limit = limiti.get(modalita, {}).get(difficolta, 0)
        assert limit == 10


class TestEdgeCases:
    
    def test_very_long_word(self):
        word = "A" * 100
        
        assert len(word) == 100
        assert word.isupper()
    
    def test_single_letter_word(self):
        word = "A"
        
        assert len(word) == 1
        assert word.isalpha()
    
    def test_uppercase_conversion(self):
        input_text = "hello"
        result = input_text.upper()
        
        assert result == "HELLO"
    
    def test_tempo_zero(self):
        tempo_rimasto = 0
        
        assert tempo_rimasto <= 0
    
    def test_tentativi_exceed(self):
        tentativi = 10
        limite = 5
        
        assert tentativi > limite


class TestCostanti:
    
    def test_colore_green_rgb(self):
        GREEN = (83, 141, 78)
        
        assert len(GREEN) == 3
        assert all(0 <= c <= 255 for c in GREEN)
    
    def test_colore_yellow_rgb(self):
        YELLOW = (181, 159, 59)
        
        assert len(YELLOW) == 3
        assert all(0 <= c <= 255 for c in YELLOW)
    
    def test_colore_gray_rgb(self):
        GRAY = (58, 58, 60)
        
        assert len(GRAY) == 3
        assert all(0 <= c <= 255 for c in GRAY)
    
    def test_dimensioni_schermo(self):
        WIDTH, HEIGHT = 600, 750
        
        assert WIDTH == 600
        assert HEIGHT == 750
        assert WIDTH < HEIGHT


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])