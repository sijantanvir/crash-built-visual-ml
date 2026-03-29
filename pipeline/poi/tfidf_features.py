import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def build_category_corpus(poi_df, crash_df, radius=500):
    """
    For each crash point, collect nearby POI categories as 'documents'.
    """

    documents = []
    ids = []

    for _, crash in crash_df.iterrows():
        lat_c, lon_c = crash["Lat"], crash["Long"]

        # simple distance filter (reuse haversine)
        distances = (
            (poi_df["Lat"] - lat_c)**2 +
            (poi_df["Long"] - lon_c)**2
        ) ** 0.5

        nearby = poi_df[distances <= 0.005]  # approx ~500m

        categories = nearby["category"].dropna().astype(str).tolist()

        documents.append(" ".join(categories))
        ids.append(crash["id"])

    return documents, ids


def compute_tfidf_features(poi_df, crash_df):
    """
    Compute TF-IDF weighted POI features.
    """

    print("[POI] Computing TF-IDF features...")

    documents, ids = build_category_corpus(poi_df, crash_df)

    vectorizer = TfidfVectorizer(
        max_features=50,
        token_pattern=r"(?u)\b\w+\b"
    )

    X = vectorizer.fit_transform(documents)

    feature_names = vectorizer.get_feature_names_out()

    tfidf_df = pd.DataFrame(X.toarray(), columns=feature_names)
    tfidf_df["id"] = ids

    return tfidf_df