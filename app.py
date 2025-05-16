import streamlit as st
import math

# Inicialización del estado de sesión
if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}

if "pagina" not in st.session_state:
    st.session_state.pagina = 0

# ---------------------- PREGUNTAS ---------------------- #
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

PREGUNTAS_POR_PAGINA = 3
total_paginas = math.ceil(len(questions) / PREGUNTAS_POR_PAGINA)

# ---------------------- INTERFAZ ---------------------- #
st.title("Diagnóstico de Vacíos en Matemáticas")
st.markdown("Responde las siguientes preguntas. Puedes hacerlo en varias sesiones.")

pagina = st.session_state.pagina
inicio = pagina * PREGUNTAS_POR_PAGINA
fin = inicio + PREGUNTAS_POR_PAGINA
preguntas_actuales = questions[inicio:fin]

with st.form(f"pagina_{pagina}_form"):
    for q in preguntas_actuales:
        key = f"resp_{q['id']}"
        st.session_state.respuestas.setdefault(q["id"], "")
        respuesta = st.text_input(q["question"], key=key)
        st.session_state.respuestas[q["id"]] = respuesta.strip()
    col1, col2, col3 = st.columns(3)
    with col1:
        if pagina > 0:
            if st.form_submit_button("⬅️ Anterior"):
                st.session_state.pagina -= 1
                st.experimental_rerun()
    with col2:
        st.markdown(f"Página {pagina+1} de {total_paginas}")
    with col3:
        if pagina < total_paginas - 1:
            if st.form_submit_button("Siguiente ➡️"):
                st.session_state.pagina += 1
                st.experimental_rerun()
        else:
            if st.form_submit_button("Finalizar diagnóstico"):
                st.session_state["finalizado"] = True
                st.experimental_rerun()

# ---------------------- INFORME FINAL ---------------------- #
if st.session_state.get("finalizado"):
    st.subheader("📊 Informe de Vacíos Académicos")

    respondidas = {qid: resp for qid, resp in st.session_state.respuestas.items() if resp.strip() != ""}
    porcentaje = int(len(respondidas) / len(questions) * 100)
    st.markdown(f"Respondiste {len(respondidas)} de {len(questions)} preguntas. Esto representa un **{porcentaje}% del diagnóstico**.")

    vacios = []
    for q in questions:
        respuesta = st.session_state.respuestas.get(q["id"], "").strip()
        if respuesta != "" and respuesta != q["correct"]:
            vacios.append(q)

    if vacios:
        st.warning("Se detectaron vacíos en los siguientes contenidos:")
        vacios_por_nivel_eje = {}
        for v in vacios:
            nivel, eje = v["nivel"], v["eje"]
            vacios_por_nivel_eje.setdefault(nivel, {}).setdefault(eje, []).append(v)

        for nivel in sorted(vacios_por_nivel_eje):
            st.markdown(f"### {nivel}")
            for eje in sorted(vacios_por_nivel_eje[nivel]):
                st.markdown(f"**{eje}**")
                for v in vacios_por_nivel_eje[nivel][eje]:
                    st.markdown(f"- 🔴 {v['question']} — **OA:** {v['oa']} — Correcta: `{v['correct']}`")
    else:
        st.success("No se detectaron vacíos académicos en las preguntas que respondiste. ¡Bien hecho!")

    if st.button("🔄 Reiniciar diagnóstico"):
        for key in ["respuestas", "pagina", "finalizado"]:
            st.session_state.pop(key, None)
        st.experimental_rerun()
