import tkinter as tk
from tkinter import ttk
import re

leyes_simplificacion = [
    #Solo leyes basicas para simplificar!
    (r'¬\(¬(\w+)\)', r'\1', "Ley de Involución: ¬(¬p) ≡ p"),
    (r'(\w+) ∧ \1', r'\1', "Ley de Idempotencia: p ∧ p ≡ p"),
    (r'(\w+) ∨ \1', r'\1', "Ley de Idempotencia: p ∨ p ≡ p"),
    (r'(\w+) ∧ (\w+)', r'\2 ∧ \1', "Ley Conmutativa: p ∧ q ≡ q ∧ p"),
    (r'(\w+) ∨ (\w+)', r'\2 ∨ \1', "Ley Conmutativa: p ∨ q ≡ q ∨ p"), 
    (r'\((\w+) ∧ (\w+)\) ∧ (\w+)', r'\1 ∧ (\2 ∧ \3)', "Ley Asociativa: (p ∧ q) ∧ r ≡ p ∧ (q ∧ r)"),
    (r'\((\w+) ∨ (\w+)\) ∨ (\w+)', r'\1 ∨ (\2 ∨ \3)', "Ley Asociativa: (p ∨ q) ∨ r ≡ p ∨ (q ∨ r)"),
    (r'(\w+) ∨ \(\1 ∨ (\w+)\)', r'(\1 ∨ \1) ∨ \2', "Ley Asociativa: (p ∨ q) ∨ r ≡ p ∨ (q ∨ r)"),
    (r'(\w+) ∧ \((\w+) ∨ (\w+)\)', r'(\1 ∧ \2) ∨ (\1 ∧ \3)', "Leyes Distributivas: p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r)"),
    (r'(\w+) ∧ \((\w+) ∨ (\w+)\)', r'(\1 ∧ \2) ∨ (\1 ∧ \3)', "Leyes Distributivas: p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r)"),
    (r'¬\((\w+) ∨ (\w+)\)', r'¬\1 ∧ ¬\2', "Ley de De Morgan: ¬(p ∨ q) ≡ ¬p ∧ ¬q"),
    (r'¬\((\w+) ∧ (\w+)\)', r'¬\1 ∨ ¬\2', "Ley de De Morgan: ¬(p ∧ q) ≡ ¬p ∨ ¬q"),
    (r'¬\(¬(\w+) ∨ (\w+)\)', r'\1 ∧ ¬\2', "Ley de De Morgan: ¬(¬p ∨ q) ≡ p ∧ ¬q"),
    (r'¬\(¬(\w+) ∧ (\w+)\)', r'\1 ∨ ¬\2', "Ley de De Morgan: ¬(¬p ∧ q) ≡ p ∨ ¬q"),
    (r'¬\((\w+) ∧ ¬(\w+)\)', r'¬\1 ∨ \2', "Ley de De Morgan: ¬(p ∧ ¬q) ≡ ¬p ∨ q"),
    (r'¬\((\w+) ∨ ¬(\w+)\)', r'¬\1 ∧ \2', "Ley de De Morgan: ¬(p ∨ ¬q) ≡ ¬p ∧ q"),
    (r'(\w+) ⇒ (\w+)', r'¬\1 ∨ \2', "Leyes del Condicional: p ⇒ q ≡ ¬p ∨ q"),
    (r'(\w+) ⇔ (\w+)', r'(\1 ⇒ \2) ∧ (\2 ⇒ \1)', "Ley del Bicondicional: (p ⇔ q) ≡ (p ⇒ q) ∧ (q ⇒ p)"),
    (r'(\w+) ∨ True', r'\1', "Leyes de Identidad: p ∨ True = p"),
    (r'(\w+) ∧ True', r'\1', "Leyes de Identidad: p ∧ True = p"),
    (r'(\w+) ∨ False', r'\1', "Leyes de Identidad: p ∨ False = p"),
    (r'(\w+) ∧ False', 'False', "Leyes de Identidad: p ∧ False = False"),
    (r'(\w+) ∧ \(\1 ∨ (\w+)\)', r'\1', "Ley de Absorción: p ∧ (p ∨ q) ≡ p"),
    (r'(\w+) ∨ \(\1 ∧ (\w+)\)', r'\1', "Ley de Absorción: p ∨ (p ∧ q) ≡ p"),
    (r'\((\w+) ∨ (\w+)\) ∧ \(\1 ∨ (\w+)\)', r'\1 ∨ (\1 ∨ \2)', "Ley de Reducción de Disyunción"),
    (r'\((\w+) ∨ (\w+)\) ∧ \((\w+) ∨ ¬(\w+)\)', r'\1', "Ley de Simplificación"),
    (r'(\w+) ∧ \((\w+) ∨ (\w+)\)', r'(\1 ∧ \2) ∨ (\1 ∧ \3)', "Ley de Distribución de Conjunción sobre Disyunción \n(inversa)"),
    (r'(\w+) ∧ \((\w+) ⇒ (\w+)\)', r'(\1 ∧ \2) ⇒ (\1 ∧ \3)', "Ley de Distribución de Conjunción sobre Implicación"),
    (r'(\w+) ∨ \((\w+) ∧ (\w+)\)', r'(\1 ∨ \2) ∧ (\1 ∨ \3)', "Ley de Distribución de Disyunción sobre Conjunción"),
    (r'(\w+) ∨ \((\w+) ⇒ (\w+)\)', r'(\1 ∨ \2) ⇒ (\1 ∨ \3)', "Ley de Distribución de Disyunción sobre Implicación"),
    (r'True ∨ (\w+)', 'True', "Restricción de Tautología: True ∨ p ≡ True"),
    (r'False ∧ (\w+)', 'False', "Restricción de Tautología: False ∧ p ≡ False")
]

