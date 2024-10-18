import customtkinter as ctk
import sympy as sp
from PIL import Image
from threading import Timer

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("1250x650")
app.title("Método de Punto Fijo - 192154")
app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)

# Frames globales

mainTab = ctk.CTkTabview(app)
mainTab.pack(pady=20, padx=20, fill="both", expand=True)

calculateTab = mainTab.add("Punto fijo")
calculateTab.columnconfigure(0, weight=1)
calculateTab.columnconfigure(1, weight=1)
calculateTab.rowconfigure(0, weight=1)
calculateTab.rowconfigure(1, weight=1)

documentationTab = mainTab.add("Guía de uso")
documentationTab.columnconfigure(0, weight=1)
documentationTab.rowconfigure(0, weight=1)

# frames contenedores de la tabla

tableScrollableFrame = ctk.CTkScrollableFrame(calculateTab)
tableScrollableFrame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10, rowspan=2)
tableScrollableFrame.columnconfigure(0, weight=1)

inputFrame = ctk.CTkFrame(calculateTab)
inputFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
inputFrame.columnconfigure(0, weight=1)
inputFrame.rowconfigure(0, weight=1)
inputFrame.rowconfigure(1, weight=1)
inputFrame.rowconfigure(2, weight=1)
inputFrame.rowconfigure(3, weight=1)
inputFrame.rowconfigure(4, weight=1)

actionFrame = ctk.CTkFrame(calculateTab)
actionFrame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

# Acciones del pad numérico

actions = [
    "(",
    ")",
    "E",
    "Clear",
    "7",
    "8",
    "9",
    "/",
    "4",
    "5",
    "6",
    "*",
    "1",
    "2",
    "3",
    "+",
    "0",
    ".",
    "-",
    "√()",
    "sin()",
    "cos()",
    "tan()",
    "^",
    "π"
]

# Crear botones de la calculadora
for i in range(len(actions)):
    actionFrame.grid_columnconfigure(i % 4, weight=1)
    actionFrame.grid_rowconfigure(i // 4, weight=1)
    value = actions[i]

    button = ctk.CTkButton(
        actionFrame, text=value, command=lambda text=value: addAction(text)
    )
    button.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="nsew")

# Inputs

functionInput = ctk.CTkEntry(inputFrame, placeholder_text="Ingrese la función")
functionInput.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

initialValueInput = ctk.CTkEntry(inputFrame, placeholder_text="Ingrese el valor inicial")
initialValueInput.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

toleranceInput = ctk.CTkEntry(inputFrame, placeholder_text="Ingrese la tolerancia")
toleranceInput.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

submitInput = ctk.CTkButton(
    inputFrame,
    text="Calcular",
    font=("Arial", 24),
    command=lambda: calculateFixedPoint(),
)
submitInput.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")


# Insertar texto en input
def addAction(text: str):
    functionInput.insert("end", text)
    if text == "Clear":
        functionInput.delete(0, "end")


# Reemplazar caracteres
def parseFn(fn: str):
    fn = fn.replace("^", "**")
    fn = fn.replace("π", "pi")
    fn = fn.replace("√", "root")
    return fn


# Agregar label de error
def showError(e: str):
    errorLabel = ctk.CTkLabel(inputFrame, text=e, text_color="red")
    errorLabel.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
    # Desaparecer después de 3 segundos
    Timer(3, lambda: errorLabel.destroy()).start()


