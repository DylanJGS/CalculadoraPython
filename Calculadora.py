import tkinter as tk
from tkinter import messagebox, simpledialog
from fractions import Fraction
import re

# Clase para la calculadora
class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.geometry("400x500")
        self.config(bg="#f0f0f0")
        self.histoy=[]

        # Campo de texto para mostrar la ecuación
        self.display = tk.Entry(self, font=("Arial", 24), borderwidth=2, relief="ridge", justify='right')
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        # Botones para la calculadora (incluyendo CE y Backspace)
        buttons = [
            '7', '8', '9', '%',
            '4', '5', '6', '/',
            '1', '2', '3', '*',
            '0', '.', '=', '-',
            'CE', '⌫', '', '+'
        ]

        # Crear botones y asignar la acción correspondiente
        for i, button in enumerate(buttons):
            if button == 'CE':
                command = self.clear_display  # Limpiar todo
            elif button == '⌫':
                command = self.backspace  # Borrar último carácter
            elif button == '=':
                command = self.calculate  # Calcular resultado
            else:
                command = lambda b=button: self.append_to_expression(b)  # Agregar a la ecuación         

            tk.Button(self, text=button, font=("Arial", 18), command=command).grid(
                row=(i // 4) + 1, column=(i % 4), sticky="nsew", padx=10, pady=10)
            
        # Configuración de columnas y filas
        for i in range(6):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i % 4, weight=1)    

        # Botón para el historial
        tk.Button(self, text='Historial', font=("Arial", 18), command=self.show_history).grid(
            row=6, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        # Asignar eventos de teclado para calcular con Enter
        self.bind("<Return>", lambda event: self.calculate())
        self.bind("<Key>", self.on_keypress)

    def append_to_expression(self, char):
        # Agregar un carácter a la ecuación
        self.display.insert(tk.END, char)

    def clear_display(self):
        # Limpiar el campo de texto
        self.display.delete(0, tk.END)

    def backspace(self):
        # Borrar el último carácter
        current_text = self.display.get()
        if current_text:
            self.display.delete(len(current_text) - 1, tk.END)

    def calculate(self):
        # Calcular la ecuación
        expression = self.display.get()
        try:
            expression = re.sub(r'(\d+)/(\d+)', r'Fraction(\1, \2)', expression)
            result = eval(expression, {"__builtins__": None}, {"Fraction": Fraction, "abs":abs,"sqrt":None})
            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            
            # Guardar en el historial
            self.history.append(f"{expression} = {result}")

        except Exception as e:
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")
            print("Error:", e)  # Para depurar
            
        def validate_expression(self):
            # Validar la expresión para asegurar que solo contenga caracteres permitidos
            expression = self.display.get()
            valid_pattern = re.compile(r'^[0-9+*/%.-]+$')

            return bool(valid_pattern.match(expression))

    def show_history(self):
        # Mostrar historial de operaciones
        
        if not self.history:
            messagebox.showinfo("Historial", "No hay historial disponible.")
        else:
            history_str = "\n".join(self.history)
            simpledialog.messagebox.showinfo("Historial", history_str)

    def on_keypress(self, event):
        # Validación para aceptar solo caracteres permitidos
        char = event.char
        if not char.isdigit() and char not in {'.', '/', '*', '-', '+', '%'}:
            messagebox.showwarning("Entrada inválida", "Solo se permiten números y operadores.")

# Iniciar la calculadora
if __name__ == "__main__":
    app = Calculator()
    app.mainloop()