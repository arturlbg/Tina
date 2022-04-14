from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.core.text import LabelBase
import decision_tree as dt
from xml.etree import ElementTree as ET
from kivy.metrics import dp, sp
from parser import Parser_DecisionTree

parser = Parser_DecisionTree('arvore.xml')
tree = parser.create_tree()
no_aux = tree
variable_range = -1
range_control = 1
nodes = []
alternatives = []
Window.clearcolor = (255, 255, 0, 0)
class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)


class Iniciar(Screen):
    def __init__(self, **kwargs):
        super(Iniciar, self).__init__(**kwargs)
        layout = FloatLayout()
        self.button_1 = Button(text='CLIQUE\nAQUI', size_hint=(None, None), pos_hint={'center_x': .50, 'y': .13},
                             background_normal='images/new_button.png', size=(dp(150), dp(80)),
                             background_color=(0, 0, 1.60, 1),halign="center",
                             font_size=sp(24))
        self.button_2 = Button(size_hint=(None, None), pos_hint={'center_x': .50, 'y': .02},
                             background_normal='images/instrucao.png',size=(dp(100), dp(100)),
                             font_size=sp(24))
        self.tina = Image(source='images/tina2.png', size_hint=(None, None), size=(dp(270), dp(270)),
                          pos_hint={'center_x': .5, 'center_y': .80})
        self.label_1 = Button(text = "TINA", size_hint=(None, None), pos_hint={'center_x': .50, 'center_y': .57},
                            color=(0,0,1.41,1), font_name="Bauhaus 98", halign="center", font_size=90,
                            background_color=(2.55, 2.55, 2.55, 0), text_size=(400, None))
        self.label_2 = Button(text = "CONSULTORIA EM NÓDULOS DE TIREOIDE VOLTADA PARA USO NA ATENÇÃO PRIMÁRIA", size_hint=(None, None), pos_hint={'center_x': .50, 'center_y': .40},
                            color=(0,0,1.41,1), font_name="Britannic Bold", halign="center", font_size=48,
                            background_color=(2.55, 2.55, 2.55, 0), text_size=(500, None))

        self.button_1.bind(on_press=self.press_button_1)
        self.button_2.bind(on_press=self.press_button_2)

        layout.add_widget(self.label_1)
        layout.add_widget(self.label_2)
        layout.add_widget(self.tina)
        layout.add_widget(self.button_1)
        layout.add_widget(self.button_2)
        self.add_widget(layout)

    def press_button_1(self, *args):
        global alternatives
        for c in no_aux.categories:
            alternatives.append(c.description)
        self.manager.get_screen('categorical').config()
        alternatives = []
        self.manager.current = 'categorical'

    def press_button_2(self, *args):
        self.manager.current='instrucoes'

    def config(self, *args):
        global nodes
        global no_aux
        global variable_range
        global range_control
        global alternatives

        parser = Parser_DecisionTree('arvore.xml')
        tree = parser.create_tree()
        no_aux = tree
        range_control=1
        alternatives=[]
        nodes=[]
        variable_range = -1

class Instrucoes(Screen):
    def __init__(self, **kwargs):
        super(Instrucoes, self).__init__(**kwargs)
        layout = FloatLayout()
        text = "       INSTRUÇÕES:        \n\n\n\n • ESSE APLICATIVO TEM O OBJETIVO DE IDENTIFICAR PACIENTES PORTADORES DE NÓDULOS DE MAIOR RISCO E QUE PORTANTO MERECEM AVALIAÇÃO DO MÉDICO ESPECIALISTA (ENDOCRINOLOGISTA)" \
               "\n\n\n • INSERIR AS INFORMAÇÕES DE CADA NÓDULO INDIVIDUALMENTE \n\n\n • É NECESSÁRIO TER ACESSO A ULTRASSONOGRAFIA DE TIREOIDE E AO RESULTADO DA DOSAGEM DO TSH(HORMÔNIO TIREOESTIMULANTE)"
        self.label = Button(text=text, size_hint=(None, None), pos_hint={'center_x': .50, 'center_y': .58},
                            color=(0,0,1.41,1), font_name="Britannic Bold", halign="center",
                            background_color=(2.55, 2.55, 2.55, 0), text_size=(600, None), font_size=36)
        self.button = Button(text='VOLTAR', size_hint=(None, None),size=(dp(150), dp(80)), pos_hint={'center_x': .50, 'y': .08},
                               background_normal='images/button_red.png',
                               font_size=sp(24))

        layout.add_widget(self.label)
        layout.add_widget(self.button)
        self.button.bind(on_press=self.press_button)

        self.add_widget(layout)

    def press_button(self, *args):
        self.manager.get_screen('iniciar').config()
        self.manager.current = 'iniciar'

