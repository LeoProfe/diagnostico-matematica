import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

questions = [
    {"id": 1, "question": "¿Cuál es el resultado de 3/4 + 2/3?", "correct": "17/12"},
    {"id": 2, "question": "Resuelve: x - 3 = 7", "correct": "10"},
    {"id": 3, "question": "¿Cuál es la pendiente de la recta y = 2x + 1?", "correct": "2"},
    {"id": 4, "question": "Calcula: 2 * (5 - 3)^2", "correct": "8"},
    {"id": 5, "question": "Resuelve: 2x + 3 = 11", "correct": "4"},
    {"id": 6, "question": "¿Cuál es el área de un triángulo de base 6 y altura 4?", "correct": "12"},
    {"id": 7, "question": "Convierte 0,75 a fracción", "correct": "3/4"},
    {"id": 8, "question": "¿Cuál es la media de los números 5, 8, 10?", "correct": "7.67"},
]

def diagnostico(respuestas):
    vacios = []
    for i, respuesta in enumerate(respuestas):
        if respuesta != questions[i]["correct"]:
            vacios.append(questions[i]["question"] + f" → Respuesta correcta: {questions[i]['correct']}")
    return vacios

def crear_mapa_conceptual(vacios=[]):
    G = nx.DiGraph()

    conceptos = {
        "Números naturales (5°)": "blue",
        "Fracciones básicas (5°)": "blue",
        "Operaciones básicas (5°)": "blue",
        "Números enteros (6°)": "blue",
        "Operaciones con fracciones y decimales (6°)": "blue",
        "Potencias y raíces (7°)": "blue",
        "Números racionales y reales (8°)": "blue",
        "Operaciones algebraicas (8°)": "blue",

        "Figuras planas (5°)": "green",
        "Medición de perímetros (5°)": "green",
        "Ángulos básicos (6°)": "green",
        "Cálculo de áreas simples (6°)": "green",
        "Polígonos y simetrías (7°)": "green",
        "Áreas y volúmenes (7°)": "green",
        "Geometría analítica básica (8°)": "green",
        "Teorema de Pitágoras (8°)": "green",

        "Introducción a variables y expresiones (5°)": "orange",
        "Ecuaciones simples (6°)": "orange",
        "Ecuaciones e inecuaciones (7°)": "orange",
        "Funciones lineales básicas (7°)": "orange",
        "Funciones lineales y cuadráticas (8°)": "orange",
        "Sistemas de ecuaciones (8°)": "orange",

        "Recolección de datos simples (5°)": "red",
        "Medidas de tendencia central (6°)": "red",
        "Representación gráfica (6°)": "red",
        "Probabilidad simple (7°)": "red",
        "Análisis de datos complejos (7°)": "red",
        "Probabilidad compuesta (8°)": "red",
        "Estadística descriptiva avanzada (8°)": "red"
    }

    for nodo, color in conceptos.items():
        G.add_node(nodo)

    edges = [
        ("Números naturales (5°)", "Fracciones básicas (5°)"),
        ("Fracciones básicas (5°)", "Operaciones con fracciones y decimales (6°)"),
        ("Operaciones básicas (5°)", "Operaciones con fracciones y decimales (6°)"),
        ("Operaciones con fracciones y decimales (6°)", "Potencias y raíces (7°)"),
        ("Potencias y raíces (7°)", "Números racionales y reales (8°)"),
        ("Números racionales y reales (8°)", "Operaciones algebraicas (8°)"),

        ("Figuras planas (5°)", "Ángulos básicos (6°)"),
        ("Medición de perímetros (5°)", "Cálculo de áreas simples (6°)"),
        ("Ángulos básicos (6°)", "Polígonos y simetrías (7°)"),
        ("Cálculo de áreas simples (6°)", "Áreas y volúmenes (7°)"),
        ("Polígonos y simetrías (7°)", "Geometría analítica básica (8°)"),
        ("Áreas y volúmenes (7°)", "Teorema de Pitágoras (8°)"),

        ("Introducción a variables y expresiones (5°)", "Ecuaciones simples (6°)"),
        ("Ecuaciones simples (6°)", "Ecuaciones e inecuaciones (7°)"),
        ("Ecuaciones e inecuaciones (7°)", "Funciones lineales básicas (7°)"),
        ("Funciones lineales básicas (7°)", "Funciones lineales y cuadráticas (8°)"),
        ("Funciones lineales y cuadráticas (8°)", "Sistemas de ecuaciones (8°)"),

        ("Recolección de datos simples (5°)", "Medidas de tendencia central (6°)"),
        ("Medidas de tendencia central (6°)", "Representación gráfica (6°)"),
        ("Representación gráfica (6°)", "Probabilidad simple (7°)"),
        ("Probabilidad simple (7°)", "Análisis de datos complejos (7°)"),
        ("Análisis de datos complejos (7°)", "Probabilidad compuesta (8°)"),
        ("Probabilidad compuesta (8°)", "Estadística descriptiva avanzada (8°)")
    ]

    G.add_edges_from(edges)

    if vacios:
        G.add_node("1° Medio", color="black")
        for v in vacios:
            concepto = v.split("→")[0].strip()
            G.add_edge(concepto, "1° Medio")

    pos = nx.spring_layout(G, k=0.8, iterations=50)
    plt.figure(figsize=(16, 12))

    color_map = [conceptos.get(node, "black") for node in G.nodes()]

    nx.draw_networkx_nodes(G, pos, node_color=color_map, node_size=1000, alpha=0.9)
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=9, font_family="sans-serif")

    plt.title("Mapa Conceptual de Matemáticas Chile (5° a 1° Medio)", fontsize=16)
    plt.axis('off')
    st.pyplot(plt)

def main():
    st.title("Diagnóstico de Vacíos en Matemáticas - 1° Medio")
    opcion = st.sidebar.selectbox("Seleccione una opción", ["Diagnóstico"])

    if opcion == "Diagnóstico":
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
                st.write([v.split("→")[0].strip() for v in vacios])
            else:
                st.write("No se detectaron vacíos académicos. ¡Bien hecho!")

            crear_mapa_conceptual(vacios)

if __name__ == "__main__":
    main()
