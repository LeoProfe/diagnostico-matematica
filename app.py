import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

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

    # Pregunta 1: Fracciones (usa opciones)
    fraccion = st.radio(
        "¿Cuál es el resultado de 3/4 + 2/3?",
        options=["17/12", "19/12", "5/6", "Otra"],
        key="q1"
    )
    respuestas.append(fraccion)

    # Pregunta 2: Ecuaciones simples
    eq = st.number_input("Resuelve: x - 3 = 7", step=1, format="%d", key="q2")
    respuestas.append(str(int(eq)))

    # Pregunta 3: Pendiente
    pendiente = st.number_input("¿Cuál es la pendiente de la recta y = 2x + 1?", step=1, format="%d", key="q3")
    respuestas.append(str(int(pendiente)))

    # Pregunta 4: Prioridad de operaciones
    operacion = st.number_input("Calcula: 2 * (5 - 3)^2", step=1, format="%d", key="q4")
    respuestas.append(str(int(operacion)))

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
