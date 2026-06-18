import streamlit as st
import pandas as pd
import requests
import io

# 1. Page Configuration & UI Title
st.set_page_config(page_title="Global Data Sanitizer", page_icon="📊", layout="wide")
st.title("📊 Global CSV or Excel Data Sanitizer & Formatter")
st.write("Upload any messy CSV or excel file to instantly clean duplicates, fix formatting, and sanitize strings.")

# 2. License Key Access Portal (The Gatekeeper)
st.sidebar.header("🔑 Premium Access Verification")
user_license_key = st.sidebar.text_input("Enter your Lemon Squeezy License Key", type="password")

# Shared state variable to track validation status
is_premium_active = False

if user_license_key:
    # Set up the secure API call directly to Lemon Squeezy servers
    api_url = "https://lemonsqueezy.com"
    payload = {"license_key": user_license_key}
    headers = {"Accept": "application/vnd.api+json", "Content-Type": "application/vnd.api+json"}

    try:
        # Send the key via an internet POST request
        response = requests.post(api_url, json=payload, headers=headers)
        response_data = response.json()
        
        # Check if Lemon Squeezy returns valid status
        if response.status_code == 200 and response_data.get("valid") == True:
            st.sidebar.success("✅ Premium Access Granted!")
            is_premium_active = True
        else:
            st.sidebar.error("❌ Invalid License Key. Please check your credentials.")
    except Exception as e:
        st.sidebar.warning("⚡ Verification server busy. Please try again.")


# 3. File Uploading (Accepts global CSV formats)
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
    
    # 4. Enforce Access Rules Based on the License Key
    st.divider()

    # # 4. Interactive Data Window Processing Controls
    # st.sidebar.header("🛠️ Cleaning Operations")
    # remove_dup = st.sidebar.checkbox("Remove Duplicate Rows")
    # remove_null = st.sidebar.checkbox("Drop Rows with Missing Values")
    # uppercase_cols = st.sidebar.multiselect("Convert Text Columns to UPPERCASE", df.select_dtypes(include=['object']).columns)

    # # 4. Execute the Logic (The equivalent of clicking a PB 'Retrieve/Update' button)
    # cleaned_df = df.copy()
    
    # if remove_dup:
    #     cleaned_df = cleaned_df.drop_duplicates()
    # if remove_null:
    #     cleaned_df = cleaned_df.dropna()
    # if uppercase_cols:
    #     for col in uppercase_cols:
    #         cleaned_df[col] = cleaned_df[col].astype(str).str.upper()

    # # 5. Display Cleaned Results
    # st.subheader("✨ Cleaned Data Preview")
    # st.dataframe(cleaned_df.head())

    # # 6. Freemium Paywall Integration (100% Free Setup)
    # st.divider()
    # col1, col2 = st.columns(2)
    
    # with col1:
    #     st.info("💡 Free Tier Limit: Download up to 50 cleaned rows.")
    #     # Free Download Button (Truncated DataWindow)
    #     free_csv = cleaned_df.head(50).to_csv(index=False).encode('utf-8')
    #     st.download_button(
    #         label="⬇️ Download Free Sample (50 Rows)",
    #         data=free_csv,
    #         file_name="sanitized_sample.csv",
    #         mime="text/csv"
    #     )

    # with col2:
    #     st.success("🚀 Premium Tier: Process unlimited rows + Automated Excel formatting.")
    #     # Place your Lemon Squeezy or Paddle checkout link directly onto the button
    #     premium_checkout_url = "https://kamaldigital.lemonsqueezy.com/checkout/buy/48a438a4-7891-4393-895b-74384a9ea100"
    #     st.link_button("🔓 Unlock Unlimited Premium Processing ($5)", premium_checkout_url)

    if is_premium_active:
        # --- PREMIUM TIER ACTIVATED ---
        st.markdown("### ✨ Premium Controls Active")
        
        # Advanced DataWindow-style cleanup tools
        remove_dup = st.checkbox("Remove All Duplicate Rows")
        remove_null = st.checkbox("Drop Rows with Empty Columns")
        
        cleaned_df = df.copy()
        if remove_dup:
            cleaned_df = cleaned_df.drop_duplicates()
        if remove_null:
            cleaned_df = cleaned_df.dropna()
            
        st.subheader("📈 Fully Cleaned Dataset")
        st.dataframe(cleaned_df)
        
        #if the selected file is an excel file, we can also offer the option to download it as an excel file with the same name but with _cleaned appended to it
        if filename.lower().endswith((".xlsx", ".xls")):
            excel_buffer = pd.ExcelWriter(f"{filename.rsplit('.', 1)[0]}_cleaned.xlsx", engine='openpyxl')
            cleaned_df.to_excel(excel_buffer, index=False)
            excel_buffer.save()
            excel_data = excel_buffer.getvalue()
            st.download_button(
                label="⬇️ Download Cleaned Dataset as Excel",
                data=excel_data,
                file_name=f"{filename.rsplit('.', 1)[0]}_cleaned.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            # Unlimited Download Option
            full_csv = cleaned_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download Complete Cleaned Dataset (Unlimited)",
                data=full_csv,
                file_name="sanitized_premium_export.csv",
                mime="text/csv"
            )
    else:
        # --- FREE TIER LIMITATION ---
        st.markdown("### 🔒 Free Tier Active")
        st.info("Showing up to 5 rows maximum. Upgrade to unlock full configurations and downloads.")
        
        # Truncate dataset entirely to protect your tool's operations
        if filename.lower().endswith((".xlsx", ".xls")):
            excel_buffer = io.BytesIO()
            # Write to Excel using context manager
            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                df.head(5).to_excel(writer, index=False)
            
            # Get the binary data
            excel_data = excel_buffer.getvalue()
            
            st.download_button(
                label="⬇️ Download Free Sample (Limited to 5 Rows)",
                data=excel_data,
                file_name=f"{filename.rsplit('.', 1)[0]}_free_sample.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            free_csv = df.head(5).to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Free Sample (Limited to 5 Rows)",
                data=free_csv,
                file_name="sanitized_free_sample.csv",
                mime="text/csv"
            )
                
        # Paywall link directing back to checkout
        st.warning("Want to unlock advanced operations and unlimited exports?")
        premium_checkout_url = "https://kamaldigital.lemonsqueezy.com/checkout/buy/48a438a4-7891-4393-895b-74384a9ea100"
        st.link_button("🔓 Buy License Key Now ($9)", premium_checkout_url)
