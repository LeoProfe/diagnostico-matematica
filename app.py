import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

questions = [
    {"id": 1, "question": "¿Cuál es el resultado de 3/4 + 2/3?", "correct": "17/12"},
    {"id": 2, "question": "Resuelve: x - 3 = 7", "correct": "10"},
    {"id": 3, "question": "¿Cuál es la pendiente de la recta y = 2x + 1?", "correct": "2"},
    {"id": 4, "question": "Calcula: 2 * (5 - 3)^2", "correct": "8"},
]

def diagnostico(respuestas):
    vacios = []
    if respuestas[0] != "17/12":
        vacios.append("Fracciones")
    if respuestas[1] != "10":
        vacios.append("Ecuaciones simples")
    if respuestas[2] != "2":
        vacios.append("Pendiente de una recta")
    if respuestas[3] != "8":
        vacios.append("Prioridad de operaciones")
    return vacios

def generar_mapa(vacios):
    G = nx.DiGraph()
    G.add_node("1° Medio")

    for v in vacios:
        G.add_node(v)
        G.add_edge(v, "1° Medio")

    fig, ax = plt.subplots()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, ax=ax)
    st.pyplot(fig)

def main():
    st.title("Diagnóstico de Vacíos en Matemáticas - 1° Medio")
    respuestas = []

    for q in questions:
        respuesta = st.text_input(q["question"], key=q["id"])
        respuestas.append(respuesta)

    if st.button("Evaluar"):
        vacios = diagnostico(respuestas)
        st.subheader("Vacíos Detectados:")
        if vacios:
            st.write(vacios)
            generar_mapa(vacios)
        else:
            st.write("No se detectaron vacíos académicos. ¡Bien hecho!")

if __name__ == "__main__":
    main()
