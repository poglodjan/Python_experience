import streamlit as st
import pandas as pd
import networkx as nx
import numpy as np
from gensim.models import Word2Vec
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
import seaborn as sns
import random
import os
import requests
import zipfile
import gc

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Movie Recommender System", layout="wide")

# CUSTOM TITLE (HTML/CSS)
st.markdown("""
    <div style='text-align: center; margin-bottom: 50px;'>
        <h1 style='font-size: 70px; margin-bottom: 0px;'>
            Advanced Movie Recommender System
        </h1>
        <h2 style='font-size: 35px; color: gray; margin-top: 10px; font-weight: normal;'>
            (based on MovieLens 1M library of movies)
        </h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; margin-bottom: 30px; font-size: 18px;'>
Comparison between two recommendation methods:<br>
<b>1. Node2Vec</b> (Graph Embedding / Random Walk) &nbsp;|&nbsp; 
<b>2. SVD</b> (Matrix Factorization / Collaborative Filtering)
</div>
""", unsafe_allow_html=True)

# ==========================================
# 1. DATA LOADING (ML-1M)
# ==========================================
@st.cache_resource
def load_data_1m():
    url = "https://files.grouplens.org/datasets/movielens/ml-1m.zip"
    data_dir = "ml-1m"
    zip_path = "ml-1m.zip"
    
    if not os.path.exists(data_dir):
        if not os.path.exists(zip_path):
            with st.spinner('Downloading MovieLens 1M dataset...'):
                r = requests.get(url)
                with open(zip_path, 'wb') as f:
                    f.write(r.content)
        with st.spinner('Extracting files...'):
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall()
    
    # Parsing
    with st.spinner('Loading data into memory...'):
        movies = pd.read_csv(f"{data_dir}/movies.dat", sep='::', engine='python', 
                             encoding='latin-1', names=['movieId', 'title', 'genres'])
        
        ratings = pd.read_csv(f"{data_dir}/ratings.dat", sep='::', engine='python', 
                              names=['userId', 'movieId', 'rating', 'timestamp'])
        
        # Filter positive ratings for the graph structure
        positive_ratings = ratings[ratings['rating'] >= 4.0]
        
    return ratings, movies, positive_ratings

try:
    ratings_df, movies_df, pos_ratings = load_data_1m()
    
    # Mappings
    movie_id_to_title = dict(zip(movies_df['movieId'], movies_df['title']))
    title_to_movie_id = dict(zip(movies_df['title'], movies_df['movieId']))
    all_genres = sorted(list(set(movies_df['genres'].str.split('|').explode())))
    
    # Calculate popularity for better centroid calculation in SVD
    movie_popularity = ratings_df['movieId'].value_counts()
    
    st.markdown(f"<div style='text-align: center; color: green; margin-bottom: 20px;'>Data Loaded Successfully: {len(ratings_df):,} ratings, {len(movies_df):,} movies.</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Data loading error: {e}")
    st.stop()

# ==========================================
# 2. MODEL IMPLEMENTATION
# ==========================================

class RecommenderBase:
    """Base class helpers"""
    def _filter_results(self, similar_nodes, top_n, exclude_id=None):
        recommendations = []
        for node, score in similar_nodes:
            if isinstance(node, str) and node.startswith('m_'): # Node2Vec format
                m_id = int(node.split('_')[1])
            else:
                m_id = node # SVD format (raw ID)
                
            if m_id != exclude_id:
                recommendations.append((m_id, score))
                if len(recommendations) >= top_n: break
        return recommendations