# Lógica del punto fijo
def calculateFixedPoint():
    try:
        # Obtener valores
        fn = parseFn(functionInput.get())
        initialValue = float(initialValueInput.get())
        tolerance = float(toleranceInput.get())
        y = sp.Symbol("y")

        i = 0
        while i < len(fn):
            fnCopy = [*fn]
            # Clonar función y reemplazar "x" por "y" en la copia para despejar la ecuacion
            if fnCopy[i] == "x":
                fnCopy[i] = "y"
                fnCopy = sp.parse_expr("".join(fnCopy))
                solutions = sp.solve(fnCopy, y)

                # Crear tabla
                for solution in solutions:
                    try:
                        # Crear gráfica a partir del último valor
                        createGraphic(
                            solution, createTable(solution, initialValue, tolerance)
                        )
                        return
                    except:
                        pass

            i += 1
            
        raise Exception("La función ingresada no converge")        

    except MemoryError:
        showError("Números demasiado grandes, posible divergencia")
    except OverflowError:
        showError("Números demasiado grandes, posible divergencia")
    except ZeroDivisionError:
        showError("División por cero")
    except ArithmeticError:
        showError("Operación no válida")
    except ValueError:
        showError("Error de Sintaxis")
    except Exception as e:
        showError(e)


def createTable(fn, x0, tolerance) -> float:
    tableFrame = ctk.CTkFrame(tableScrollableFrame)
    tableFrame.grid_columnconfigure([0, 1, 2, 3], weight=1)

    ctk.CTkLabel(tableFrame, fg_color="#155a8f", text="n").grid(
        row=0, column=0, sticky="nsew"
    )
    ctk.CTkLabel(tableFrame, fg_color="#155a8f", text="x").grid(
        row=0, column=1, sticky="nsew"
    )
    ctk.CTkLabel(tableFrame, fg_color="#155a8f", text=fn).grid(
        row=0, column=2, sticky="nsew"
    )
    ctk.CTkLabel(tableFrame, fg_color="#155a8f", text="|eₐ|").grid(
        row=0, column=3, sticky="nsew"
    )

    # Reemplazar x por el valor inicial
    x = sp.Symbol("x")
    n = 1
    e = 0
    while True:
        # Reemplazar x por el valor actual de la iteración
        val = round(float(fn.subs(x, x0).evalf()), 4) # Evaluamos la funcion en el punto inicla x0 y lo redondeamos a 4 decimales
        color = "#155a8f" if n % 2 == 0 else "#1870b1"

        ctk.CTkLabel(tableFrame, text=n, fg_color=color).grid(
            row=n, column=0, sticky="nsew"
        )
        ctk.CTkLabel(tableFrame, text=f"{x0:.4f}", fg_color=color).grid(
            row=n, column=1, sticky="nsew"
        )
        ctk.CTkLabel(tableFrame, text=f"{val:.4f}", fg_color=color).grid(
            row=n, column=2, sticky="nsew"
        )
        ctk.CTkLabel(
            tableFrame, text="-" if n == 1 else f"{e:.4f}%", fg_color=color
        ).grid(row=n, column=3, sticky="nsew")

        # Si la tolerancia es menor al error, se rompe el ciclo
        if e <= tolerance and n != 1:
            break

        # si el valor es cero, ajustar error
        e = 0
        if val != 0:
            e = round(abs((val - x0) / val) * 100, 4)

        x0 = val
        n += 1

        if not (-1 <= sp.diff(fn, x).subs(x, x0) <= 1):
            raise Exception("La función ingresada no converge")

    ctk.CTkLabel(
        tableFrame,
        text=f"El valor aproximado del cero de la función, para un error de {tolerance:.4f}% es de {x0:.4f}",
        fg_color="#144870",
    ).grid(row=n + 1, column=0, sticky="nsew", columnspan=4)
    tableFrame.pack(pady=10, padx=10, fill="both", expand=True)
    return x0


# Crear gráfica
def createGraphic(fn, xf):
    # Imprimir gx, x y la intersección
    #Representa la función g(x) que se obtuvo al despejar la ecuación original.
    x = sp.Symbol("x")
    plot = sp.plotting.plot
    plotter = plot(
        fn,
        show=False,
        line_color="red",
        ylabel=fn,
        legend=True,
    )
    plotter.append( #Esta gráfica se utiliza para encontrar puntos de intersección con g(x), que son las soluciones donde g(x) = x.
        plot(
            x,
            show=False,
            line_color="blue",
            legend=True,
        )[0]
    )
    plotter.append(
        plot(#Representa la aproximación final del valor de x encontrado mediante las iteraciones del método de punto fijo.
            xf,
            show=False,
            line_color="#263238",
            lengend=True,
        )[0]
    )
    plotter.append(#Esta línea sirve para indicar el valor de x donde g(x) = x ha sido alcanzado, que corresponde al punto fijo deseado.
        sp.plot_implicit(
            sp.Eq(x, xf),
            show=False,
            line_color="green",
            legend=True,
        )[0]
    )

    plotter.show()

