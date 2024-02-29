import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from funcion import parse_input as parse_funcion_input
from variable import parse_input as parse_variable_input
from ciclo import parse_input as parse_ciclo_input
from condicional import parse_input as parse_condicional_input

def analyze_input():
    input_text = entry.get()
    tokens, lexeme_count, valid = None, None, False

    if 'def' in input_text.lower():
        tokens, lexeme_count, valid = parse_funcion_input(input_text)
    elif any(op in input_text for op in {'int', 'float', 'string', '='}):
        tokens, lexeme_count, valid = parse_variable_input(input_text)
    elif 'while' in input_text.lower():
        tokens, lexeme_count, valid = parse_ciclo_input(input_text)
    elif 'if' in input_text.lower():
        tokens, lexeme_count, valid = parse_condicional_input(input_text)
    else:
        messagebox.showwarning("Advertencia", "No se puede determinar qué tipo de análisis sintáctico realizar. Por favor, asegúrese de ingresar una cadena válida.")

    # Actualizar la tabla de salida
    if tokens is not None:
        # Limpiar tabla
        for row in token_tree.get_children():
            token_tree.delete(row)
        
        # Insertar datos en la tabla
        for token, lexeme in tokens:
            token_tree.insert("", "end", values=(token, lexeme, lexeme_count.get(lexeme, 0)))

        if valid:
            valid_var.set("La cadena es válida.")
            valid_label.config(fg="green")  # Cambiar color del texto a verde
        else:
            valid_var.set("La cadena es inválida.")
            valid_label.config(fg="red")  # Cambiar color del texto a rojo

# Crear la ventana principal
window = tk.Tk()
window.title("Análisis Sintáctico")

# Función para configurar la expansión de columnas y filas
def configure_grid():
    for i in range(3):
        window.grid_columnconfigure(i, weight=1)
    window.grid_rowconfigure(1, weight=1)

# Estilo de la interfaz
bg_color = "#f0f0f0"
window.configure(bg="#E6E6FA")  # Cambiar el color de fondo de la ventana a lavanda

label_font = ("Arial", 12, "bold")  # Establecer el texto en negrita
entry_font = ("Arial", 12)
button_font = ("Arial", 12, "bold")

# Crear los elementos de la interfaz
input_label = tk.Label(window, text="Ingrese la cadena de texto:", bg=bg_color, font=label_font)
entry = tk.Entry(window, width=50, font=entry_font)
analyze_button = tk.Button(window, text="Analizar", command=analyze_input, font=button_font)

valid_var = tk.StringVar()
valid_label = tk.Label(window, textvariable=valid_var, bg=bg_color, font=label_font)  # Sin color de fondo

# Crear la tabla para mostrar los resultados
token_tree = ttk.Treeview(window, columns=("Token", "Lexema", "Cantidad"), show="headings", height=10)
token_tree.heading("Token", text="Token")
token_tree.heading("Lexema", text="Lexema")
token_tree.heading("Cantidad", text="Cantidad")
token_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")  # Centrar la tabla en la ventana

# Colocar los elementos en la ventana usando la cuadrícula
input_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
entry.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
analyze_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
valid_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

# Configurar expansión de columnas y filas
configure_grid()

# Iniciar el bucle de eventos
window.mainloop()
