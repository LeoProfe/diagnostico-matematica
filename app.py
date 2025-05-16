import streamlit as st
import sympy as sp

# --- Datos ---
questions = [
    {"id": 1, "question": "¿Cuál es el resultado de 3/4 + 2/3?", "correct": "17/12", "oa": "OA6", "nivel": "5° Básico", "eje": "Números"},
    {"id": 2, "question": "Convierte 0,75 a fracción", "correct": "3/4", "oa": "OA7", "nivel": "6° Básico", "eje": "Números"},
    {"id": 3, "question": "Calcula: 2 * (5 - 3)^2", "correct": "8", "oa": "OA8", "nivel": "6° Básico", "eje": "Álgebra"},
    # ... más preguntas como en el prototipo original ...
]

# --- Funciones ---
def comparar_respuestas(respuesta_usuario, respuesta_correcta):
    try:
        return sp.simplify(sp.sympify(respuesta_usuario)) == sp.simplify(sp.sympify(respuesta_correcta))
    except Exception:
        return False

def diagnostico(respuestas):
    vacios = []
    for i, respuesta in enumerate(respuestas):
        if not comparar_respuestas(respuesta.strip(), questions[i]["correct"]):
            vacios.append(questions[i])
    return vacios

# --- Interfaz Principal ---
def main():
    st.set_page_config(page_title="Diagnóstico Matemático", layout="centered")
    st.title("🧠 Diagnóstico de Vacíos Académicos en Matemáticas")
    st.markdown("Responde con precisión para detectar brechas de aprendizaje desde **5° Básico hasta 1° Medio**.")

    respuestas = []
    for q in questions:
        with st.expander(f"🔹 {q['nivel']} - {q['eje']} | {q['question']}"):
            respuesta = st.text_input("Tu respuesta:", key=q["id"])
            respuestas.append(respuesta)

    if st.button("📊 Evaluar Respuestas"):
        vacios = diagnostico(respuestas)

        st.subheader("✅ Resumen de Resultados")
        for i, r in enumerate(respuestas):
            correcto = questions[i]["correct"]
            if comparar_respuestas(r.strip(), correcto):
                st.success(f"✔️ {questions[i]['question']} — Tu respuesta: `{r}`")
            else:
                st.error(f"❌ {questions[i]['question']} — Tu respuesta: `{r}` | Correcta: `{correcto}`")

        st.subheader("📌 Vacíos Detectados por Nivel y Eje:")
        if vacios:
            agrupados = {}
            for v in vacios:
                nivel, eje = v["nivel"], v["eje"]
                agrupados.setdefault(nivel, {}).setdefault(eje, []).append(v)

            for nivel in sorted(agrupados):
                st.markdown(f"### {nivel}")
                for eje in sorted(agrupados[nivel]):
                    st.markdown(f"**{eje}**")
                    for v in agrupados[nivel][eje]:
                        st.markdown(f"- 🔴 {v['question']} — **OA:** {v['oa']} — Correcta: `{v['correct']}`")
        else:
            st.balloons()
            st.success("¡Felicidades! No se detectaron vacíos académicos.")

if __name__ == "__main__":
    main()