class Node2VecRecommender(RecommenderBase):
    def __init__(self, data, vector_size=64, walk_length=15, num_walks=5):
        self.data = data
        self.vector_size = vector_size
        self.walk_length = walk_length
        self.num_walks = num_walks
        self.model = None
        self.graph = None
        self.movie_nodes = []

    def fit(self):
        self.graph = nx.Graph()
        edges = [(f"u_{uid}", f"m_{mid}") for uid, mid in zip(self.data['userId'], self.data['movieId'])]
        self.graph.add_edges_from(edges)
        self.movie_nodes = [n for n in self.graph.nodes() if n.startswith('m_')]
        
        walks = []
        nodes = list(self.graph.nodes())
        
        # DeepWalk-like random walks
        for i in range(self.num_walks):
            random.shuffle(nodes)
            for node in nodes:
                walk = [node]
                while len(walk) < self.walk_length:
                    cur = walk[-1]
                    try:
                        nbrs = list(self.graph[cur])
                        if nbrs: walk.append(random.choice(nbrs))
                        else: break
                    except: break
                walks.append(walk)
        
        self.model = Word2Vec(sentences=walks, vector_size=self.vector_size, window=5, min_count=5, sg=1, workers=4)
        del walks
        gc.collect()

    def recommend_by_id(self, movie_id, top_n=5):
        node_id = f"m_{movie_id}"
        if node_id not in self.model.wv: return []
        similar = self.model.wv.most_similar(node_id, topn=top_n+20)
        return self._filter_results(similar, top_n, exclude_id=movie_id)

    def recommend_by_genre(self, genre, movies_df, top_n=5):
        # Improved strategy: use top 50 popular movies of that genre to form the centroid
        candidates = movies_df[movies_df['genres'].str.contains(genre, regex=False)]['movieId'].values
        
        vectors = []
        for mid in candidates:
            nid = f"m_{mid}"
            if nid in self.model.wv:
                vectors.append(self.model.wv[nid])
        
        if not vectors: return []
        
        # Calculate centroid
        genre_vector = np.mean(vectors, axis=0)
        
        similar = self.model.wv.similar_by_vector(genre_vector, topn=top_n+20)
        return self._filter_results(similar, top_n)

    def get_embeddings(self):
        ids, vecs = [], []
        for node in self.movie_nodes:
            if node in self.model.wv:
                vecs.append(self.model.wv[node])
                ids.append(int(node.split('_')[1]))
        return np.array(ids), normalize(np.array(vecs))

class SVDRecommender(RecommenderBase):
    def __init__(self, ratings_df, n_components=50):
        self.ratings_df = ratings_df
        self.n_components = n_components
        self.movie_user_matrix = None
        self.svd = None
        self.item_vectors = None 
        self.corr_matrix = None

    def fit(self):
        self.movie_user_matrix = self.ratings_df.pivot(index='movieId', columns='userId', values='rating').fillna(0)
        self.svd = TruncatedSVD(n_components=self.n_components, random_state=42)
        self.item_vectors = self.svd.fit_transform(self.movie_user_matrix)
        self.item_vectors = normalize(self.item_vectors)
        self.corr_matrix = cosine_similarity(self.item_vectors)

    def recommend_by_id(self, movie_id, top_n=5):
        if movie_id not in self.movie_user_matrix.index: return []
        idx = self.movie_user_matrix.index.get_loc(movie_id)
        corr = self.corr_matrix[idx]
        top_indices = corr.argsort()[-(top_n+1):-1][::-1]
        
        recs = []
        for i in top_indices:
            recs.append((self.movie_user_matrix.index[i], corr[i]))
        return recs

    def recommend_by_genre(self, genre, movies_df, top_n=5, popularity_df=None):
        # FIX for 0% Match: Filter candidates to only include popular movies
        
        genre_movies = movies_df[movies_df['genres'].str.contains(genre, regex=False)]
        
        if popularity_df is not None:
             valid_pop = popularity_df[popularity_df.index.isin(genre_movies['movieId'])]
             top_genre_ids = valid_pop.head(50).index.tolist()
        else:
             top_genre_ids = genre_movies['movieId'].head(50).values

        valid_indices = []
        for mid in top_genre_ids:
            if mid in self.movie_user_matrix.index:
                valid_indices.append(self.movie_user_matrix.index.get_loc(mid))
        
        if not valid_indices: return []
        
        genre_vec = np.mean(self.item_vectors[valid_indices], axis=0)
        sim_scores = cosine_similarity(genre_vec.reshape(1, -1), self.item_vectors).flatten()
        top_indices = sim_scores.argsort()[-top_n:][::-1]
        
        recs = []
        for i in top_indices:
            recs.append((self.movie_user_matrix.index[i], sim_scores[i]))
        return recs

    def get_embeddings(self):
        return self.movie_user_matrix.index.values, self.item_vectors

# ==========================================
# 3. TRAINING
# ==========================================
@st.cache_resource
def train_models(_pos_ratings, _all_ratings):
    with st.spinner('Training Node2Vec (Graph based)...'):
        n2v = Node2VecRecommender(_pos_ratings, num_walks=4, walk_length=12)
        n2v.fit()
        
    with st.spinner('Training SVD (Matrix based)...'):
        svd = SVDRecommender(_all_ratings, n_components=50)
        svd.fit()
    return n2v, svd

n2v_model, svd_model = train_models(pos_ratings, ratings_df)

