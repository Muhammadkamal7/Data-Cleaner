import streamlit as st
import pandas as pd

# 1. Page Configuration & UI Title
st.set_page_config(page_title="Global Data Sanitizer", page_icon="📊", layout="wide")
st.title("📊 Global CSV or Excel Data Sanitizer & Formatter")
st.write("Upload any messy CSV or excel file to instantly clean duplicates, fix formatting, and sanitize strings.")

# 2. File Uploading (Accepts global CSV formats)
uploaded_file = st.file_uploader("Choose a CSV or Excel file to process", type=["csv","xlsx","xls"])

if uploaded_file is not None:
    # Read the data into a DataFrame (handle CSV and Excel uploads)
    try:
        filename = uploaded_file.name
        if filename.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")
        st.stop()
    
    st.subheader("👀 Original Data Preview (First 5 Rows)")
    st.dataframe(df.head())
    
    # 3. Interactive Data Window Processing Controls
    st.sidebar.header("🛠️ Cleaning Operations")
    remove_dup = st.sidebar.checkbox("Remove Duplicate Rows")
    remove_null = st.sidebar.checkbox("Drop Rows with Missing Values")
    uppercase_cols = st.sidebar.multiselect("Convert Text Columns to UPPERCASE", df.select_dtypes(include=['object']).columns)

    # 4. Execute the Logic (The equivalent of clicking a PB 'Retrieve/Update' button)
    cleaned_df = df.copy()
    
    if remove_dup:
        cleaned_df = cleaned_df.drop_duplicates()
    if remove_null:
        cleaned_df = cleaned_df.dropna()
    if uppercase_cols:
        for col in uppercase_cols:
            cleaned_df[col] = cleaned_df[col].astype(str).str.upper()

    # 5. Display Cleaned Results
    st.subheader("✨ Cleaned Data Preview")
    st.dataframe(cleaned_df.head())

    # 6. Freemium Paywall Integration (100% Free Setup)
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("💡 Free Tier Limit: Download up to 50 cleaned rows.")
        # Free Download Button (Truncated DataWindow)
        free_csv = cleaned_df.head(50).to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Free Sample (50 Rows)",
            data=free_csv,
            file_name="sanitized_sample.csv",
            mime="text/csv"
        )

    with col2:
        st.success("🚀 Premium Tier: Process unlimited rows + Automated Excel formatting.")
        # Place your Lemon Squeezy or Paddle checkout link directly onto the button
        premium_checkout_url = "https://kamaldigital.lemonsqueezy.com/checkout/buy/48a438a4-7891-4393-895b-74384a9ea100"
        st.link_button("🔓 Unlock Unlimited Premium Processing ($5)", premium_checkout_url)
