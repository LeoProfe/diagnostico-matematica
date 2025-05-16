import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

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
    vacios = []
    for i, respuesta in enumerate(respuestas):
        if respuesta != questions[i]["correct"]:
            vacios.append((questions[i]["question"], questions[i]["correct"], questions[i]["oa"]))
    return vacios

def crear_mapa_conceptual(vacios=[]):
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

    # Crear todos los nodos con atributos
    node_labels = {}
    for oa, nombre, nivel in conceptos:
        label = f"{oa}: {nombre}\n({nivel})"
        color = "red" if any(v[2] == oa for v in vacios) else "skyblue"
        G.add_node(label, level=niveles[nivel], color=color)
        node_labels[oa] = label

    # Agregar aristas
    for origen, destino in edges:
        if origen in node_labels and destino in node_labels:
            G.add_edge(node_labels[origen], node_labels[destino])

    # Filtrar nodos: solo los que están en vacios + sus ancestros (para mostrar la rama completa)
    nodos_interes = set()
    for v in vacios:
        oa_vacio = v[2]
        if oa_vacio in node_labels:
            nodo = node_labels[oa_vacio]
            nodos_interes.add(nodo)
            # Subir por el grafo para añadir ancestros
            padres = list(G.predecessors(nodo))
            while padres:
                nodos_interes.update(padres)
                nuevos = []
                for p in padres:
                    nuevos.extend(G.predecessors(p))
                padres = nuevos

    if not nodos_interes:
        nodos_interes = G.nodes()  # Si no hay vacíos, mostrar todo

    G_sub = G.subgraph(nodos_interes).copy()

    # Corregir atributo "level" faltante en subgrafo
    for n in G_sub.nodes():
        if "level" not in G_sub.nodes[n]:
            G_sub.nodes[n]["level"] = 0

    pos = nx.multipartite_layout(G_sub, subset_key="level")

    plt.figure(figsize=(14, 10))
    node_colors = [G_sub.nodes[n]["color"] for n in G_sub.nodes()]
    nx.draw(G_sub, pos, with_labels=True, node_color=node_colors, node_size=2500, font_size=9, font_weight="bold")
    plt.title("Mapa Conceptual Progresivo (5° Básico a 1° Medio)")
    plt.axis('off')
    st.pyplot(plt)

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
                st.markdown(f"🔴 {v[0]} — **OA:** {v[2]} — Correcta: `{v[1]}`")
        else:
            st.success("No se detectaron vacíos académicos. ¡Bien hecho!")

        crear_mapa_conceptual(vacios)

if __name__ == "__main__":
    main()
