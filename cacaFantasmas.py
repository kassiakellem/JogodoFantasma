from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label  # Importa Label para exibir pontuação e tempo
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
import random
import time

# Classe base para elementos do jogo (Fantasmas e Bombas)
class GameElement(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 100)
        # Posição inicial aleatória dentro dos limites da tela
        self.pos = (random.randint(0, 300), random.randint(0, 500))
        # Agenda o movimento do elemento
        self.movement_event = Clock.schedule_interval(self.mover, 0.5)

    def mover(self, dt):
        """Move o elemento para uma nova posição aleatória"""
        self.pos = (random.randint(0, 300), random.randint(0, 500))

    def stop_movement(self):
        """Cancela o evento de movimento quando o elemento é removido"""
        if self.movement_event:
            self.movement_event.cancel()

class Fantasma(GameElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "Fantasma.png"  # Imagem do fantasma

class Bomba(GameElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Imagem da bomba. 
        self.source = "Bomb_Stock_Photography_PNG-removebg-preview.png"

class CacaFantasmas(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pontos = 0
        self.tempo_total_jogo = 30  # Duração total do jogo em segundos
        self.tempo_restante = self.tempo_total_jogo
        self.level = 1  # Nível inicial do jogo
        self.game_over = False  # Flag para indicar se o jogo acabou
        self.layout = FloatLayout()
        self.menu_ativo = True
        self.score_label = None  # Referência para o rótulo da pontuação
        self.time_label = None   # Referência para o rótulo do tempo
        self.game_update_event = None  # Para armazenar o evento de atualização do jogo

    def mostrar_menu(self):
        """Exibe o menu inicial com um GIF animado de fundo"""
        self.layout.clear_widgets()

        # Criando o GIF de fundo
        fundo_menu = Image(source="Caveira.gif", allow_stretch=True, size_hint=(1, 1))

        # Criando o botão para começar
        botao = Button(text="Começar!", size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        botao.bind(on_press=self.iniciar_jogo)

        # Adiciona o fundo e o botão ao layout
        self.layout.add_widget(fundo_menu)
        self.layout.add_widget(botao)

    def build(self):
        self.mostrar_menu()  # Exibe o menu inicial
        return self.layout

    def iniciar_jogo(self, instance):
        """Inicia o jogo, removendo o menu e adicionando fantasmas"""
        self.layout.clear_widgets()
        self.menu_ativo = False

        # Reinicia o estado do jogo
        self.pontos = 0
        self.level = 1
        self.game_over = False
        self.tempo_restante = self.tempo_total_jogo

        # Adiciona elementos de UI para pontuação e tempo
        self.score_label = Label(text=f"Pontos: {self.pontos}", size_hint=(None, None), size=(200, 50), pos=(10, 550), font_size='20sp', color=(1,1,1,1))
        self.time_label = Label(text=f"Tempo: {int(self.tempo_restante)}s", size_hint=(None, None), size=(200, 50), pos=(250, 550), font_size='20sp', color=(1,1,1,1))
        self.layout.add_widget(self.score_label)
        self.layout.add_widget(self.time_label)

        # Adiciona fantasmas iniciais
        for _ in range(5):  # Começa com 5 fantasmas
            self.adicionar_fantasma()

        # Agenda o loop principal de atualização do jogo
        self.game_update_event = Clock.schedule_interval(self.update_game, 1)  # Atualiza a cada segundo

    def update_game(self, dt):
        """Loop principal de atualização do jogo: lida com tempo, progressão de nível e fim de jogo"""
        if self.game_over:
            self.fim_de_jogo() # Garante que a tela final seja mostrada se o jogo já acabou
            return

        self.tempo_restante -= dt
        self.time_label.text = f"Tempo: {int(self.tempo_restante)}s"

        if self.tempo_restante <= 0:
            self.game_over = True
            self.fim_de_jogo()
            return

        # Progressão de nível: transição para o Nível 2 após 10 pontos
        if self.level == 1 and self.pontos >= 10:
            self.level = 2
            print("Nível 2 alcançado! Bombas aparecerão.")
            # Adiciona algumas bombas ao entrar no Nível 2
            for _ in range(2):  # Adiciona 2 bombas
                self.adicionar_bomba()

    def adicionar_fantasma(self):
        """Adiciona um novo fantasma ao jogo"""
        if not self.game_over and self.tempo_restante > 0:
            fantasma = Fantasma()
            # Vincula o evento de toque ao fantasma
            fantasma.bind(on_touch_down=lambda _, touch: self.tocar_fantasma(fantasma) if fantasma.collide_point(*touch.pos) and not self.game_over else None)
            self.layout.add_widget(fantasma)

    def adicionar_bomba(self):
        """Adiciona uma nova bomba ao jogo"""
        if not self.game_over and self.tempo_restante > 0:
            bomba = Bomba()
            # Vincula o evento de toque à bomba
            bomba.bind(on_touch_down=lambda _, touch: self.tocar_bomba(bomba) if bomba.collide_point(*touch.pos) and not self.game_over else None)
            self.layout.add_widget(bomba)

    def tocar_fantasma(self, fantasma):
        """Lida com o clique em um fantasma"""
        if self.game_over: # Impede ações se o jogo já acabou
            return

        self.pontos += 1
        self.score_label.text = f"Pontos: {self.pontos}"
        self.layout.remove_widget(fantasma)  # Remove o fantasma clicado
        fantasma.stop_movement()  # Para o movimento do fantasma removido
        self.adicionar_fantasma()  # Adiciona outro fantasma

    def tocar_bomba(self, bomba):
        """Lida com o clique em uma bomba (aciona o fim de jogo)"""
        if self.game_over: # Impede ações se o jogo já acabou
            return

        self.game_over = True
        print("Bomba clicada! Fim de jogo.")
        self.fim_de_jogo()

    def fim_de_jogo(self):
        """Exibe a tela final do jogo"""
        if self.game_update_event:
            Clock.unschedule(self.game_update_event)  # Para o loop principal de atualização do jogo

        # Para o movimento de todos os elementos do jogo existentes e os remove
        for widget in list(self.layout.children):  # Itera sobre uma cópia para evitar problemas durante a remoção
            if isinstance(widget, GameElement):
                widget.stop_movement()
                self.layout.remove_widget(widget)

        self.layout.clear_widgets()  # Limpa todos os widgets do layout

        # Mensagem de Fim de Jogo
        game_over_label = Label(text=f"Fim de Jogo!\nPontos Finais: {self.pontos}",
                                font_size='30sp',
                                pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                color=(1,1,1,1))

        # Botão de Reiniciar
        restart_button = Button(text="Jogar Novamente",
                                size_hint=(None, None),
                                size=(250, 60),
                                pos_hint={'center_x': 0.5, 'center_y': 0.4})
        restart_button.bind(on_press=self.reiniciar_jogo)

        self.layout.add_widget(game_over_label)
        self.layout.add_widget(restart_button)

    def reiniciar_jogo(self, instance):
        """Reinicia o jogo e mostra o menu principal"""
        self.mostrar_menu()

CacaFantasmas().run()

