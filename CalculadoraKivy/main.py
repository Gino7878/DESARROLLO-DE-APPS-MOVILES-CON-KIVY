from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
import math

from kivy.core.window import Window  

class CalculatorApp(App):
    def build(self):
        self.title = "Calculadora UNT"
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        self.icon = "unt.png"
        return CalculatorTabs()



class CalculatorTabs(TabbedPanel):
    pass

class BasicCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Display
        self.display = TextInput(
            text='0', 
            font_size=32, 
            size_hint=(1, 0.2),
            readonly=True,
            halign='right',
            background_color=[1,1,1,1],
            foreground_color=[0,0,0,1]
        )
        self.add_widget(self.display)
        
        # Botones - CAMBIO: "⌫" por "DEL"
        buttons_layout = GridLayout(cols=4, spacing=5, size_hint=(1, 0.8))
        
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', 'DEL', '(', ')'
        ]
        
        for button in buttons:
            btn = Button(text=button, font_size=24)
            btn.bind(on_press=self.on_button_press)
            buttons_layout.add_widget(btn)
        
        self.add_widget(buttons_layout)
        
        self.expression = ''
    
    def on_button_press(self, instance):
        current_text = self.display.text
        button_text = instance.text
        
        if button_text == 'C':
            self.display.text = '0'
            self.expression = ''
        elif button_text == 'DEL':  # CAMBIO: "⌫" por "DEL"
            if len(current_text) > 1:
                self.display.text = current_text[:-1]
                self.expression = self.expression[:-1]
            else:
                self.display.text = '0'
                self.expression = ''
        elif button_text == '=':
            try:
                result = str(eval(self.expression))
                self.display.text = result
                self.expression = result
            except:
                self.display.text = 'Error'
                self.expression = ''
        else:
            if current_text == '0' or current_text == 'Error':
                self.display.text = button_text
                self.expression = button_text
            else:
                self.display.text += button_text
                self.expression += button_text

class ScientificCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Display
        self.display = TextInput(
            text='0', 
            font_size=32, 
            size_hint=(1, 0.15),
            readonly=True,
            halign='right',
            background_color=[1,1,1,1],
            foreground_color=[0,0,0,1]
        )
        self.add_widget(self.display)
        
        # Botones científicos - CAMBIO: "⌫" por "DEL"
        sci_layout = GridLayout(cols=5, spacing=5, size_hint=(1, 0.85))
        
        sci_buttons = [
            '7', '8', '9', '/', '√',
            '4', '5', '6', '*', 'x²',
            '1', '2', '3', '-', 'sin',
            '0', '.', '=', '+', 'cos',
            'C', 'DEL', '(', ')', 'tan'  # CAMBIO: "⌫" por "DEL"
        ]
        
        for button in sci_buttons:
            btn = Button(text=button, font_size=18)
            btn.bind(on_press=self.on_sci_button_press)
            sci_layout.add_widget(btn)
        
        self.add_widget(sci_layout)
        
        self.expression = ''
        self.special_ops = ['√', 'sin', 'cos', 'tan', 'x²']
    
    def on_sci_button_press(self, instance):
        current_text = self.display.text
        button_text = instance.text
        
        if button_text == 'C':
            self.display.text = '0'
            self.expression = ''
        elif button_text == 'DEL':  # CAMBIO: "⌫" por "DEL"
            if len(current_text) > 1:
                self.display.text = current_text[:-1]
                self.expression = self.expression[:-1]
            else:
                self.display.text = '0'
                self.expression = ''
        elif button_text == '=':
            self.calculate_result()
        elif button_text in self.special_ops:
            self.handle_special_operation(button_text)
        else:
            if current_text == '0' or current_text == 'Error':
                self.display.text = button_text
                self.expression = button_text
            else:
                self.display.text += button_text
                self.expression += button_text
    
    def handle_special_operation(self, op):
        """Maneja operaciones científicas especiales"""
        if op == '√':
            # Para raíz cuadrada: si hay número antes, multiplicar; si no, solo raíz
            if self.expression and self.expression[-1].isdigit():
                self.expression += '*math.sqrt('
                self.display.text += '×√('
            else:
                self.expression += 'math.sqrt('
                self.display.text += '√('
        elif op in ['sin', 'cos', 'tan']:
            # Para funciones trigonométricas
            if self.expression and self.expression[-1].isdigit():
                self.expression += f'*math.{op}(math.radians('
                self.display.text += f'×{op}('
            else:
                self.expression += f'math.{op}(math.radians('
                self.display.text += f'{op}('
        elif op == 'x²':
            self.expression += '**2'
            self.display.text += '²'
    
    def calculate_result(self):
        """Calcula el resultado de la expresión científica"""
        try:
            # Asegurarse de que todos los paréntesis estén cerrados
            open_parens = self.expression.count('(')
            close_parens = self.expression.count(')')
            for _ in range(open_parens - close_parens):
                self.expression += ')'
                self.display.text += ')'
            
            # Evaluar la expresión
            result = eval(self.expression)
            self.display.text = str(round(result, 10))  # Redondear para evitar decimales largos
            self.expression = str(result)
            
        except Exception as e:
            self.display.text = 'Error'
            self.expression = ''

class ComplexCalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Inputs para números complejos
        input_layout = GridLayout(cols=2, spacing=10, size_hint=(1, 0.3))
        
        self.real1 = TextInput(text='0', hint_text='Parte real 1', font_size=20)
        self.imag1 = TextInput(text='0', hint_text='Parte imaginaria 1', font_size=20)
        self.real2 = TextInput(text='0', hint_text='Parte real 2', font_size=20)
        self.imag2 = TextInput(text='0', hint_text='Parte imaginaria 2', font_size=20)
        
        input_layout.add_widget(Label(text='Número 1:', font_size=20, color=[0,0,0,1]))
        input_layout.add_widget(Label(text='', font_size=20))
        input_layout.add_widget(self.real1)
        input_layout.add_widget(self.imag1)
        input_layout.add_widget(Label(text='Número 2:', font_size=20, color=[0,0,0,1]))
        input_layout.add_widget(Label(text='', font_size=20))
        input_layout.add_widget(self.real2)
        input_layout.add_widget(self.imag2)
        
        self.add_widget(input_layout)
        
        # Botones de operaciones
        ops_layout = GridLayout(cols=2, spacing=10, size_hint=(1, 0.4))
        
        complex_buttons = [
            'SUMA', 'RESTA', 'MULTIPLICACIÓN', 'DIVISIÓN'
        ]
        
        for button in complex_buttons:
            btn = Button(text=button, font_size=20)
            btn.bind(on_press=self.on_complex_operation)
            ops_layout.add_widget(btn)
        
        self.add_widget(ops_layout)
        
        # Resultado
        self.result_display = TextInput(
            text='Resultado: 0+0j', 
            font_size=24, 
            size_hint=(1, 0.3),
            readonly=True,
            halign='center',
            background_color=[1,1,1,1],
            foreground_color=[0,0,0,1]
        )
        self.add_widget(self.result_display)
    
    def on_complex_operation(self, instance):
        try:
            # Crear números complejos
            z1 = complex(float(self.real1.text), float(self.imag1.text))
            z2 = complex(float(self.real2.text), float(self.imag2.text))
            
            operation = instance.text
            
            if operation == 'SUMA':
                result = z1 + z2
            elif operation == 'RESTA':
                result = z1 - z2
            elif operation == 'MULTIPLICACIÓN':
                result = z1 * z2
            elif operation == 'DIVISIÓN':
                if z2 != 0:
                    result = z1 / z2
                else:
                    self.result_display.text = 'Error: División por cero'
                    return
            
            self.result_display.text = f'Resultado: {result}'
            
        except ValueError:
            self.result_display.text = 'Error: Entrada inválida'
        except Exception as e:
            self.result_display.text = f'Error: {str(e)}'

if __name__ == '__main__':
    CalculatorApp().run()