import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Cargar variables de entorno
load_dotenv()

# Protocolo de mensajes entre agentes
class Mensaje:
    def __init__(self, origen, destino, contenido):
        self.origen = origen
        self.destino = destino
        self.contenido = contenido

class BusMensajes:
    def __init__(self):
        self.mensajes = []
    def enviar_mensaje(self, origen, destino, contenido):
        mensaje = Mensaje(origen, destino, contenido)
        self.mensajes.append(mensaje)
        print(f"\n>>> Mensaje enviado de '{origen}' a '{destino}'")
    def recibir_mensaje(self, destino):
        for i, mensaje in enumerate(self.mensajes):
            if mensaje.destino == destino:
                print(f"\n>>> '{destino}' recibio mensaje de '{mensaje.origen}'")
                return self.mensajes.pop(i)
        return None

# Agente Investigador
class ResearchAgent:
    def __init__(self, bus):
        self.bus = bus
        self.nombre = 'Agente Investigador'
        # Cada agente tiene su propia instancia de LLM (arquitectura descentralizada)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY").strip('"'),
            temperature=0.3
        )
        self.rol = "Experto en busqueda de informacion"
    
    def investigar(self, tema):
        print(f"\n{'='*80}")
        print(f"[{self.nombre}] Rol: {self.rol}")
        print(f"[{self.nombre}] Iniciando investigacion sobre: {tema}")
        print(f"{'='*80}")
        
        prompt = f"""Eres un investigador experto en tecnologia. Investiga sobre el tema: {tema}
        
Proporciona:
- Puntos clave y conceptos principales
- Datos relevantes y estadisticas recientes
- Tendencias actuales en el area
- Aplicaciones practicas

Formato: Lista estructurada de datos investigados."""
        
        datos = self.llm.invoke(prompt).content
        print(f"\n[{self.nombre}] Investigacion completada.")
        print(f"\nDATOS ENCONTRADOS:\n{datos[:300]}...")
        
        self.bus.enviar_mensaje(self.nombre, 'Agente Redactor', datos)

# Agente Redactor
class WriterAgent:
    def __init__(self, bus):
        self.bus = bus
        self.nombre = 'Agente Redactor'
        # Cada agente tiene su propia instancia de LLM (arquitectura descentralizada)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY").strip('"'),
            temperature=0.5  # Temperatura ligeramente mas alta para creatividad
        )
        self.rol = "Experto en redaccion creativa y tecnica"
    
    def redactar(self):
        mensaje = self.bus.recibir_mensaje(self.nombre)
        if mensaje:
            print(f"\n{'='*80}")
            print(f"[{self.nombre}] Rol: {self.rol}")
            print(f"[{self.nombre}] Redactando articulo basado en la investigacion...")
            print(f"{'='*80}")
            
            prompt = f"""Eres un redactor profesional de contenido tecnologico. Basandote en la siguiente informacion de investigacion, redacta un articulo completo para un blog de tecnologia:

DATOS DE INVESTIGACION:
{mensaje.contenido}

Requisitos del articulo:
- Titulo atractivo y profesional
- Introduccion enganchadora
- Desarrollo claro y estructurado con subtitulos
- Conclusion impactante
- Lenguaje profesional pero accesible
- Longitud: articulo completo y detallado

Redacta el articulo completo ahora:"""
            
            borrador = self.llm.invoke(prompt).content
            print(f"\n[{self.nombre}] Borrador completado.")
            print(f"\nBORRADOR (preview):\n{borrador[:300]}...")
            
            self.bus.enviar_mensaje(self.nombre, 'Agente Editor', borrador)

# Agente Editor
class EditorAgent:
    def __init__(self, bus):
        self.bus = bus
        self.nombre = 'Agente Editor'
        # Cada agente tiene su propia instancia de LLM (arquitectura descentralizada)
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY").strip('"'),
            temperature=0.2  # Temperatura mas baja para precision en edicion
        )
        self.rol = "Experto en cumplimiento de estilo y gramatica"
    
    def revisar(self):
        mensaje = self.bus.recibir_mensaje(self.nombre)
        if mensaje:
            print(f"\n{'='*80}")
            print(f"[{self.nombre}] Rol: {self.rol}")
            print(f"[{self.nombre}] Revisando y editando el borrador...")
            print(f"{'='*80}")
            
            prompt = f"""Eres un editor profesional de contenido tecnologico. Revisa y mejora el siguiente borrador de articulo:

BORRADOR:
{mensaje.contenido}

Tareas de edicion:
- Corregir errores gramaticales y ortograficos
- Mejorar la claridad y coherencia
- Optimizar la estructura y flujo
- Verificar que el tono sea profesional
- Asegurar que la informacion sea precisa
- Eliminar frases de mensaje y solo regresar el artículo completo

Proporciona el articulo final editado y pulido:"""
            
            articulo_final = self.llm.invoke(prompt).content
            
            print(f"\n{'='*80}")
            print(f"TAREA COMPLETADA! Articulo Finalizado.")
            print(f"{'='*80}")
            print(f"\nARTICULO FINAL:\n")
            print(articulo_final)
            print(f"\n{'='*80}")

# Flujo de trabajo principal
def flujo_trabajo(tema):
    print(f"\n{'#'*80}")
    print(f"SISTEMA MULTIAGENTE - GENERACION DE CONTENIDO PARA BLOG")
    print(f"{'#'*80}")
    print(f"\nTema: {tema}")
    print(f"\nArquitectura: Horizontal (Colaboracion entre pares)")
    print(f"Agentes: Investigador -> Redactor -> Editor")
    print(f"{'#'*80}")
    
    bus = BusMensajes()
    investigador = ResearchAgent(bus)
    redactor = WriterAgent(bus)
    editor = EditorAgent(bus)

    # Flujo de trabajo secuencial
    investigador.investigar(tema)
    redactor.redactar()
    editor.revisar()

if __name__ == "__main__":
    tema_blog = input("Ingresa el tema a investigar: ")
    flujo_trabajo(tema_blog)

