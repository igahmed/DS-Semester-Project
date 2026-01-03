import streamlit as st

def load_soc_theme():
    st.markdown(
        """
        <style>
        /* ================= GLOBAL ================= */
        .stApp {
            background-color: #0b1220;
            color: #e5e7eb;
        }

        header {
            background-color: #020617 !important;
        }

        /* ================= SIDEBAR ================= */
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
        }

        [data-testid="stSidebar"] * {
            color: #cbd5e1 !important;
        }

        /* ================= CARDS ================= */
        .soc-card {
            background: linear-gradient(145deg, #0f172a, #020617);
            border: 1px solid #1e3a8a;
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 0 18px rgba(37, 99, 235, 0.15);
            margin-bottom: 16px;
        }

        /* ================= TABLE / AGGRID ================= */
        .ag-theme-dark {
            --ag-background-color: #020617;
            --ag-header-background-color: #020617;
            --ag-odd-row-background-color: #020617;
            --ag-foreground-color: #e5e7eb;
            --ag-header-foreground-color: #93c5fd;
            --ag-row-hover-color: #020617cc;
        }

        /* ================= SCROLLBAR ================= */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-thumb {
            background: #2563eb;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-track {
            background: #020617;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