# Manual de usuario

docsScrollableFrame = ctk.CTkScrollableFrame(documentationTab)
docsScrollableFrame.pack(pady=20, padx=20, fill="both", expand=True)
docsScrollableFrame.columnconfigure(0, weight=1)

ctk.CTkLabel(
    docsScrollableFrame,
    text="Método de Punto Fijo",
    font=("Arial", 24, "bold"),
).pack(pady=10, padx=10, fill="both", expand=True)

ctk.CTkLabel(
    docsScrollableFrame,
    text="SANTIAGO JOSE QUINTERO SANCHEZ",
    font=("Arial", 18, "bold"),
).pack(pady=10, padx=10, fill="both", expand=True)

ctk.CTkLabel(
    docsScrollableFrame,
    text="""
El método de punto fijo es un procedimiento iterativo de tipo abierto que se emplea en el análisis numérico para aproximar la solución de una ecuación f(x) = 0.

La idea principal es reestructurar la ecuación original en una forma equivalente g(x) = x, donde el proceso consiste en iterar a partir de un valor inicial hasta obtener una aproximación que se acerque a cero. Esto se hace calculando recursivamente los valores de g(x) usando el resultado anterior, es decir, xₙ = g(xₙ₋₁).

Para verificar si g(x) converge a cero, se evalúa la primera derivada de g(x). Si es menor o igual a 1, se puede continuar el proceso. De lo contrario, la función diverge y no tiene sentido seguir iterando. Un ejemplo de esto es f(x) = e^(-x) - x, que al despejar x nos da g(x) = e^(-x).

No todos los despejes de x conducirán a una aproximación de la solución. Según el criterio de convergencia, el valor absoluto de la derivada de g(x) debe ser menor o igual a 1; de lo contrario, no convergerá.""",
    font=("Arial", 18),
    wraplength=1000,
    justify="left",
).pack(pady=10, padx=10, fill="both", expand=True)

# Guía de uso

ctk.CTkLabel(
    docsScrollableFrame,
    text="Guía de uso",
    font=("Arial", 24, "bold"),
).pack(pady=10, padx=10, fill="both", expand=True)

guides = [
    {
        "title": "Entrada de la función",
        "description": "En este campo deberás ingresar tu función en términos de x, no en forma f(x) = 0. Simplemente coloca la función en este input, y el sistema se encargará de despejar g(x). La función debe contener al menos una variable xm. Puedes usar el panel numérico en la parte inferior como ayuda. Si la función es fácil de despejar, el sistema mostrará el primer resultado que cumpla con f(x) = 0.",
    },
    {
        "title": "Valor inicial",
        "description": "Introduce el valor inicial de x, desde donde comenzarán las iteraciones. Cuanto más cerca esté este valor del cero de la función, menos iteraciones serán necesarias",
    },
    {
        "title": "Tolerancia de error",
        "description": "Introduce el error permitido en formato porcentual. Se detendrán las iteraciones cuando el error aproximado actual sea menor o igual al límite permitido",
    },
]

for guide in guides:
    ctk.CTkLabel(
        docsScrollableFrame,
        text=f"{guide['title']} {guide['description']}",
        font=("Arial", 18),
        wraplength=1000,
        justify="left",
    ).pack(pady=10, padx=10, fill="both", expand=True)

canvas = ctk.CTkLabel(
    docsScrollableFrame,
    image=ctk.CTkImage(Image.open("./example.png"), size=(1000, 900)),
    text="",
).pack(pady=10, padx=10, fill="both", expand=True)
app.mainloop()
