import streamlit as st

questions = [
    {"id": 1, "question": "¿Cuál es el resultado de 3/4 + 2/3?", "correct": "17/12", "oa": "OA6", "nivel": "5° Básico", "eje": "Número"},
    {"id": 2, "question": "Resuelve: x - 3 = 7", "correct": "10", "oa": "OA13", "nivel": "6° Básico", "eje": "Álgebra"},
    {"id": 3, "question": "¿Cuál es la pendiente de la recta y = 2x + 1?", "correct": "2", "oa": "OA15", "nivel": "8° Básico", "eje": "Álgebra"},
    {"id": 4, "question": "Calcula: 2 * (5 - 3)^2", "correct": "8", "oa": "OA8", "nivel": "6° Básico", "eje": "Número"},
    {"id": 5, "question": "Resuelve: 2x + 3 = 11", "correct": "4", "oa": "OA14", "nivel": "7° Básico", "eje": "Álgebra"},
    {"id": 6, "question": "¿Cuál es el área de un triángulo de base 6 y altura 4?", "correct": "12", "oa": "OA9", "nivel": "6° Básico", "eje": "Geometría"},
    {"id": 7, "question": "Convierte 0,75 a fracción", "correct": "3/4", "oa": "OA7", "nivel": "6° Básico", "eje": "Número"},
    {"id": 8, "question": "¿Cuál es la media de los números 5, 8, 10?", "correct": "7.67", "oa": "OA16", "nivel": "6° Básico", "eje": "Estadística"},
]

def diagnostico(respuestas):
    vacios = []
    for i, respuesta in enumerate(respuestas):
        if respuesta != questions[i]["correct"]:
            vacios.append(questions[i])
    return vacios

def agrupar_vacios(vacios):
    agrupado = {}
    for v in vacios:
        nivel = v["nivel"]
        eje = v["eje"]
        if nivel not in agrupado:
            agrupado[nivel] = {}
        if eje not in agrupado[nivel]:
            agrupado[nivel][eje] = []
        agrupado[nivel][eje].append(v)
    return agrupado

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

        st.subheader("Vacíos Detectados por Nivel y Eje")
        if vacios:
            agrupado = agrupar_vacios(vacios)
            for nivel in sorted(agrupado.keys()):
                st.markdown(f"### {nivel}")
                for eje in sorted(agrupado[nivel].keys()):
                    st.markdown(f"**{eje}**")
                    for v in agrupado[nivel][eje]:
                        st.markdown(f"- 🔴 {v['question']} — **OA:** {v['oa']} — Correcta: `{v['correct']}`")
        else:
            st.success("No se detectaron vacíos académicos. ¡Bien hecho!")

if __name__ == "__main__":
    main()