# ==========================================
# 4. METRICS UTILS
# ==========================================
def calculate_metrics(recommendations, movies_df, ratings_df, source_genre=None):
    if not recommendations:
        return 0, 0, 0

    rec_ids = [r[0] for r in recommendations]
    rec_movies = movies_df[movies_df['movieId'].isin(rec_ids)]
    
    # 1. Diversity (Unique genres count / Total items)
    # Since one movie can have multiple genres, this ratio can be > 1.0
    all_rec_genres = rec_movies['genres'].str.split('|').explode().tolist()
    unique_genres = set(all_rec_genres)
    diversity = len(unique_genres) / len(rec_ids) if len(rec_ids) > 0 else 0
    
    # 2. Novelty (Inverse popularity)
    popularity = ratings_df[ratings_df['movieId'].isin(rec_ids)]['movieId'].value_counts().mean()
    # Normalize log scale (Max ~3400 ratings => log ~8.1)
    novelty = 1 - (np.log(popularity + 1) / 8.5) if popularity > 0 else 0
    novelty = max(0, novelty)
    
    # 3. Genre Consistency
    consistency = 0
    if source_genre:
        matches = rec_movies['genres'].str.contains(source_genre, regex=False).sum()
        consistency = matches / len(rec_ids)
        
    return diversity, novelty, consistency

# ==========================================
# 5. UI - TABS
# ==========================================
tab1, tab2, tab3 = st.tabs(["Recommendations", "Cluster Visualization", "Comparative Metrics"])

# --- TAB 1: RECOMMENDATIONS ---
with tab1:
    col_ctrl, col_res = st.columns([1, 2])
    
    with col_ctrl:
        st.subheader("Settings")
        mode = st.radio("Recommendation Mode:", ["By Movie", "By Genre"])
        
        selected_movie_id = None
        selected_genre = None
        
        if mode == "By Movie":
            titles = sorted(movies_df['title'].unique())
            start_idx = titles.index("Toy Story (1995)") if "Toy Story (1995)" in titles else 0
            sel_title = st.selectbox("Select Movie:", titles, index=start_idx)
            selected_movie_id = title_to_movie_id[sel_title]
            
            g = movies_df[movies_df['movieId']==selected_movie_id]['genres'].values[0]
            st.caption(f"Genres: {g}")
            
        else:
            selected_genre = st.selectbox("Select Genre:", all_genres)
            st.info(f"Finding movies that best represent **{selected_genre}**.")

        btn = st.button("Generate Recommendations", type="primary")

    with col_res:
        if btn:
            # FETCHING RESULTS
            recs_n2v = []
            recs_svd = []
            source_g_for_metrics = None
            
            if mode == "By Movie":
                recs_n2v = n2v_model.recommend_by_id(selected_movie_id)
                recs_svd = svd_model.recommend_by_id(selected_movie_id)
                source_g_for_metrics = movies_df[movies_df['movieId']==selected_movie_id]['genres'].values[0].split('|')[0]
            else:
                recs_n2v = n2v_model.recommend_by_genre(selected_genre, movies_df)
                recs_svd = svd_model.recommend_by_genre(selected_genre, movies_df, popularity_df=movie_popularity)
                source_g_for_metrics = selected_genre

            # DISPLAY
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Node2Vec")
                st.caption("(Graph Random Walk)")
                if recs_n2v:
                    for rid, s in recs_n2v:
                        t = movie_id_to_title.get(rid, str(rid))
                        g = movies_df[movies_df['movieId']==rid]['genres'].values[0]
                        st.markdown(f"**{t}**\n\n*{g}* (Sim: {s:.2f})")
                else: st.warning("No results found.")
            
            with c2:
                st.subheader("SVD")
                st.caption("(Matrix Factorization)")
                if recs_svd:
                    for rid, s in recs_svd:
                        t = movie_id_to_title.get(rid, str(rid))
                        g = movies_df[movies_df['movieId']==rid]['genres'].values[0]
                        st.markdown(f"**{t}**\n\n*{g}* (Sim: {s:.2f})")
                else: st.warning("No results found.")
            
            # Save for Tab 3
            st.session_state['last_recs'] = (recs_n2v, recs_svd, source_g_for_metrics)

