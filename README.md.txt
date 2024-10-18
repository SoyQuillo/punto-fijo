Documentación - Método de Punto Fijo 🔢
Santiago Jose Quintero Sanchez 192154
Descripción del Proyecto 👀
El proyecto implementa el método de punto fijo, una técnica iterativa para encontrar soluciones aproximadas a ecuaciones de la forma f(x) = 0. A través de una interfaz gráfica, el usuario puede ingresar una función, un valor inicial y una tolerancia, generando resultados paso a paso y una gráfica de la función.

Requisitos del Proyecto 🚀
Python 3.12.2
Dependencias: Instalar con el siguiente comando:
pip install -r requirements.txt
Estructura del Código 🏗
Interfaz gráfica (customtkinter): Se configura un Tabview principal con dos pestañas: una para el cálculo y otra para la guía de uso.
Ingreso de datos: Se utilizan campos de entrada para la función, el valor inicial y la tolerancia.
Resultados: Se muestra una tabla con las iteraciones, errores aproximados y el resultado final en una interfaz amigable.
Gráficas: Se genera una gráfica de la función con las intersecciones de los puntos calculados.
Uso de la Aplicación 🛠
Entrada de la función: Ingrese una función en términos de x. El sistema despejará g(x) para el cálculo.
Valor inicial: Proporcione un valor de partida para las iteraciones.
Tolerancia: Introduzca el error máximo permitido. Las iteraciones se detendrán cuando se alcance esta tolerancia.
Calcular: Haga clic en el botón "Calcular" para iniciar el proceso y ver los resultados.
Ejemplo de Uso 💻
Ingrese la función x - e^(-x).
Proporcione un valor inicial cercano al cero de la función, por ejemplo, 0.5.
Defina una tolerancia de error, como 0.01.
Presione "Calcular". El sistema mostrará los pasos de iteración y la gráfica correspondiente.
Manejador de Errores ❗
La aplicación incluye mensajes para situaciones como:

Números grandes que generan errores de memoria.
Operaciones no válidas como divisiones por cero.
Funciones que no convergen, generando advertencias.
Contribuir 🛠
El código está estructurado en el script principal, sin separación en componentes adicionales. Cualquier contribución futura deberá centrarse en la modularización y optimización del código.