def centrar_ventana(ventana):
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    if ventana == mprincipal:
        x = (ancho_pantalla - ventana.winfo_reqwidth()) // 2
        y = (alto_pantalla - ventana.winfo_reqheight()) // 2 - 150
    else: 
        x = (ancho_pantalla - ventana.winfo_reqwidth()) // 2 - 300
        y = (alto_pantalla - ventana.winfo_reqheight()) // 2 - 200
    ventana.geometry("+{}+{}".format(x, y))

def cerrar_ventana(ventana):
    ventana.destroy()

def simplificar_proposicion(oracion, resultado_pasos):
    prop_inicial = prop = oracion.get()
    pasos = []  
    for patron, sustitucion, descripcion in leyes_simplificacion:
        nueva_prop = re.sub(patron, sustitucion, prop)
        if nueva_prop != prop:
            prop = nueva_prop
            pasos.append(descripcion + ": \n" + prop)

    resultado_pasos.config(state=tk.NORMAL)
    resultado_pasos.delete(1.0, tk.END)
    
    resultado_pasos.insert(tk.END, "Proposicion original: " + prop_inicial + "\n")
    resultado_pasos.insert(tk.END, "Pasos de simplificacion: \n\n")
    for paso in pasos:
        resultado_pasos.insert(tk.END,  paso + "\n")
        print(paso)
    
    resultado_pasos.config(state=tk.DISABLED)

def calculadora():
    cerrar_ventana(mprincipal)
    calculadora_sec = tk.Tk()
    calculadora_sec.title("Simplificación de Proposiciones Lógicas")
    calculadora_sec.geometry("900x400")
    calculadora_sec.resizable(False, False)
    centrar_ventana(calculadora_sec )
    
    separador = ttk.PanedWindow(calculadora_sec, orient="horizontal")
    separador.pack(fill="both", expand=True)

    seccion_calculadora = ttk.Frame(separador)
    separador.add(seccion_calculadora)
    seccion_pasos = ttk.Frame(separador)
    separador.add(seccion_pasos)
    
    titulo_calc = ttk.Label(seccion_calculadora, text="SIMPLIFICADOR DE PROPOSICIONES", font=("Roboto", 17, "bold"), justify='center')
    titulo_calc.place(x=10, y=10)
    guiatexto1 = "Ingrese una proposición lógica utilizando los botones y/o caracteres del teclado y luego presione 'Simplificar' para obtener el resultado. \n\nNo olvide respetar los espacios que correspondan!\nEjemplo: (p ⇔ q)"
    texto1 = tk.Label(seccion_calculadora, text=guiatexto1, wraplength=450, justify='left')
    texto1.place(x=10, y=40)
    oracion = ttk.Entry(seccion_calculadora, width=70)
    oracion.pack(pady=130, padx=10)

    boton1 = ttk.Button(seccion_calculadora, text="AND", command=lambda: agregar_caracter("∧"))
    boton2 = ttk.Button(seccion_calculadora, text="NOT", command=lambda: agregar_caracter("¬"))
    boton3 = ttk.Button(seccion_calculadora, text="OR", command=lambda: agregar_caracter("∨"))
    boton4 = ttk.Button(seccion_calculadora, text="COND", command=lambda: agregar_caracter("⇒"))
    boton5 = ttk.Button(seccion_calculadora, text="BICOND", command=lambda: agregar_caracter("⇔"))
    boton1.place(x=20, y=170)
    boton2.place(x=100, y=170)
    boton3.place(x=180, y=170)
    boton4.place(x=260, y=170)
    boton5.place(x=340, y=170)

    boton_simplificar = ttk.Button(seccion_calculadora, text="Simplificar", command=lambda:simplificar_proposicion(oracion,resultado_pasos))
    boton_simplificar.place(x=180,y=210)

    scrollbar_pasos = ttk.Scrollbar(seccion_pasos)
    scrollbar_pasos.pack(side="right", fill="y")
    
    resultado_pasos = tk.Text(seccion_pasos, wrap="none", yscrollcommand=scrollbar_pasos.set)
    resultado_pasos.config(state=tk.DISABLED)
    resultado_pasos.pack(fill="both", expand=True)

    ayuda = ttk.Button(calculadora_sec, text="(?)", width=4, style="Custom.TButton", command=ventana_ayuda)
    ayuda.place(x=400, y=350)

    def agregar_caracter(caracter):
        cursor_pos = oracion.index(tk.INSERT)
        oracion.insert(cursor_pos, caracter + " ")
        cursor_pos = oracion.index(tk.INSERT)

        #Bloquear espacio
        calculadora_sec.bind('<space>', lambda event: None) 
        oracion.focus_set() 
        calculadora_sec.after(100, lambda: calculadora_sec.bind('<space>', lambda event: agregar_caracter(" ")))  

