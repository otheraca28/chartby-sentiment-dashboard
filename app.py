
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Dashboard Analisis Sentimen Chartby",
    page_icon="📊",
    layout="wide"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

.stApp{
    background-color:#f5f7fb;
}

.hero{
    background: linear-gradient(135deg,#2563eb,#14b8a6);
    padding:30px;
    border-radius:20px;
    color:white;
    text-align:center;
    margin-bottom:20px;
}

.section{
    background:white;
    padding:20px;
    border-radius:15px;
    margin-top:20px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown("""
<div class="hero">
    <h1>📊 Dashboard Analisis Sentimen Chartby</h1>
    <p>Visualisasi Sentimen Ulasan Pengguna Aplikasi Chartby</p>
</div>
""", unsafe_allow_html=True)

# =========================
# UPLOAD FILE
# =========================

uploaded_file = st.file_uploader(
    "📁 Upload Dataset CSV",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # =========================
    # VALIDASI KOLOM
    # =========================

    required_columns = [
        "rating",
        "sentiment",
        "clean_review"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        st.error(
            f"Kolom tidak ditemukan: {missing_columns}"
        )
        st.stop()

    # =========================
    # FILTER
    # =========================

    st.sidebar.header("🔎 Filter Data")

    rating_filter = st.sidebar.multiselect(
        "Pilih Rating",
        sorted(df["rating"].unique()),
        default=sorted(df["rating"].unique())
    )

    sentiment_filter = st.sidebar.multiselect(
        "Pilih Sentimen",
        sorted(df["sentiment"].unique()),
        default=sorted(df["sentiment"].unique())
    )

    df_filter = df[
        (df["rating"].isin(rating_filter))
        &
        (df["sentiment"].isin(sentiment_filter))
    ]

    if df_filter.empty:
        st.warning(
            "Data kosong setelah filter."
        )
        st.stop()

    # =========================
    # DISTRIBUSI RATING
    # =========================

    st.markdown(
        '<div class="section">',
        unsafe_allow_html=True
    )

    st.subheader("📊 Distribusi Rating")

    rating_count = (
        df_filter["rating"]
        .value_counts()
        .sort_index()
    )

    col1, col2 = st.columns(2)

    with col1:

        fig1, ax1 = plt.subplots(figsize=(6,4))

        sns.barplot(
            x=rating_count.index,
            y=rating_count.values,
            ax=ax1
        )

        ax1.set_xlabel("Rating")
        ax1.set_ylabel("Jumlah Review")

        st.pyplot(fig1)

    with col2:

        fig2, ax2 = plt.subplots(figsize=(6,4))

        ax2.pie(
            rating_count.values,
            labels=rating_count.index,
            autopct="%1.1f%%"
        )

        st.pyplot(fig2)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # =========================
    # DISTRIBUSI SENTIMEN
    # =========================

    st.markdown(
        '<div class="section">',
        unsafe_allow_html=True
    )

    st.subheader("📈 Distribusi Sentimen")

    sentiment_count = (
        df_filter["sentiment"]
        .value_counts()
    )

    col3, col4 = st.columns(2)

    with col3:

        fig3, ax3 = plt.subplots(figsize=(6,4))

        sns.barplot(
            x=sentiment_count.index,
            y=sentiment_count.values,
            ax=ax3
        )

        ax3.set_xlabel("Sentimen")
        ax3.set_ylabel("Jumlah Review")

        st.pyplot(fig3)

    with col4:

        fig4, ax4 = plt.subplots(figsize=(6,4))

        ax4.pie(
            sentiment_count.values,
            labels=sentiment_count.index,
            autopct="%1.1f%%"
        )

        st.pyplot(fig4)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # =========================
    # WORDCLOUD
    # =========================

    st.markdown(
        '<div class="section">',
        unsafe_allow_html=True
    )

    st.subheader("☁️ WordCloud")

    text = " ".join(
        df_filter["clean_review"]
        .dropna()
        .astype(str)
    )

    if text.strip():

        wordcloud = WordCloud(
            width=1000,
            height=500,
            background_color="white"
        ).generate(text)

        fig5, ax5 = plt.subplots(
            figsize=(12,5)
        )

        ax5.imshow(
            wordcloud,
            interpolation="bilinear"
        )

        ax5.axis("off")

        st.pyplot(fig5)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # =========================
    # DATASET
    # =========================

    st.markdown(
        '<div class="section">',
        unsafe_allow_html=True
    )

    st.subheader("📄 Dataset Hasil Analisis")

    st.dataframe(
        df_filter[
            [
                "rating",
                "sentiment",
                "clean_review"
            ]
        ],
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

else:

    st.info(
        "Silakan upload dataset CSV terlebih dahulu."
        )

