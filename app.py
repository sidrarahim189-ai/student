import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------
# 1. ڕێکخستنی پەڕە (Page Configuration)
# -------------------------------------
st.set_page_config(
    page_title="داشبۆردی ئاستی خوێندکارانی AI",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------------
# 1.5 ستایلی ئاراستەی ڕاست بۆ چەپ (RTL CSS)
# -------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stAlert, .stCaption {
        text-align: right !important;
        direction: rtl !important;
    }
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
        text-align: right !important;
        direction: rtl !important;
    }
    input {
        direction: rtl !important;
        text-align: right !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------
# 2. ناونیشانی بەرنامەکە
# -------------------------------------
st.title("🎓 داشبۆردی هەڵسەنگاندنی ئاستی خوێندکارانی زیرەکی دەستکرد (AI)")
st.write("شیکردنەوەی ئاستی خوێندکاران لەسەر بنەمای کڵاود (Cloud)")

# -------------------------------------
# 3. بارکردنی داتا (Load Dataset)
# -------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("students.csv")

df = load_data()

# -------------------------------------
# 4. بارکردنی فایلی نوێی CSV
# -------------------------------------
uploaded_file = st.file_uploader(
    "فایلی CSVـی خوێندکاران باربکە",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

# -------------------------------------
# 5. هەژمارکردنی کۆی گشتی و تێکڕا
# -------------------------------------
subjects = [
    "AI",
    "Programming",
    "Statistics",
    "DataScience"
]

df["کۆی گشتی"] = df[subjects].sum(axis=1)
df["تێکڕا"] = df[subjects].mean(axis=1).round(2)

# -------------------------------------
# 6. دیاریکردنی ئاستی خوێندکار
# -------------------------------------
def performance_level(score):
    if score >= 85:
        return "نایاب"
    elif score >= 70:
        return "زۆر باش"
    elif score >= 50:
        return "دەرچوو"
    else:
        return "پێویستی بە هاوکارییە"

df["ئاست"] = df["تێکڕا"].apply(performance_level)

# -------------------------------------
# 7. کارتەکانی ئامار (KPI Cards)
# -------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "کۆی خوێندکاران",
    len(df)
)

col2.metric(
    "تێکڕای گشتی پۆل",
    round(df["تێکڕا"].mean(), 2)
)

col3.metric(
    "بەرزترین تێکڕا",
    round(df["تێکڕا"].max(), 2)
)

col4.metric(
    "پێویستیان بە هاوکارییە",
    int((df["ئاست"] == "پێویستی بە هاوکارییە").sum())
)

col5.metric(
    "هیوا عومەر حەسەن",
    len(df)
)

st.divider()

# -------------------------------------
# 8. گەڕان بەدوای خوێندکاردا
# -------------------------------------
st.subheader("🔍 گەڕان بەدوای خوێندکاردا")

search = st.text_input(
    "ناو یان کۆدی خوێندکار (ID) بنووسە"
)

# گۆڕینی ناوی ستوونەکان بۆ کوردی لە کاتی پیشاندانی خشتەکەدا
display_df = df.rename(columns={
    "Student_ID": "کۆدی خوێندکار",
    "Name": "ناو",
    "AI": "زیرەکی دەستکرد",
    "Programming": "پڕۆگرامسازی",
    "Statistics": "ئامار",
    "DataScience": "زانستی داتا"
})

if search:
    filtered_df = display_df[
        display_df["ناو"].astype(str).str.contains(
            search, case=False, na=False
        ) |
        display_df["کۆدی خوێندکار"].astype(str).str.contains(
            search, case=False, na=False
        )
    ]
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.dataframe(display_df, use_container_width=True)

# -------------------------------------
# 9. هێڵکاری تێکڕای نمرەی خوێندکاران
# -------------------------------------
st.subheader("📊 تێکڕای نمرەی خوێندکاران")

fig1 = px.bar(
    display_df,
    x="ناو",
    y="تێکڕا",
    color="ئاست",
    title="تێکڕای نمرە بەپێی خوێندکار",
    text="تێکڕا",
    labels={
        "ناو": "ناوی خوێندکار",
        "تێکڕا": "تێکڕای نمرە",
        "ئاست": "ئاستی خوێندکار"
    }
)

fig1.update_layout(yaxis_range=[0, 100])
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------------
# 10. بەراوردکردنی وانەکان
# -------------------------------------
st.subheader("📚 ئاستی وانەکان")

subject_names_ku = {
    "AI": "زیرەکی دەستکرد",
    "Programming": "پڕۆگرامسازی",
    "Statistics": "ئامار",
    "DataScience": "زانستی داتا"
}

subject_avg = df[subjects].mean().reset_index()
subject_avg.columns = ["وانە", "تێکڕای نمرە"]
subject_avg["وانە"] = subject_avg["وانە"].map(subject_names_ku)

fig2 = px.bar(
    subject_avg,
    x="وانە",
    y="تێکڕای نمرە",
    color="وانە",
    title="تێکڕای نمرەکان بەپێی وانە"
)

fig2.update_layout(yaxis_range=[0, 100])
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------
# 11. دابەشبوونی ئاستی خوێندکاران
# -------------------------------------
st.subheader("🎯 ئاستەکانی خوێندکاران")

performance_counts = (
    df["ئاست"]
    .value_counts()
    .reset_index()
)

performance_counts.columns = [
    "ئاست",
    "ژمارەی خوێندکاران"
]

fig3 = px.pie(
    performance_counts,
    names="ئاست",
    values="ژمارەی خوێندکاران",
    title="دابەشبوونی ئاستی خوێندکاران",
    hole=0.4
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------------------
# 12. داگرتنی ئەنجامەکان
# -------------------------------------
st.subheader("📥 داگرتنی ئەنجامەکان")

# بەکارهێنانی utf-8-sig بۆ ئەوەی پیتە کوردییەکان لە Excel بە تێکچوویی دەرنەکەون
csv_data = display_df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    label="داگرتنی ڕاپۆرتی خوێندکاران (CSV)",
    data=csv_data,
    file_name="student_report_kurdish.csv",
    mime="text/csv"
)

# -------------------------------------
# 13. بەشی کۆتایی (Footer)
# -------------------------------------
st.success(
    "بەرنامەکە بە سەرکەوتوویی کاردەکات!"
)

st.caption(
    "تاقیگەی کڵاود کۆمپیوتینگ | بەشی زیرەکی دەستکرد (AI)"
)