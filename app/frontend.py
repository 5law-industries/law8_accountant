"""
Frontend entry point for 8law Accountant Streamlit application.

This file serves as a compatibility wrapper for the old app/frontend.py entry point.
The actual application logic is in main.py at the project root.

DEPRECATED: Use main.py instead. This file is maintained for backward compatibility.
"""

import os
import sys
import warnings

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Show deprecation warning
warnings.warn(
    "Running 'streamlit run app/frontend.py' is deprecated. "
    "Please use 'streamlit run main.py' instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import Streamlit
import streamlit as st

# Import the auth module - now using correct import path
from app.auth_supabase import require_login

# Configure Streamlit page
st.set_page_config(
    page_title="8law Accountant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main application entry point."""
    
    # Show deprecation notice in the UI
    st.warning(
        "⚠️ **Deprecation Notice**: You're using the old entry point (`app/frontend.py`). "
        "Please update your command to `streamlit run main.py` for the latest features.",
        icon="⚠️"
    )
    
    # Require login before showing any content
    user = require_login()
    
    if user:
        # Main application UI
        st.title("📊 8law Accountant")
        st.write(f"Welcome, {user.get('email', 'User')}!")
        
        # Sidebar navigation
        with st.sidebar:
            st.header("Navigation")
            page = st.radio(
                "Select a page:",
                ["Dashboard", "Ledger", "Reports", "Admin"]
            )
        
        # Page routing
        if page == "Dashboard":
            st.header("Dashboard")
            st.info("Dashboard features coming soon...")
            
            # Display some sample metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Revenue", "$45,231", "+12%")
            with col2:
                st.metric("Total Expenses", "$23,456", "+5%")
            with col3:
                st.metric("Net Income", "$21,775", "+23%")
        
        elif page == "Ledger":
            st.header("Journal Ledger")
            st.info("Ledger features coming soon...")
            st.write("Create and manage journal entries with automatic validation.")
        
        elif page == "Reports":
            st.header("Financial Reports")
            st.info("Report features coming soon...")
            st.write("Generate financial statements and custom reports.")
        
        elif page == "Admin":
            st.header("Administration")
            st.info("Admin features coming soon...")
            st.write("Manage users, system settings, and view logs.")
        
        # Footer
        st.divider()
        st.caption("8law Accountant © 2026 | Secure, Multi-tenant Accounting Platform")


if __name__ == "__main__":
    main()
