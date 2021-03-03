from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen,NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window
import decision_tree as dt
from xml.etree import ElementTree as ET
from kivy.metrics import dp, sp

class Parser_DecisionTree:
    def __init__(self, file_name):
        self.root = ET.parse(file_name).getroot()

    def create_tree(self):
        node = self.root[0]
        return self.create_node(node)

    def create_node(self, node):
        t = node.find('type')
        if (t == None):
            return None

        type = t.text
        if (type == "categorical"):
            return self.create_categorical(node)
        if (type == "range"):
            return self.create_range(node)
        if (type == "decision"):
            return self.create_decision(node)

        return None

    def create_categorical(self, node):
        cat_node = dt.CategoricalNode()
        query = node.find('query')
        for line in query:
            cat_node.addQueryLine(line.text)

        categories = node.find("categories")
        node_children = node.find("node_children")
        for cat, child in zip(categories, node_children):
            category = self.create_category(cat)
            node_child = self.create_node(child)
            cat_node.addChild(category, node_child)

        return cat_node

    def create_category(self, cat):
        desc = cat.find('description').text
        category = dt.Category(desc)
        return category

    def create_range(self, node):
        u = node.find('unit')
        if (u == None):
            unit = 'und.'
        else:
            unit = u.text
        rang_node = dt.RangeNode(unit)

        query = node.find('query')
        for line in query:
            rang_node.addQueryLine(line.text)

        thresholds = node.find("thresholds")
        node_children = node.find("node_children")
        for th, child in zip(thresholds, node_children):
            threshold = self.create_threshold(th)
            node_child = self.create_node(child)
            rang_node.addChild(node_child, threshold)

        return rang_node

    def create_threshold(self, th):
        threshold = dt.Threshold()
        interval = th.find('interval').text
        if (interval == 'unbounded'):
            threshold.interval = dt.UNBOUNDED_INTERVAL
            threshold.value = float("inf")
        else:
            if (interval == 'open'):
                threshold.interval = dt.OPEN_INTERVAL
            else:
                threshold.interval = dt.CLOSED_INTERVAL
            threshold.value = float(th.find('upper_bound').text)
        return threshold

    def create_decision(self, node):
        desc = node.find('description').text
        return dt.DecisionNode(desc)

parser = Parser_DecisionTree('sbem_new.xml')
tree = parser.create_tree()
no_aux = tree

alternatives = []
Window.clearcolor = (255, 255, 0, 0)
class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)


class Iniciar(Screen):
    def __init__(self, **kwargs):
        super(Iniciar, self).__init__(**kwargs)
        lock = FloatLayout()
        self.btn = Button(text='INICIAR',size_hint=(None, None), pos_hint={'center_x': .5, 'y': .08},size = (dp(130), dp(80)) ,background_color=(0, 0, 1.60, 1),font_size=sp(28), color=(.8, .9, 0, 1))
        self.img2 = Image(source='tina3.png', size_hint=(None, None), size=(dp(330), dp(330)),
                          pos_hint={'center_x': .5, 'center_y': .62})
        self.btn.bind(on_press=self.press_button)
        lock.add_widget(self.img2)
        lock.add_widget(self.btn)
        self.add_widget(lock)

        self.config()

    def press_button(self,*args):
        global alternatives
        for c in no_aux.categories:
                alternatives.append(c.description)
        self.manager.get_screen('categorical').config()
        alternatives = []
        self.manager.current='categorical'
    def config(self):
        global alternatives
        alternatives = []

