"""
Footer Component for The Mountain Path - World of Finance
"""

import streamlit as st
from datetime import datetime


def render_footer():
    """Render the professional footer with contact links and disclaimer"""
    
    st.markdown("---")
    st.markdown(f"""
        <div style="text-align: center; color: #666; padding: 2rem;">
            <p><strong>THE MOUNTAIN PATH - WORLD OF FINANCE</strong></p>
            <p>Top US Tech Companies 3 Year Performance Analysis</p>
            <p>Prof. V. Ravichandran | 28+ Years Finance Experience</p>
            <p style="margin-top: 1rem;">
                <a href="https://www.linkedin.com/in/trichyravis" target="_blank" 
                   style="display: inline-block; padding: 0.5rem 1.5rem; 
                          background: linear-gradient(135deg, #0077b5 0%, #0a66c2 100%); 
                          color: white; text-decoration: none; border-radius: 5px; 
                          font-weight: 600; margin: 0 0.5rem;">
                   🔗 LinkedIn Profile
                </a>
                <a href="https://github.com/trichyravis" target="_blank" 
                   style="display: inline-block; padding: 0.5rem 1.5rem; 
                          background: linear-gradient(135deg, #333 0%, #555 100%); 
                          color: white; text-decoration: none; border-radius: 5px; 
                          font-weight: 600; margin: 0 0.5rem;">
                   🐙 GitHub
                </a>
            </p>
            <p style="font-size: 0.8rem; margin-top: 1rem;">
                Disclaimer: This tool is for educational purposes. Not financial advice. 
                Always consult with a qualified financial advisor before making investment decisions.
            </p>
            <div class="time-display">
                📊 Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </div>
        </div>
    """, unsafe_allow_html=True)
