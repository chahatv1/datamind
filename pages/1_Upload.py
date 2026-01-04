import streamlit as st
import pandas as pd

st.header("📤 Upload Dataset")
st.write("Upload a CSV file to begin the DataMind analysis pipeline.")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Store raw data in session state
        st.session_state.raw_df = df

        st.success("✅ File uploaded successfully")

        # Basic dataset info
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())

        st.subheader("🔍 Data Preview")
        st.dataframe(df.head(50), use_container_width=True)

        st.info(
            "➡️ Proceed to **Quality Analysis** using the sidebar to continue."
        )

    except Exception as e:
        st.error("❌ Failed to read the CSV file.")
        st.code(str(e))
else:
    st.warning("Please upload a CSV file to continue.")
