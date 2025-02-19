import streamlit as st
import pandas as pd
import os
import time
from io import BytesIO

# ✅ Ensure set_page_config is the FIRST Streamlit command
st.set_page_config(
    page_title="💿 DATA REFINERY",
    layout="wide",
    page_icon="💿",
)

# 🎨 Custom CSS for Styling
st.markdown(
    """
    <style>
        /* Background and text color */
        .stApp {
            background-color: #121212;
            color: white;
        }

        /* Title styling */
        h1 {
            color: #f1c40f;
            text-align: center;
        }

        /* File uploader */
        .stFileUploader {
            border: 2px dashed #1abc9c !important;
            background-color: #1e1e1e;
            padding: 15px;
            border-radius: 10px;
        }

        /* Custom buttons */
        .stButton>button {
            background-color: #3498db;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #2980b9;
        }

        /* Card Styling */
        .card {
            background-color: #1e1e1e;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px #000000;
            margin-bottom: 20px;
        }

        /* Footer */
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 10px;
            background-color: #0e0e0e;
            color: white;
            font-size: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🌟 Animated Header
st.markdown("<h1>💿 DATA REFINERY</h1>", unsafe_allow_html=True)
st.write("**Transform your files between CSV and Excel formats with built-in data cleaning and visualization!**")

# 📂 File Uploader
st.markdown('<div class="card">', unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "**Upload your files (CSV or Excel):**",
    type=["csv", "xlsx"],
    accept_multiple_files=True,
)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # 🕒 Progress Indicator
        with st.spinner(f"Processing {file.name}..."):
            time.sleep(1)

        # 📌 Read File Based on Extension
        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"⚠️ Error reading file: {e}")
            continue

        # 📋 Display File Information
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"**📄 File Name:** {file.name}")
        st.write(f"**📦 File Size:** {round(file.size / 1024, 2)} KB")
        st.markdown("</div>", unsafe_allow_html=True)

        # 🔍 Data Preview
        st.subheader("🔍 Preview the First 5 Rows")
        st.dataframe(df.head())

        # 🛠️ Data Cleaning Section
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🧹 Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")

            with col2:
                if st.button(f"📊 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if not numeric_cols.empty:
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("✅ Missing Values Filled!")
                    else:
                        st.warning("⚠️ No numeric columns available for filling missing values.")

        # 🔄 Column Selection
        st.subheader("🔄 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # 📊 Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            numeric_data = df.select_dtypes(include="number")
            if not numeric_data.empty:
                st.bar_chart(numeric_data.iloc[:, :2])
            else:
                st.warning("⚠️ No numeric columns available for visualization.")

        # 📂 File Conversion
        st.subheader("🛠️ Conversion Options")
        conversion_types = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"🔄 Convert {file.name}"):
            buffer = BytesIO()
            if conversion_types == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_types == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # ⬇️ Download Button
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_types}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
            )

# 🎉 Success Message
st.success("✅ All files processed successfully!")

# 📌 Footer
st.markdown('<div class="footer">💾 DATA REFINERY | Developed with Love❤️ by Umaima</div>', unsafe_allow_html=True)