class Decision(Screen):
    def __init__(self, **kwargs):
        super(Decision, self).__init__(**kwargs)
        layout = FloatLayout()

        self.label = Button(text='', size_hint=(.8, .5), pos_hint={'center_x': .50, 'center_y': .70},
                            background_normal='images/new_button.png', text_size=(540, None), halign="center",
                            font_size='22sp')
        self.tina = Image(source='images/tina2.png', size_hint=(None, None), size=(dp(165), dp(180)),
                          pos_hint={'center_x': .50, 'center_y': .295})

        self.button = Button(text='REINICIAR', size_hint=(.2, .1), pos_hint={'center_x': .50, 'y': .06},
                           background_normal='images/button_red.png',
                           font_size=28)

        self.button.bind(on_press=self.press_button)
        layout.add_widget(self.button)
        self.add_widget(self.tina)
        layout.add_widget(self.label)
        self.add_widget(layout)


    def press_button(self, *args):
        self.manager.get_screen('iniciar').config()
        self.manager.current = 'iniciar'

    def config(self):
        lines = ''
        for c in no_aux.description:
            lines += c.text
            lines += '\n'
        self.label.text = lines

class Categorical(Screen):
    def __init__(self, **kwargs):
        super(Categorical, self).__init__(**kwargs)

        self.id = 'categorical_id'

        layout = FloatLayout()

        self.label = Button(text='', size_hint=(.8, .5), pos_hint={'center_x': .50, 'center_y': .70},
                            background_normal = 'images/new_button.png', text_size=(540, None), halign="center", font_size='22sp')

        layout.add_widget(self.label)

        self.button_a = Button(text='',size_hint=(.6, .1), pos_hint={'center_x': .505, 'y': .32},
                               halign="center", background_normal = 'images/new_button.png',
                               background_color=(0, 0, 1.60, 1),font_size=38)
        self.button_a.id='1'
        self.button_b = Button(text='', size_hint=(.6, .1), pos_hint={'center_x': .505, 'y': .21},
                               halign="center", background_normal = 'images/new_button.png',
                               background_color=(0, 0, 1.60, 1), font_size=38)
        self.button_b.id='2'
        self.back_button = Button(text='VOLTAR',size_hint=(.4, .1), pos_hint={'center_x': .505, 'y': .06},
                             background_normal = 'images/button_red.png',
                             font_size=28)
        self.back_button.bind(on_press = self.press_back)

        layout.add_widget(self.back_button)
        layout.add_widget(self.button_a)
        layout.add_widget(self.button_b)

        self.add_widget(layout)

    def config(self):
        lines = ''
        count=0

        if len(no_aux.query) > 1:
            for c in no_aux.query:
                count+=1
                lines+=c
                lines+='\n'
            self.label.text = lines
        else:
            self.label.text = no_aux.query[0]

        if len(alternatives)==2:
            text = ''
            lenght_list = [alternatives[0].split("ou"), alternatives[1].split("ou")]
            count = 0
            
            if len(lenght_list[0]) > 1:
                for i in lenght_list[0]:
                    text+=i
                    if count == 0:
                        text+='\nou\n'
                        count+=1
                self.button_a.text = text
                self.button_a.font_size = 36
                count = 0
                text = ''
            else:
                self.button_a.text = alternatives[0]

            if len(lenght_list[1]) > 1:
                for i in lenght_list[1]:
                    text += i
                    if count == 0:
                        text += '\nou\n'
                        count += 1
                self.button_b.text = text
                self.button_b.font_size = 36
                count = 0
                text = ''
            else:
                self.button_b.text = alternatives[1]
            self.button_a.bind(on_press=self.press_button)
            self.button_b.bind(on_press=self.press_button)

    def press_back(self, *args):
        global nodes
        global no_aux
        global alternatives
        global variable_range

        parser = Parser_DecisionTree('arvore.xml')
        tree = parser.create_tree()
        no_aux = tree
        if len(nodes) > 1:
            if len(nodes) == 7:
                del nodes[-1]
                del nodes[-1]
            else:
                del nodes[-1]
                if len(nodes) > 4:
                    if type(nodes[-1]) == float:
                        del nodes[-1]
            for i in nodes:
                no_aux = no_aux.getChild(i)
            if no_aux.type == dt.CATEGORICAL_NODE:
                alternatives = []
                for c in no_aux.categories:
                    alternatives.append(c.description)
                self.manager.get_screen('categorical').config()
                self.manager.current = 'categorical'
            elif no_aux.type == dt.INTERACTIVE_RANGE:
                if len(nodes) == 4:
                    variable_range = -1
                if variable_range == -1:
                    self.manager.current = 'range'
                    self.manager.get_screen('range').config()
                else:
                    no_aux.isVar = True
                    self.manager.get_screen('range').config()
            elif no_aux.type == dt.DECISION_NODE:
                self.manager.get_screen('decision').config()
                self.manager.current = 'decision'
            else:
                self.manager.get_screen('range').var_range()
        elif len(nodes) == 0:
            self.manager.get_screen('iniciar').config()
            self.manager.current = 'iniciar'
        else:
            for c in no_aux.categories:
                alternatives.append(c.description)
            self.manager.get_screen('categorical').config()
            alternatives = []
            self.manager.current = 'categorical'
            del nodes[-1]

    def press_button(self, button):
        global no_aux
        global alternatives
        global nodes

        pos = int(button.id)
        cat = no_aux.categories[pos - 1]
        no_aux = no_aux.getChild(cat)
        nodes.append(cat)
        if no_aux.type == dt.CATEGORICAL_NODE:
            alternatives = []
            for c in no_aux.categories:
                alternatives.append(c.description)
            self.manager.get_screen('categorical').config()
            self.manager.current = 'categorical'
        elif no_aux.type == dt.INTERACTIVE_RANGE:
            self.manager.get_screen('range').config()
            if variable_range == -1:
                self.manager.current = 'range'
        elif no_aux.type == dt.DECISION_NODE:
            self.manager.get_screen('decision').config()
            self.manager.current = 'decision'
        else:
            self.manager.get_screen('range').var_range()