# --- TAB 2: CLUSTERS (SIDE BY SIDE) ---
with tab2:
    st.header("Movie Space Visualization")
    st.markdown("Comparing how both models group movies. Dots are movies, colors are clusters.")
    
    if st.button("Render Clusters"):
        with st.spinner("Calculating t-SNE and Clusters for both models (this might take a moment)..."):
            
            # Helper to generate plot data
            def get_plot_data(model, model_name):
                ids, vecs = model.get_embeddings()
                # Sample max 1500 points
                if len(ids) > 1500:
                    idx = np.random.choice(len(ids), 1500, replace=False)
                    ids_s = ids[idx]
                    vecs_s = vecs[idx]
                else:
                    ids_s, vecs_s = ids, vecs
                
                # TSNE
                tsne = TSNE(n_components=2, init='pca', learning_rate='auto', random_state=42)
                vecs_2d = tsne.fit_transform(vecs_s)
                
                # KMeans
                n_clust = 6
                kmeans = KMeans(n_clusters=n_clust, random_state=42)
                clusters = kmeans.fit_predict(vecs_s)
                
                return pd.DataFrame({
                    'x': vecs_2d[:,0], 'y': vecs_2d[:,1], 'cluster': clusters,
                    'title': [movie_id_to_title.get(i, "") for i in ids_s],
                    'genre': [movies_df[movies_df['movieId']==i]['genres'].values[0] for i in ids_s]
                })

            # Get data
            df_n2v = get_plot_data(n2v_model, "Node2Vec")
            df_svd = get_plot_data(svd_model, "SVD")
            
            # Helper to get dominant genre (Top 2)
            def get_cluster_desc(df):
                desc = []
                for c in range(6):
                    subset = df[df['cluster'] == c]
                    if not subset.empty:
                        # Explode genres to count individual ones
                        all_genres = subset['genre'].str.split('|').explode()
                        # Take top 2 most common genres
                        top_genres = all_genres.value_counts().head(2).index.tolist()
                        genre_str = " / ".join(top_genres)
                        desc.append(f"**Cluster {c}:** {genre_str}")
                    else:
                        desc.append(f"**Cluster {c}:** Empty")
                return desc

            n2v_desc = get_cluster_desc(df_n2v)
            svd_desc = get_cluster_desc(df_svd)
            
            # Render Side-by-Side
            col_viz1, col_viz2 = st.columns(2)
            
            with col_viz1:
                st.subheader("Node2Vec Structure")
                fig1, ax1 = plt.subplots(figsize=(6, 5))
                sns.scatterplot(data=df_n2v, x='x', y='y', hue='cluster', palette='turbo', s=30, alpha=0.7, ax=ax1, legend=False)
                plt.axis('off')
                st.pyplot(fig1)
                st.markdown("#### Dominant Categories (Node2Vec)")
                st.markdown("  \n".join(n2v_desc))
                
            with col_viz2:
                st.subheader("SVD Structure")
                fig2, ax2 = plt.subplots(figsize=(6, 5))
                sns.scatterplot(data=df_svd, x='x', y='y', hue='cluster', palette='turbo', s=30, alpha=0.7, ax=ax2, legend=False)
                plt.axis('off')
                st.pyplot(fig2)
                st.markdown("#### Dominant Categories (SVD)")
                st.markdown("  \n".join(svd_desc))

# --- TAB 3: METRICS ---
with tab3:
    st.header("Quality Metrics Analysis")
    
    if 'last_recs' in st.session_state:
        recs_n2v, recs_svd, source_g = st.session_state['last_recs']
        
        # Calculate
        m_n2v = calculate_metrics(recs_n2v, movies_df, ratings_df, source_g)
        m_svd = calculate_metrics(recs_svd, movies_df, ratings_df, source_g)
        
        # Dataframe
        metrics_data = pd.DataFrame({
            'Metric': ['Diversity', 'Novelty', 'Genre Match'] * 2,
            'Score': [m_n2v[0], m_n2v[1], m_n2v[2], m_svd[0], m_svd[1], m_svd[2]],
            'Model': ['Node2Vec']*3 + ['SVD']*3
        })
        
        # Determine max Y limit to handle Diversity > 1.0
        max_val = metrics_data['Score'].max()
        y_limit = max(1.1, max_val + 0.2)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=metrics_data, x='Metric', y='Score', hue='Model', palette=['#FF4B4B', '#1E90FF'], ax=ax)
        plt.ylim(0, y_limit) # Dynamic limit
        
        # Add values
        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f')
            
        plt.title(f"Comparison for target: {source_g}")
        st.pyplot(fig)
        
        st.markdown("""
        **Metric Explanations:**
        * **Diversity:** Ratio of unique genres per number of recommended movies. Can be > 1.0 because movies often have multiple genres (e.g. *Comedy|Romance* counts as 2 genres for 1 movie).
        * **Novelty:** Measures how "niche" the recommendations are. Higher score = less popular movies.
        * **Genre Match:** Percentage of recommendations that share the source genre.
        """)
        
    else:
        st.info("Please generate recommendations in the first tab to see metrics here.")

st.markdown("---")
st.caption("Powered by Streamlit & MovieLens 1M | Python Project")