# streamlit_app.py

import streamlit as st
import pandas as pd
from io import StringIO
from google.oauth2 import service_account
from google.cloud import storage

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)

# Retrieve file contents.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=10)
def read_file(bucket_name, score_file_path, ranking_file_path):
    bucket = client.bucket(bucket_name)
    scores = bucket.blob(score_file_path).download_as_string().decode("utf-8")
    rankings = bucket.blob(ranking_file_path).download_as_string().decode("utf-8")
    return scores, rankings

bucket_name = "scoutoid-streamlit-bucket"
scores_file_path = "scores.csv"
rankings_file_path = "rankings.csv"

scores, rankings = read_file(bucket_name, scores_file_path, rankings_file_path)

# Print results.


tab1, tab2 = st.tabs(["Scores", "Rankings"])

with tab1:
   st.header("Scores")
   df = pd.read_csv(StringIO(scores), sep=",")
   st.dataframe(df)

with tab2:
   st.header("Rankings")
   df = pd.read_csv(StringIO(rankings), sep=",")
   st.dataframe(df)

    
    
# st.write(content)
# for line in content.strip().split("\n"):
#     st.write(line)