class Range(Screen):
    def __init__(self, **kwargs):
        super(Range, self).__init__(**kwargs)

        layout = FloatLayout()

        self.label = Button(text='', size_hint=(.8, .5), pos_hint={'center_x': .50, 'center_y': .70},
                            background_normal='images/new_button.png', text_size=(540, None), halign="center",
                            font_size='22sp')
        self.back = Button(text='VOLTAR', size_hint=(.2, .1), pos_hint={'center_x': .505, 'y': .04},
                           background_normal='images/button_red.png',
                           font_size=28)
        self.back.bind(on_press = self.press_back)
        layout.add_widget(self.label)

        self.input = TextInput(multiline=False, size_hint=(.3, .08), background_color = (.8, .9, 0, 1),  pos_hint={'center_x':.50, 'y':0.32}, font_size='26sp', hint_text='(mm)')
        self.button = Button(text='ENVIAR', size_hint=(.3, .1), pos_hint={'center_x': .505, 'y': .19}, background_normal = 'images/new_button.png', background_color=(0, 0, 1.60, 1), font_size=28)
        self.button.bind(on_press=self.press_button)

        layout.add_widget(self.button)
        layout.add_widget(self.back)
        layout.add_widget(self.input)
        self.add_widget(layout)

    def config(self):
        global variable_range
        global no_aux
        global alternatives
        global range_control
        global nodes

        if variable_range == -1:
            lines = ''
            for c in no_aux.query:
                lines += c
                lines += '\n'
            self.label.text = lines

        else:
            nodes.append(variable_range)
            no_aux.isVar = True
            range_control += 1
            no_aux = no_aux.getChild(variable_range)
            if no_aux.type == dt.CATEGORICAL_NODE:
                alternatives = []
                for c in no_aux.categories:
                    alternatives.append(c.description)
                self.manager.get_screen('categorical').config()
                self.manager.current = 'categorical'
            elif no_aux.type == dt.INTERACTIVE_RANGE:
                self.manager.get_screen('range').config()
                if variable_range == -1:
                    self.manager.current = 'range'
            elif no_aux.type == dt.DECISION_NODE:
                self.manager.get_screen('decision').config()
                self.manager.current = 'decision'
            else:
                self.manager.get_screen('range').var_range()
    def press_back(self, *args):
        global nodes
        global no_aux
        global alternatives
        global variable_range

        parser = Parser_DecisionTree('arvore.xml')
        tree = parser.create_tree()
        no_aux = tree
        if len(nodes) > 1:
            del nodes[-1]
            if len(nodes) > 4:
                if type(nodes[-1]) == float:
                    del nodes[-1]
            for i in nodes:
                no_aux = no_aux.getChild(i)
            if no_aux.type == dt.CATEGORICAL_NODE:
                alternatives = []
                for c in no_aux.categories:
                    alternatives.append(c.description)
                self.manager.get_screen('categorical').config()
                self.manager.current = 'categorical'
            elif no_aux.type == dt.INTERACTIVE_RANGE:
                if len(nodes) == 4:
                    variable_range = -1
                if variable_range == -1:
                    self.manager.current = 'range'
                    self.manager.get_screen('range').config()
                else:
                    no_aux.isVar = True
                    self.manager.get_screen('range').config()
            elif no_aux.type == dt.DECISION_NODE:
                self.manager.get_screen('decision').config()
                self.manager.current = 'decision'
            else:
                self.manager.get_screen('range').var_range()
        elif len(nodes) == 0:
            self.manager.get_screen('iniciar').config()
            self.manager.current = 'iniciar'
        else:
            for c in no_aux.categories:
                alternatives.append(c.description)
            self.manager.get_screen('categorical').config()
            alternatives = []
            self.manager.current = 'categorical'
            del nodes[-1]

    def press_button(self, button):
        global no_aux
        global alternatives
        global variable_range
        global nodes
        entry = self.input.text
        try:
            if entry != str and entry != '':
                if variable_range == -1:
                    variable_range = float(entry)
                nodes.append(variable_range)
                no_aux = no_aux.getChild(variable_range)
                if no_aux.type == dt.CATEGORICAL_NODE:
                    alternatives = []
                    for c in no_aux.categories:
                        alternatives.append(c.description)
                    self.manager.get_screen('categorical').config()
                    self.manager.current = 'categorical'
                elif no_aux.type == dt.INTERACTIVE_RANGE:
                    self.manager.get_screen('range').config()
                    if variable_range == -1:
                        self.manager.current = 'range'
                elif no_aux.type == dt.DECISION_NODE:
                    self.manager.get_screen('decision').config()
                    self.manager.current = 'decision'
                else:
                    self.manager.get_screen('range').var_range()
        except:
            pass

LabelBase.register(name='Bauhaus 98',
                   fn_regular='Bauhaus.ttf')

LabelBase.register(name='Britannic Bold',
                   fn_regular='britannic-bold.ttf')

class Application(App):
    def build(self):
        sm = ScreenManagement(transition=NoTransition())
        sm.add_widget(Iniciar(name='iniciar'))
        sm.add_widget(Instrucoes(name='instrucoes'))
        sm.add_widget(Categorical(name='categorical'))
        sm.add_widget(Decision(name='decision'))
        sm.add_widget(Range(name='range'))

        return sm


if __name__ == "__main__":
    Application().run()
