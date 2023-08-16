import pandas as pd
import streamlit as st
from pandas import DataFrame

from constants import (
    COUNTRY_GROUPS,
    GROUP_1,
    GROUP_2,
    GROUP_3,
    GROUP_4,
    GROUP_5,
)


def update_model_and_show_output():
    pass


def build_model_inputs():
    heatmap_file = st.file_uploader("Upload Heatmap") or None
    groups = None
    st.session_state["input_dict"] = {}
    st.session_state["input_dict"]["eligible_employees"] = 0
    st.session_state["heatmap"] = None
    st.session_state["input_dict"]["group_1"] = 0
    st.session_state["input_dict"]["group_2"] = 0
    st.session_state["input_dict"]["group_3"] = 0
    st.session_state["input_dict"]["group_4"] = 0
    st.session_state["input_dict"]["group_5"] = 0
    if heatmap_file is not None:
        st.session_state["heatmap"] = pd.read_csv(heatmap_file)
        st.session_state["heatmap"]["Group"] = st.session_state["heatmap"][
            "Country"
        ].map(COUNTRY_GROUPS)
        st.session_state["input_dict"]["group_1"] = (
            st.session_state["heatmap"][st.session_state["heatmap"]["Group"] == 1][
                "EE count"
            ].sum()
            or 0
        )
        st.session_state["input_dict"]["group_2"] = (
            st.session_state["heatmap"][st.session_state["heatmap"]["Group"] == 2][
                "EE count"
            ].sum()
            or 0
        )
        st.session_state["input_dict"]["group_3"] = (
            st.session_state["heatmap"][st.session_state["heatmap"]["Group"] == 3][
                "EE count"
            ].sum()
            or 0
        )
        st.session_state["input_dict"]["group_4"] = (
            st.session_state["heatmap"][st.session_state["heatmap"]["Group"] == 4][
                "EE count"
            ].sum()
            or 0
        )
        st.session_state["input_dict"]["group_5"] = (
            st.session_state["heatmap"][st.session_state["heatmap"]["Group"] == 5][
                "EE count"
            ].sum()
            or 0
        )
        groups = pd.DataFrame.from_dict(
            {
                "Group 1": [st.session_state["input_dict"]["group_1"]],
                "Group 2": [st.session_state["input_dict"]["group_2"]],
                "Group 3": [st.session_state["input_dict"]["group_3"]],
                "Group 4": [st.session_state["input_dict"]["group_4"]],
                "Group 5": [st.session_state["input_dict"]["group_5"]],
            }
        ).T
        groups.columns = ["EE Count"]
    st.header("Model Inputs")
    with st.form("Model Inputs"):
        st.subheader("Pricing Model Basics")
        st.session_state["input_dict"]["model_type"] = st.selectbox(
            options=["PEPM", "UBP"], label="Model type?"
        )
        st.session_state["input_dict"]["include_dependents"] = st.selectbox(
            options=["Yes", "No"], label="Include Dependents?"
        )
        st.session_state["input_dict"]["disc."] = st.number_input(
            "disc. for PEPM model", value=0.0
        )
        st.session_state["input_dict"]["therapy_sessions"] = st.number_input(
            "# Therapy Sessions Paid by Company HR Budget", value=0
        )
        st.session_state["input_dict"]["coaching_sessions"] = st.number_input(
            "# Coaching Sessions Paid by Company HR Budget", value=0
        )
        st.session_state["input_dict"]["deskless_population"] = st.selectbox(
            options=[
                "0-10%",
                "10-25%",
                "25-50%",
                "50-75%",
                "75-100%",
            ],
            label="% Population that is Non-Desk (ok if you don't know, use 0-10% to start and adjust later)",
        )
        st.session_state["input_dict"]["year"] = st.selectbox(
            options=[
                "Year 1",
                "Year 2",
                "Year 3",
            ],
            label="Year 1 / 2 / 3 (~8% higher each following year; e.g. Year 1 = 10%, Year 2 = 10.8%)",
        )

        st.subheader("Add-on Services")
        st.session_state["input_dict"]["phone"] = st.selectbox(
            options=["Yes", "No"], label="Phone Services"
        )
        st.session_state["input_dict"]["crisis"] = st.selectbox(
            options=["Yes", "No"], label="Crisis Support Services"
        )
        st.session_state["input_dict"]["worklife"] = st.selectbox(
            options=["Yes", "No"], label="Work-Life Services"
        )
        st.session_state["input_dict"]["supervisory"] = st.selectbox(
            options=["Yes", "No"], label="Supervisory Services (no Mandatory Ref.)"
        )
        st.session_state["input_dict"]["mandatory_referral"] = st.selectbox(
            options=["Yes", "No"], label="Mandatory Referral"
        )
        st.session_state["input_dict"]["health_plan_integration"] = st.selectbox(
            options=["Yes", "No"], label="Health Plan Integration (HPI)"
        )
        st.session_state["input_dict"][
            "psychiatry_and_medication_management"
        ] = st.selectbox(
            options=["Yes", "No"], label="Psychiatry & Medication Management (PAMM)"
        )
        st.session_state["input_dict"][
            "counseling_sessions_covered_by_eap"
        ] = st.selectbox(
            options=[
                "Same as therapy sessions for MH covered countries",
                "2x the number of therapy sessions for MH covered countries",
            ],
            label="# of counseling sessions for EEs in countries covered by EAP",
        )
        st.session_state["input_dict"]["private_circles"] = st.number_input(
            "# Private Circles included for Free", value=0
        )

        st.subheader("EE count in each country?")
        if not isinstance(st.session_state["heatmap"], DataFrame):
            st.session_state["input_dict"]["group_1"] = st.number_input(
                label="# Eligible Employees in Group 1", help=GROUP_1, value=0
            )
            st.session_state["input_dict"]["group_2"] = st.number_input(
                label="# Eligible Employees in Group 2", help=GROUP_2, value=0
            )
            st.session_state["input_dict"]["group_3"] = st.number_input(
                label="# Eligible Employees in Group 3", help=GROUP_3, value=0
            )
            st.session_state["input_dict"]["group_4"] = st.number_input(
                label="# Eligible Employees in Group 4 (US in this group)",
                help=GROUP_4,
                value=0,
            )
            st.session_state["input_dict"]["group_5"] = st.number_input(
                label="# Eligible Employees in Group 5", help=GROUP_5, value=0
            )
        else:
            st.table(data=groups)
            st.session_state["input_dict"]["eligible_employees"] = st.number_input(
                "# Eligible Employees (exclude EEs in countries where EAP providing therapy like China or Russia)",
                value=st.session_state["heatmap"]["EE count"].sum(),
            )
        st.form_submit_button(
            "Submit Model Inputs", on_click=update_model_and_show_output
        )


def format_currency(x):
    try:
        return f"${float(x)}"
    except ValueError:
        return x


if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        initial_sidebar_state="collapsed",
        page_icon="🔮",
    )
    build_model_inputs()
