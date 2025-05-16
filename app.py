import streamlit as st

# Lista completa de preguntas
questions = [
    {"id": 1, "question": "¿Cuál es el resultado de 3/4 + 2/3?", "correct": "17/12", "oa": "OA6", "nivel": "5° Básico", "eje": "Números"},
    {"id": 2, "question": "Convierte 0,75 a fracción", "correct": "3/4", "oa": "OA7", "nivel": "6° Básico", "eje": "Números"},
    {"id": 3, "question": "Calcula: 2 * (5 - 3)^2", "correct": "8", "oa": "OA8", "nivel": "6° Básico", "eje": "Álgebra"},
    {"id": 4, "question": "¿Cuál es el área de un triángulo de base 6 y altura 4?", "correct": "12", "oa": "OA9", "nivel": "6° Básico", "eje": "Geometría"},
    {"id": 5, "question": "Resuelve: x - 3 = 7", "correct": "10", "oa": "OA13", "nivel": "6° Básico", "eje": "Álgebra"},
    {"id": 6, "question": "Resuelve: 2x + 3 = 11", "correct": "4", "oa": "OA14", "nivel": "7° Básico", "eje": "Álgebra"},
    {"id": 7, "question": "¿Cuál es la pendiente de la recta y = 2x + 1?", "correct": "2", "oa": "OA15", "nivel": "8° Básico", "eje": "Álgebra"},
    {"id": 8, "question": "¿Cuál es la media de los números 5, 8, 10?", "correct": "7.67", "oa": "OA16", "nivel": "6° Básico", "eje": "Estadística"},
    {"id": 9, "question": "¿Cuál es el resultado de 5 - 7?", "correct": "-2", "oa": "OA17", "nivel": "5° Básico", "eje": "Números"},
    {"id": 10, "question": "Convierte 3/5 a decimal", "correct": "0.6", "oa": "OA18", "nivel": "6° Básico", "eje": "Números"},
    {"id": 11, "question": "Resuelve: 3(x - 2) = 9", "correct": "5", "oa": "OA19", "nivel": "7° Básico", "eje": "Álgebra"},
    {"id": 12, "question": "Calcula el perímetro de un cuadrado de lado 4", "correct": "16", "oa": "OA20", "nivel": "6° Básico", "eje": "Geometría"},
    {"id": 13, "question": "¿Cuál es la mediana de los números 3, 7, 7, 9, 10?", "correct": "7", "oa": "OA21", "nivel": "6° Básico", "eje": "Estadística"},
    {"id": 14, "question": "Redondea 7.678 a dos decimales", "correct": "7.68", "oa": "OA22", "nivel": "6° Básico", "eje": "Números"},
    {"id": 15, "question": "Resuelve: x/2 = 5", "correct": "10", "oa": "OA23", "nivel": "7° Básico", "eje": "Álgebra"},
    {"id": 16, "question": "¿Cuál es el área de un círculo de radio 3? (Use π=3.14)", "correct": "28.26", "oa": "OA24", "nivel": "8° Básico", "eje": "Geometría"},
    {"id": 17, "question": "Calcula la desviación de los números 2, 4, 4, 4, 5, 5, 7, 9", "correct": "2", "oa": "OA25", "nivel": "8° Básico", "eje": "Estadística"},
    {"id": 18, "question": "Convierte 1500 gramos a kilogramos", "correct": "1.5", "oa": "OA26", "nivel": "5° Básico", "eje": "Números"},
    {"id": 19, "question": "Calcula 3^3", "correct": "27", "oa": "OA27", "nivel": "7° Básico", "eje": "Álgebra"},
    {"id": 20, "question": "Calcula el volumen de un cubo de lado 2", "correct": "8", "oa": "OA28", "nivel": "8° Básico", "eje": "Geometría"},
]

# Número de preguntas por página
QUESTIONS_PER_PAGE = 3

# Diagnóstico: compara respuestas del usuario con las correctas
def diagnostico(respuestas_parciales):
    vacios = []
    for q_id, respuesta in respuestas_parciales.items():
        question = next(q for q in questions if q["id"] == q_id)
        if respuesta.strip() != question["correct"]:
            vacios.append(question)
    return vacios

# App principal
def main():
    st.title("🧠 Diagnóstico de Vacíos en Matemáticas - 1° Medio")

    # Variables de sesión
    if "page" not in st.session_state:
        st.session_state.page = 0
    if "respuestas" not in st.session_state:
        st.session_state.respuestas = {}

    # Paginación
    start_index = st.session_state.page * QUESTIONS_PER_PAGE
    end_index = start_index + QUESTIONS_PER_PAGE
    current_questions = questions[start_index:end_index]

    st.markdown("Responde las siguientes preguntas. Puedes avanzar o terminar cuando quieras para ver tus resultados hasta ese punto.")

    # Preguntas
    for q in current_questions:
        respuesta = st.text_input(q["question"], key=q["id"])
        st.session_state.respuestas[q["id"]] = respuesta

    # Navegación
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.page > 0:
            if st.button("⬅️ Anterior"):
                st.session_state.page -= 1
                st.experimental_rerun()
    with col2:
        if end_index < len(questions):
            if st.button("➡️ Siguiente"):
                st.session_state.page += 1
                st.experimental_rerun()
    with col3:
        if st.button("📊 Finalizar Diagnóstico"):
            total_respondidas = len(st.session_state.respuestas)
            porcentaje = round((total_respondidas / len(questions)) * 100)

            st.subheader("✅ Diagnóstico Completado")
            st.markdown(f"Has respondido el **{porcentaje}%** del diagnóstico.")

            vacios = diagnostico(st.session_state.respuestas)

            st.subheader("📉 Resultados y Vacíos Detectados:")
            for q in questions:
                user_resp = st.session_state.respuestas.get(q["id"], "")
                correcto = q["correct"]
                if user_resp.strip() == correcto:
                    st.markdown(f"✅ **{q['question']}** — Tu respuesta: `{user_resp}`")
                else:
                    st.markdown(f"❌ **{q['question']}** — Tu respuesta: `{user_resp}` | Correcta: `{correcto}`")

            if vacios:
                st.markdown("---")
                st.subheader("🔍 Vacíos por Nivel y Eje:")
                agrupados = {}
                for v in vacios:
                    nivel = v["nivel"]
                    eje = v["eje"]
                    if nivel not in agrupados:
                        agrupados[nivel] = {}
                    if eje not in agrupados[nivel]:
                        agrupados[nivel][eje] = []
                    agrupados[nivel][eje].append(v)

                for nivel in sorted(agrupados.keys()):
                    st.markdown(f"### {nivel}")
                    for eje in sorted(agrupados[nivel].keys()):
                        st.markdown(f"**{eje}**")
                        for v in agrupados[nivel][eje]:
                            st.markdown(f"- 🔴 {v['question']} — OA: {v['oa']} — Correcta: `{v['correct']}`")
            else:
                st.success("¡No se detectaron vacíos académicos! Excelente trabajo.")

if __name__ == "__main__":
    main()
