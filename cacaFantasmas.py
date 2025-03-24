from kivy.app import App
from kivy.uix.image import Image 
from kivy.uix.button import Button 
from kivy.clock import Clock 
from kivy.uix.floatlayout import FloatLayout
import random
import time

class Fantasma(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "Fantasma.png"  # Imagem do fantasma
        self.size_hint = (None, None)
        self.size = (100, 100)
        self.pos = (random.randint(0, 300), random.randint(0, 500))  # Posição aleatória
        
        Clock.schedule_interval(self.mover, 0.5)  # 🔹 Faz o fantasma se mover sozinho
        
    def mover(self, dt):
        # """Move o fantasma para uma nova posição aleatória"""
        self.pos = (random.randint(0, 300), random.randint(0, 500))

class CacaFantasmas(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pontos = 0
        self.tempo_final = time.time() + 30  # O jogo dura 30 segundos
        self.layout = FloatLayout()
        self.menu_ativo = True  # Indica se o menu está ativo

    def mostrar_menu(self):
        # """Mostra o menu inicial com um GIF animado de fundo"""
        self.layout.clear_widgets()
        
        # 🔹 Criando o GIF de fundo dentro do método
        fundo_menu = Image(source="Caveira.gif")
        fundo_menu.size_hint = (1, 1)  # Ocupa toda a tela
        fundo_menu.allow_stretch = True
        
        # 🔹 Criando o botão para começar
        botao = Button(text="Começar!", size_hint=(None, None), size=(200, 50), pos=(100, 300))
        botao.bind(on_press=self.iniciar_jogo)
        
        # 🔹 Adiciona o fundo e o botão ao layout
        self.layout.add_widget(fundo_menu)
        self.layout.add_widget(botao)

    def build(self):
        self.mostrar_menu()  # 🔹 Exibe o menu inicial com o GIF
        return self.layout

    def iniciar_jogo(self, instance):
        # """Inicia o jogo removendo o menu e adicionando fantasmas"""
        self.layout.clear_widgets()  
        self.menu_ativo = False  

        for _ in range(5):  # Começa com 5 fantasmas
            self.adicionar_fantasma()

    def adicionar_fantasma(self):
        if time.time() < self.tempo_final:
            fantasma = Fantasma()
            fantasma.bind(on_touch_down=lambda _, touch: self.tocar_fantasma(fantasma) if fantasma.collide_point(*touch.pos) else None)
            self.layout.add_widget(fantasma)

    def tocar_fantasma(self, fantasma):
        self.pontos += 1
        self.layout.remove_widget(fantasma)  # Remove o fantasma
        self.adicionar_fantasma()  # Adiciona outro

CacaFantasmas().run()
