"""
Styling Module - Centralized CSS/theming for consistent Mountain Path branding
Purpose: Apply themes, colors, and custom styling to Streamlit app
"""

import streamlit as st
from config import COLORS, LINKEDIN_URL, GITHUB_URL

def apply_mountain_path_theme():
    """
    Apply Mountain Path branding theme to Streamlit app
    Uses custom CSS for enhanced visual control
    """
    custom_css = f"""
    <style>
        /* Global Font & Background */
        html, body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: {COLORS['text']};
            background-color: {COLORS['background']};
        }}
        
        /* Streamlit Main Content */
        .stApp {{
            background-color: {COLORS['background']};
        }}
        
        /* Header Styling */
        h1 {{
            color: {COLORS['primary']};
            font-weight: 700;
        }}
        
        h2, h3, h4, h5, h6 {{
            color: {COLORS['primary']};
            font-weight: 600;
        }}
        
        /* Metric Cards */
        .metric {{
            background-color: white;
            padding: 16px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* Data Table Styling */
        .dataframe {{
            border-collapse: collapse;
        }}
        
        /* Button Styling */
        .stButton > button {{
            background-color: {COLORS['primary']};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 24px;
            font-weight: 500;
            transition: all 0.3s;
        }}
        
        .stButton > button:hover {{
            background-color: {COLORS['secondary']};
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        /* Warning/Info Boxes */
        .stWarning {{
            background-color: #FFF3E0;
            border-left: 4px solid {COLORS['warning']};
            padding: 12px;
        }}
        
        .stInfo {{
            background-color: #E3F2FD;
            border-left: 4px solid {COLORS['primary']};
            padding: 12px;
        }}
        
        .stError {{
            background-color: #FFEBEE;
            border-left: 4px solid {COLORS['error']};
            padding: 12px;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {COLORS['background']};
        }}
        
        .stTabs [aria-selected="true"] {{
            border-bottom: 3px solid {COLORS['primary']};
            color: {COLORS['primary']};
        }}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {{
            .stApp {{
                padding: 0;
            }}
        }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def render_header():
    """
    Render Mountain Path branded header
    Returns: None (displays in Streamlit)
    """
    header_html = f"""
    <div style='
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        padding: 40px 30px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    '>
        <h1 style='
            color: {COLORS['accent']};
            margin: 0;
            font-size: 2.5em;
            font-weight: 700;
            letter-spacing: 1px;
        '>
            THE MOUNTAIN PATH - WORLD OF FINANCE
        </h1>
        <p style='
            color: white;
            margin: 12px 0 0 0;
            font-size: 1.2em;
            font-weight: 500;
        '>
            Top IT Companies Performance Analysis
        </p>
        <p style='
            color: {COLORS['accent']};
            margin: 8px 0 0 0;
            font-size: 0.95em;
        '>
            3-Year Rolling Window • Educational Purpose Only
        </p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_footer():
    """
    Render branded footer with contact & disclaimer
    Returns: None (displays in Streamlit)
    """
    footer_html = f"""
    <div style='
        background-color: {COLORS['primary']};
        color: {COLORS['accent']};
        padding: 30px;
        border-radius: 8px;
        margin-top: 50px;
        text-align: center;
        font-size: 0.9em;
    '>
        <p style='margin: 0 0 15px 0; font-weight: 700;'>
            © THE MOUNTAIN PATH - WORLD OF FINANCE
        </p>
        
        <p style='margin: 0 0 10px 0;'>
            <a href='{LINKEDIN_URL}' target='_blank' style='color: {COLORS['accent']}; text-decoration: none; margin-right: 20px;'>
                🔗 LinkedIn: trichyravis
            </a>
            <a href='{GITHUB_URL}' target='_blank' style='color: {COLORS['accent']}; text-decoration: none;'>
                🐙 GitHub: trichyravis
            </a>
        </p>
        
        <p style='margin: 10px 0 0 0; font-size: 0.85em; opacity: 0.9;'>
            <strong>Data Source:</strong> Yahoo Finance | <strong>Updated:</strong> Every 4 Hours  
        </p>
        
        <p style='margin: 5px 0 0 0; font-size: 0.85em; opacity: 0.85;'>
            <strong>Prof. V. Ravichandran</strong> • 28+ Years Finance & Banking • 10+ Years Academic
        </p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


def metric_card(label, value, unit="", delta=None, icon=""):
    """
    Render a styled metric card
    Args:
        label (str): Metric name
        value (float): Metric value
        unit (str): Unit suffix (%, $, etc.)
        delta (float): Change indicator
        icon (str): Emoji icon
    """
    delta_html = ""
    if delta is not None:
        delta_color = COLORS['success'] if delta >= 0 else COLORS['error']
        delta_arrow = "↑" if delta >= 0 else "↓"
        delta_html = f"<div style='color: {delta_color}; font-size: 0.9em;'>{delta_arrow} {abs(delta):.2f}%</div>"
    
    card_html = f"""
    <div style='
        background-color: white;
        border-left: 4px solid {COLORS['primary']};
        padding: 16px;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    '>
        <div style='
            color: {COLORS['text']};
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 8px;
        '>
            {icon} {label}
        </div>
        <div style='
            color: {COLORS['primary']};
            font-size: 1.8em;
            font-weight: 700;
        '>
            {value:.2f} {unit}
        </div>
        {delta_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def status_badge(status, text):
    """
    Render a status badge (✓ Good, ⚠️ Warning, ✗ Bad)
    Args:
        status (str): 'good', 'warning', or 'bad'
        text (str): Badge text
    """
    color_map = {
        'good': COLORS['success'],
        'warning': COLORS['warning'],
        'bad': COLORS['error']
    }
    symbol_map = {
        'good': '✓',
        'warning': '⚠️',
        'bad': '✗'
    }
    
    badge_html = f"""
    <span style='
        background-color: {color_map.get(status, COLORS['text'])};
        color: white;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85em;
        font-weight: 600;
    '>
        {symbol_map.get(status, '•')} {text}
    </span>
    """
    st.markdown(badge_html, unsafe_allow_html=True)
