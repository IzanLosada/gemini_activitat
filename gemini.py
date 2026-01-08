import os
import ast
import google.generativeai as genai

api_key_value = os.getenv("GEMINI_API_KEY")
if not api_key_value:
    print("Error: No se ha encontrado la clave API.")
    exit()

genai.configure(api_key=api_key_value.strip())

try:
    model_name = next(
        m.name for m in genai.list_models()
        if "generateContent" in m.supported_generation_methods
    )
    model = genai.GenerativeModel(model_name)
    print(f"Conectado con éxito al modelo: {model_name}")
except Exception as e:
    print(f"Error fatal al detectar modelo: {e}")
    exit()

# Diccionario de listas
listas = {}

def limpiar_y_convertir(text):
    text = text.replace("```python", "").replace("```", "").strip()
    try:
        return ast.literal_eval(text)
    except:
        return []

opcio = ""
while opcio != "d":
    print("\n--- GESTOR DE LISTAS PYTHON ---")
    print("a) Generar nueva lista.")
    print("b) Visualizar lista.")
    print("c) Eliminar lista.")
    print("d) Salir")
    
    opcio = input("Selecciona una opción (a-d): ").lower()

    match opcio:
        case "a":
            nombre_lista = input("Introduce el nombre de la lista: ").strip()

            if nombre_lista in listas:
                print("Error: ya existe una lista con ese nombre.")
                continue

            tema = input("¿Sobre qué tema quieres los nombres?: ")
            cant = input("¿Cuántos elementos?: ")

            prompt = (
                f"Genera una lista de Python de tipo string con {cant} elementos sobre '{tema}'. "
                "Responde SOLAMENTE la lista de strings. Sin introducciones ni comentarios. "
                "Ejemplo: ['Nombre1', 'Nombre2']"
            )

            try:
                print("Generando...")
                res = model.generate_content(prompt)
                lista_generada = limpiar_y_convertir(res.text)

                if lista_generada:
                    listas[nombre_lista] = lista_generada
                    print(f"Lista '{nombre_lista}' guardada con {len(lista_generada)} elementos.")
                else:
                    print("Error: la IA no respondió con el formato de lista esperado.")
            except Exception as e:
                print(f"Error en la petición: {e}")

        case "b":
            if not listas:
                print("No hay listas guardadas.")
                continue

            print("\nListas disponibles:")
            for nombre in listas:
                print(f"- {nombre}")

            nombre_lista = input("Introduce el nombre de la lista a visualizar: ").strip()

            if nombre_lista in listas:
                print(f"\n--- LISTA: {nombre_lista} ---")
                for i, nombre in enumerate(listas[nombre_lista], 1):
                    print(f"{i}. {nombre}")
            else:
                print("La lista indicada no existe.")

        case "c":
            nombre_lista = input("Introduce el nombre de la lista a eliminar: ").strip()

            if nombre_lista in listas:
                del listas[nombre_lista]
                print(f"Lista '{nombre_lista}' eliminada.")
            else:
                print("La lista indicada no existe.")

        case "d":
            print("Saliendo...")
