import os
import streamlit as st
import pandas as pd
import numpy as np
import requests

from datetime import datetime

st.title("Investment Calculator")

# bonus: dict[int, float] | None = {},

API_URL = os.environ.get("API_URL")

meses = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]

# Dicionário onde os valores serão armazenados
valores_por_mes = {}

if "tipo_entrada" not in st.session_state:
    st.session_state["tipo_entrada"] = "Nenhum"

tipo = st.selectbox(
    "Escolha o tipo de cálculo", ["Por tempo", "Por meta"], key="tipo_entrada"
)


with st.form("my_form"):
    st.write("Preencha seus dados de investimento")

    mensal = st.number_input("Investimento mensal", step=100, min_value=100)
    juros = st.number_input(
        "Taxa de juros",
        step=1,
        value=15,
    )
    inicial = st.number_input("Valor inicial", min_value=0, step=100)

    begin = st.date_input("Inicio do cálculo")

    goal = None
    end = None

    if st.session_state.tipo_entrada == "Por meta":
        goal = st.number_input("Qual a sua meta?", min_value=0.0)
    elif st.session_state.tipo_entrada == "Por tempo":
        end = st.date_input("Fim do cálculo")

    # if metodo == "Por data":
    #     end = st.date_input("Fim do cálculo")
    # elif metodo == "Por objetivo final":
    #     goal = st.number_input("Qual a sua meta?", min_value=inicial)

    with st.expander("Ganha alguma renda extra em algum desses meses?"):
        for i, nome_mes in enumerate(meses, start=1):
            valor = st.number_input(
                f"{nome_mes}:", value=0.0, min_value=0.0, step=100.0
            )
            valores_por_mes[i] = valor

    kwargs = {
        "monthly_investment": mensal,
        "interest_rate": juros / 100,
        "begin": begin.isoformat(),
        "end": end.isoformat() if end else end,
        "goal": goal,
        "initial_value": inicial,
        "bonus": valores_por_mes,
    }

    disabled = st.session_state.tipo_entrada == "Nenhum"

    submitted = st.form_submit_button(
        "Submit", disabled=(st.session_state.tipo_entrada == "Nenhum")
    )

    if disabled:
        st.caption("ℹ️ Selecione uma opção para habilitar o botão.")

    if submitted:
        response = requests.post(f"{API_URL}/simulate", json=kwargs)

        if 400 <= response.status_code < 500:
            print("Erro 4xx (cliente)")
            st.error("This is an error", icon="🚨")
        elif 500 <= response.status_code < 600:
            print("Erro 5xx (servidor)")
            st.error("This is an error", icon="🚨")
        else:
            st.toast("Simulação enviada com sucesso!")

            final_dict = response.json()

            final_date = datetime.fromisoformat(final_dict["final_date"]).strftime(
                "%m-%Y"
            )
            goal = round(final_dict["goal"], 2)

            st.header(f"O objetivo será alcançado em {final_date}", divider="grey")
            st.header(f"Valor agregado até o final: {goal}", divider="grey")

            data = pd.DataFrame(
                list(final_dict["evolution"].items()), columns=["data", "valor"]
            )

            # Convertendo a coluna de data para datetime
            data["data"] = pd.to_datetime(data["data"])

            st.line_chart(data, x="data", y="valor")