def ventana_ayuda():
    vent_ayuda = tk.Toplevel()
    vent_ayuda.title("Ayuda")
    vent_ayuda.geometry("400x450")
    vent_ayuda.resizable(False,False)
    cerrar_ayuda = ttk.Button(vent_ayuda, text="Cerrar", command=lambda:cerrar_ventana(vent_ayuda))
    cerrar_ayuda.place(x=110, y=230)

    texto_and = "\nBotón 'AND' (∧): Utiliza este botón para insertar el operador lógico 'AND' (conjunción) en tu expresión lógica. El operador 'AND' se utiliza para representar la intersección o la conjunción de dos proposiciones."
    texto_not = "\nBotón 'NOT' (¬): Utiliza este botón para insertar el operador lógico 'NOT' (negación) en tu expresión lógica. El operador 'NOT' se utiliza para representar la negación o la inversión de una proposición."
    texto_or = "\nBotón 'OR' (v): Utiliza este botón para insertar el operador lógico 'OR' (disyunción) en tu expresión lógica. El operador 'OR' se utiliza para representar la unión o la disyunción de dos proposiciones."
    texto_cond = "\nBotón 'COND' (⇒): Utiliza este botón para insertar el operador lógico 'COND' (implicación) en tu expresión lógica. El operador 'COND' se utiliza para representar la implicación lógica entre dos proposiciones."
    texto_bicond = "\nBotón 'BICOND' (⇔): Utiliza este botón para insertar el operador lógico 'BICOND' (bicondicional) en tu expresión lógica. El operador 'BICOND' se utiliza para representar la equivalencia lógica entre dos proposiciones."
    
    guia_text = tk.Label(vent_ayuda, text="GUIA DE USO DE BOTONES", font=("Roboto", 14, "bold"))
    guia_text.pack()
    textoguia1 = ttk.Label(vent_ayuda, text=texto_and, wraplength=360, justify='left')
    textoguia1.pack()
    textoguia2 = ttk.Label(vent_ayuda, text=texto_not, wraplength=360, justify='left')
    textoguia2.pack()
    textoguia3 = ttk.Label(vent_ayuda, text=texto_or, wraplength=360, justify='left')
    textoguia3.pack()
    textoguia4 = ttk.Label(vent_ayuda, text=texto_cond, wraplength=360, justify='left')
    textoguia4.pack()
    textoguia5 = ttk.Label(vent_ayuda, text=texto_bicond, wraplength=360, justify='left')
    textoguia5.pack()
    vent_ayuda.grab_set()

mprincipal = tk.Tk()
mprincipal.title("Menu Principal")
mprincipal.geometry("300x300")
mprincipal.resizable(False,False)
centrar_ventana(mprincipal)

style = ttk.Style()
style.configure("Custom.TButton", font=("Arial", 10))

nombre = tk.Label(mprincipal, text="SimpliLogic", font=("Verdana", 28,"bold"), justify='center')
nombre.pack(pady=20)
subtitulo = tk.Label(mprincipal, text="Logica Proposicional", font=("Verdana", 12,), justify='center')
subtitulo.pack()
text = tk.Label(mprincipal, text="¡Bienvenido a Mi Programa de Simplificación Lógica!", wraplength=200, font=("Verdana", 10,), justify='center')
text.pack(pady=10)
inicio = ttk.Button(mprincipal, text="Comenzar",width=10, style="Custom.TButton", command=calculadora)
inicio.pack(pady=50)

mprincipal.mainloop()
