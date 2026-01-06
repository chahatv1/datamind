import streamlit as st

from modules.story_generator import generate_story

st.header("✍️ AI-Generated Data Story")

# --------------------------------------------------
# Guards
# --------------------------------------------------
if st.session_state.quality_report is None:
    st.warning("⚠️ Quality analysis not found. Please complete earlier steps.")
    st.stop()

# --------------------------------------------------
# Context for story
# --------------------------------------------------
report = st.session_state.quality_report

df_desc = "Uploaded dataset"
if st.session_state.raw_df is not None:
    df_desc = f"Dataset with {st.session_state.raw_df.shape[0]:,} rows"

# --------------------------------------------------
# Generate story
# --------------------------------------------------
with st.spinner("Generating executive summary..."):
    story = generate_story(report, df_desc)
    st.session_state.story = story

st.success("✅ Story generated")

st.divider()

# --------------------------------------------------
# Display story
# --------------------------------------------------
st.subheader("📖 Executive Summary")
st.markdown(story)

# --------------------------------------------------
# Info / Next step
# --------------------------------------------------
st.info("➡️ Proceed to **Reports** to export results.")