class Decision(Screen):
    def __init__(self, **kwargs):
        super(Decision, self).__init__(**kwargs)
        floate = FloatLayout()


        self.balao = Image(source='baloon2.png', size_hint=(None, None), size=(dp(360), dp(360)),
                           pos_hint={'center_x': .50, 'center_y': .70})
        self.tina = Image(source='tina2.png', size_hint=(None, None), size=(dp(200), dp(200)),
                          pos_hint={'center_x': .62, 'center_y': .35})

        self.label = Button(text='', size_hint=(None, None), pos_hint={'center_x': .50, 'center_y': .72},size = (dp(80), dp(80)),color=(0,0,0,1),
                             background_color=(2.55, 2.55, 2.55, 0), text_size=(330, None), font_size='15sp')

        self.reload = Image(source='reload.png', size_hint=(None, None), size = (dp(80), dp(80)),
                            pos_hint={'center_x': .50, 'y': .08})

        self.button = Button(text='', size_hint=(None, None), pos_hint={'center_x': .50, 'y': .08},size = (dp(80), dp(80)),
                             background_color=(2.55, 2.55, 0, 0), font_size='18sp')
        self.button.bind(on_press=self.press_button)
        floate.add_widget(self.balao)
        floate.add_widget(self.tina)
        floate.add_widget(self.button)
        floate.add_widget(self.reload)
        floate.add_widget(self.label)
        self.add_widget(floate)


    def press_button(self, *args):
        global no_aux
        global tree
        global parser
        parser = Parser_DecisionTree('sbem_new.xml')
        tree = parser.create_tree()
        no_aux = tree
        self.manager.get_screen('iniciar').config()
        self.manager.current = 'iniciar'

    def config(self):


        self.label.text=no_aux.description
        if len(no_aux.description) > 100:
            self.label.font_size='13sp'
        else:
            self.label.font_size='13sp'

class Categorical(Screen):
    def __init__(self, **kwargs):
        super(Categorical, self).__init__(**kwargs)

        self.id = 'categorical_id'

        floate = FloatLayout()

        self.balao = Image(source='baloon.png', size_hint=(None, None), size=(dp(360), dp(360)),
                           pos_hint={'center_x': .50, 'center_y': .75})
        self.tina = Image(source='tina2.png', size_hint=(None, None), size=(dp(200), dp(200)),
                          pos_hint={'center_x': .38, 'center_y': .40})

        self.label = Button(text='', size_hint=(None, None), pos_hint={'center_x': .52, 'center_y': .77},color=(0,0,0,1),
                             background_color=(2.55, 2.55, 2.55, 0), text_size=(330, None))

        floate.add_widget(self.balao)
        floate.add_widget(self.tina)
        floate.add_widget(self.label)


        self.button_a = Button(text='',size_hint=(.2, .1), pos_hint={'center_x': .39, 'y': .13},background_color=(0, 0, 1.60, 1),font_size=28, color=(.8, .9, 0, 1))
        self.button_a.id='1'
        self.button_b = Button(text='', size_hint=(.2, .1), pos_hint={'center_x': .60, 'y': .13},background_color=(0, 0, 1.60, 1), font_size=28, color=(.8, .9, 0, 1))
        self.button_b.id='2'
        self.button_c = Button(text='', size_hint=(.2, .1), pos_hint={'center_x': .39, 'y': .02},background_color=(0, 0, 1.60, 1), font_size=28, color=(.8, .9, 0, 1))
        self.button_c.id='3'
        self.button_d = Button(text='', size_hint=(.2, .1), pos_hint={'center_x': .60, 'y': .02},background_color=(0, 0, 1.60, 1), font_size=28, color=(.8, .9, 0, 1))
        self.button_d.id='4'
        floate.add_widget(self.button_a)
        floate.add_widget(self.button_b)
        floate.add_widget(self.button_c)
        floate.add_widget(self.button_d)

        self.add_widget(floate)

    def config(self):
        lines = ''
        count=0
        if len(no_aux.query) > 1:
            for c in no_aux.query:
                count+=1
                lines+=c
                lines+='\n'
            self.label.text = lines
            self.label.font_size='10sp'
        else:
            self.label.text = no_aux.query[0]
            self.label.font_size='18sp'
        if len(alternatives)==4:
            self.button_a.text=alternatives[0]
            self.button_a.bind(on_press=self.press_button)

            self.button_b.text=alternatives[1]
            self.button_b.bind(on_press=self.press_button)

            self.button_c.text=alternatives[2]
            self.button_c.background_color = (0, 0, 1.60, 1)
            self.button_c.color=(.8, .9, 0, 1)
            self.button_c.bind(on_press=self.press_button)

            self.button_d.text=alternatives[3]
            self.button_d.background_color = (0, 0, 1.60, 1)
            self.button_d.color = (.8, .9, 0, 1)
            self.button_d.bind(on_press=self.press_button)
        elif len(alternatives)==2:
            self.button_a.text = alternatives[0]
            self.button_a.bind(on_press=self.press_button)

            self.button_b.text = alternatives[1]
            self.button_b.bind(on_press=self.press_button)

            self.button_c.background_color=(2.55, 2.55, 0, 0)
            self.button_c.color=(2.55, 2.55, 0, 0)
            self.button_c.bind(on_press=self.do_nothing)

            self.button_d.background_color=(2.55, 2.55, 0, 0)
            self.button_d.color = (2.55, 2.55, 0, 0)
            self.button_d.bind(on_press=self.do_nothing)
    def do_nothing(self, *args):
        pass

    def press_button(self, button):
        global no_aux
        global alternatives

        pos = int(button.id)
        cat = no_aux.categories[pos - 1]
        no_aux = no_aux.getChild(cat)
        if no_aux != None and (no_aux.is_leaf == False):
            if no_aux.type == dt.CATEGORICAL_NODE:
                alternatives = []
                for c in no_aux.categories:
                    alternatives.append(c.description)
                self.manager.get_screen('categorical').config()
                self.manager.current = 'categorical'
            elif no_aux.type == dt.RANGE_NODE:
                self.manager.get_screen('range').config()
                self.manager.current = 'range'
        else:
            self.manager.get_screen('decision').config()
            self.manager.current = 'decision'

