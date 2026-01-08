import os
import google.generativeai as genai

api_key_value = os.getenv("GEMINI_API_KEY")

if not api_key_value:
    print("Error: No s'ha trobat la clau API.")
else:
    genai.configure(api_key=api_key_value.strip())
    
    # Intentem detectar quin nom de model accepta la teva clau exactament
    try:
        # 1. Obtenim tots els models que poden generar contingut
        tots_els_models = genai.list_models()
        models_aptes = []
        
        for m in tots_els_models:
            if 'generateContent' in m.supported_generation_methods:
                models_aptes.append(m.name)

        # 2. Triem quin model utilitzar
        nom_model = ""
        
        # Preferim el 'gemini-1.5-flash' si està disponible
        for nom in models_aptes:
            if "gemini-1.5-flash" in nom:
                nom_model = nom
                break # Ja l'hem trobat, sortim del bucle
        
        # Si no hem trobat el flash, agafem el primer de la llista
        if not nom_model and models_aptes:
            nom_model = models_aptes[0]

        # 3. Configurem el model final
        if nom_model:
            model = genai.GenerativeModel(nom_model)
            print(f"Connexió establerta amb el model: {nom_model}")
        else:
            print("No s'ha trobat cap model compatible.")

    except Exception as e:
        print(f"Error en la configuració: {e}")

set_de_dades = ""

opcio = ""
while opcio != "d":
    print("\n--- GESTOR DE SETS DE DADES AMB IA ---")
    print("a) Generar un nou set de dades.")
    print("b) Visualitzar set de dades.")
    print("c) Eliminar sets de dades.")
    print("d) Sortir")
    
    opcio = input("Selecciona una opció (a-d): ").lower()

    match(opcio):
        case "a":
            print("\n--- GENERACIÓ DE DADES ---")
            tema = input("Sobre quin tema vols les dades? (ex: usuaris, inventari, vendes): ")
            quantitat = input("Quants registres necessites?: ")
            format_dades = input("Quin format prefereixes? (CSV, JSON o SQL): ")
            
            # Preparem la instrucció (prompt) per a la IA
            prompt = (f"Genera un set de dades de prova sobre '{tema}'. "
                      f"Necessito {quantitat} registres en format {format_dades}. "
                      "Si us plau, retorna només el codi o les dades, sense explicacions inicials.")
            
            try:
                print("⏳ Connectant amb Gemini per generar les dades...")
                resposta = model.generate_content(prompt)
                set_de_dades = resposta.text
                print("Set de dades generat correctament!")
            except Exception as e:
                print(f"Hi ha hagut un error en la generació: {e}")

        case "b":
            if set_de_dades:
                print("\n--- VISUALITZACIÓ DEL SET DE DADES ---")
                print(set_de_dades)
            else:
                print("\nNo hi ha cap set de dades generat. Utilitza l'opció 'a' primer.")

        case "c": # Eliminem el set de dades
            if set_de_dades:
                set_de_dades = ""
                print("\nEl set de dades s'ha eliminat de la memòria.")
            else: # Si no hi ha mostrem que ja està buida
                print("\nLa memòria ja està buida.")

        case "d": # Opció per sortir
            print("\nSortint del programa...")
            
        case _:
            print("\nOpció no vàlida. Introdueix una lletra de la 'a' a la 'd'.")