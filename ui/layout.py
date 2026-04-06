"""
DebateSphere AI - Layout Helpers
Page section wrappers for cleaner app.py.
"""

import streamlit as st
from ui.components import render_header, render_divider


def render_page_setup():
    """Configure Streamlit page and inject CSS."""
    st.set_page_config(
        page_title="DebateSphere AI",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_top_section():
    render_header()


def render_empty_state():
    st.markdown("""
    <div style="text-align:center; padding: 4rem 2rem; color: #475569;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">⚖️</div>
        <div style="font-size: 1.2rem; font-weight: 600; color: #64748b; margin-bottom: 0.5rem;">
            No debate running yet
        </div>
        <div style="font-size: 0.9rem; color: #475569;">
            Configure your debate in the sidebar and click <strong>Start Debate</strong> to begin.
        </div>
    </div>
    """, unsafe_allow_html=True)