class Range(Screen):
    def __init__(self, **kwargs):
        super(Range, self).__init__(**kwargs)

        floate = FloatLayout()

        self.balao = Image(source='baloon.png', size_hint=(None, None), size=(dp(360), dp(360)),
                           pos_hint={'center_x': .50, 'center_y': .75})
        self.tina = Image(source='tina2.png', size_hint=(None, None), size=(dp(200), dp(200)),
                          pos_hint={'center_x': .38, 'center_y': .40})

        self.label = Button(text='', size_hint=(None, None), pos_hint={'center_x': .52, 'center_y': .77},
                            color=(0, 0, 0, 1),
                            background_color=(2.55, 2.55, 2.55, 0), text_size=(330, None), font_size='18sp')

        floate.add_widget(self.balao)
        floate.add_widget(self.tina)
        floate.add_widget(self.label)

        self.input = TextInput(multiline=False, size_hint=(.2, .06), pos_hint={'center_x':.50, 'y':0.15}, font_size='26sp', hint_text='(mm)')
        self.button = Button(text='ENVIAR', size_hint=(.2, .1), pos_hint={'center_x': .50, 'y': .01}, background_color=(0, 0, 1.60, 1), font_size=28, color=(.8, .9, 0, 1))
        self.button.bind(on_press=self.press_button)

        floate.add_widget(self.button)
        floate.add_widget(self.input)
        self.add_widget(floate)

    def config(self):

        global no_aux
        self.label.text = no_aux.query[0]

    def press_button(self, button):
        global no_aux
        global alternatives
        entry = self.input.text
        if entry != str and entry != '':
            try:
                no_aux = no_aux.getChild(float(entry))
                if no_aux != None and (no_aux.is_leaf == False):
                    if no_aux.type == dt.CATEGORICAL_NODE:
                        alternatives = []
                        for c in no_aux.categories:
                            alternatives.append(c.description)
                        self.manager.get_screen('categorical').config()
                        self.manager.current = 'categorical'
                    elif no_aux.type == dt.RANGE_NODE:
                        self.manager.get_screen('range').config()
                        self.manager.current = 'range'
                else:
                    self.manager.get_screen('decision').config()
                    self.manager.current = 'decision'
            except:
                pass

class Application(App):
    def build(self):
        sm = ScreenManagement(transition=NoTransition())
        sm.add_widget(Iniciar(name='iniciar'))
        sm.add_widget(Categorical(name='categorical'))
        sm.add_widget(Decision(name='decision'))
        sm.add_widget(Range(name='range'))

        return sm


if __name__ == "__main__":
    Application().run()