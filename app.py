import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

questions = [
    {"id": 1, "question": "¿Cuál es el resultado de 3/4 + 2/3?", "correct": "17/12", "oa": "OA6"},
    {"id": 2, "question": "Resuelve: x - 3 = 7", "correct": "10", "oa": "OA13"},
    {"id": 3, "question": "¿Cuál es la pendiente de la recta y = 2x + 1?", "correct": "2", "oa": "OA15"},
    {"id": 4, "question": "Calcula: 2 * (5 - 3)^2", "correct": "8", "oa": "OA8"},
    {"id": 5, "question": "Resuelve: 2x + 3 = 11", "correct": "4", "oa": "OA14"},
    {"id": 6, "question": "¿Cuál es el área de un triángulo de base 6 y altura 4?", "correct": "12", "oa": "OA9"},
    {"id": 7, "question": "Convierte 0,75 a fracción", "correct": "3/4", "oa": "OA7"},
    {"id": 8, "question": "¿Cuál es la media de los números 5, 8, 10?", "correct": "7.67", "oa": "OA16"},
]

def diagnostico(respuestas):
    vacios = set()
    for i, respuesta in enumerate(respuestas):
        if respuesta != questions[i]["correct"]:
            vacios.add(questions[i]["oa"])
    return vacios

def crear_mapa_interactivo(vacios):
    G = nx.DiGraph()

    niveles = {
        "1° Medio": 0,
        "8° Básico": -1,
        "7° Básico": -2,
        "6° Básico": -3,
        "5° Básico": -4
    }

    conceptos = [
        ("OA6", "Fracciones básicas", "5° Básico"),
        ("OA7", "Decimales y fracciones", "6° Básico"),
        ("OA8", "Prioridad de operaciones", "6° Básico"),
        ("OA13", "Ecuaciones simples", "6° Básico"),
        ("OA14", "Ecuaciones de primer grado", "7° Básico"),
        ("OA15", "Funciones lineales", "8° Básico"),
        ("OA9", "Área del triángulo", "6° Básico"),
        ("OA16", "Medidas de tendencia central", "6° Básico"),
    ]

    edges = [
        ("OA6", "OA7"),
        ("OA7", "OA8"),
        ("OA8", "OA14"),
        ("OA13", "OA14"),
        ("OA14", "OA15"),
    ]

    for oa, nombre, nivel in conceptos:
        G.add_node(oa, label=f"{oa}: {nombre}\n({nivel})", level=niveles[nivel])

    for origen, destino in edges:
        G.add_edge(origen, destino)

    net = Network(height="700px", width="100%", directed=True)
    net.force_atlas_2based()

    for node, data in G.nodes(data=True):
        color = "red" if node in vacios else "deepskyblue"
        net.add_node(node, label=data['label'], color=color, title=data['label'])

    for source, target in G.edges():
        net.add_edge(source, target)

    net.set_options("""
    var options = {
      "nodes": {
        "font": {"size": 16},
        "scaling": {"min": 10, "max": 30}
      },
      "edges": {
        "arrows": {"to": {"enabled": true}},
        "smooth": false
      },
      "physics": {
        "enabled": true,
        "stabilization": {"iterations": 100}
      },
      "interaction": {
        "zoomView": true,
        "dragView": true
      }
    }
    """)

    return net

def main():
    st.title("Diagnóstico de Vacíos en Matemáticas - 1° Medio")
    st.markdown("Responde las siguientes preguntas para identificar posibles vacíos académicos.")

    respuestas = []
    for q in questions:
        respuesta = st.text_input(q["question"], value="", key=q["id"])
        respuestas.append(respuesta)

    if st.button("Evaluar"):
        vacios = diagnostico(respuestas)

        st.subheader("Resumen de Resultados")
        for i, respuesta in enumerate(respuestas):
            correcto = questions[i]["correct"]
            if respuesta == correcto:
                st.markdown(f"✅ **{questions[i]['question']}** — Tu respuesta: `{respuesta}`")
            else:
                st.markdown(f"❌ **{questions[i]['question']}** — Tu respuesta: `{respuesta}` | Correcta: `{correcto}`")

        st.subheader("Vacíos Detectados:")
        if vacios:
            for v in vacios:
                pregunta = next(q for q in questions if q['oa'] == v)
                st.markdown(f"🔴 {pregunta['question']} — **OA:** {v} — Correcta: `{pregunta['correct']}`")
        else:
            st.success("No se detectaron vacíos académicos. ¡Bien hecho!")

        st.subheader("Mapa Conceptual Completo")
        net = crear_mapa_interactivo(vacios)
        net.save_graph("mapa_conceptual.html")

        with open("mapa_conceptual.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
        components.html(html_content, height=700, scrolling=True)

if __name__ == "__main__":
    main()
