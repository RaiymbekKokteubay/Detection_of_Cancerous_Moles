import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
import time

API_TOKEN = st.secrets['api_token']
API_URL = st.secrets['api_url']
headers = {"Authorization": f"Bearer {API_TOKEN}"}

links = {
    "Melanoma": "https://www.wikipedia.org/wiki/Melanoma",
    "Vascular-lesions": "https://en.wikipedia.org/wiki/Vascular_anomaly",
}

def query(data):
    """Send a request to the API and return the response."""
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

if __name__ == '__main__':

    page_title = "Skin cancer detection"
    page_icon = "🐒"
    layout = "centered"

    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    st.title(page_title)

    st.write("""
        Hello! This app is an ongoing project that helps to promote cancer awareness.
        Please remember that the results of the computer vision might not be precise,
        and one should see a doctor for a professional observation. 

        First, you can upload an image of your skin lesion. Then, the model will predict
        the type of skin cancer and you can read more about the disease and its
        treatment.
        """)

    st.subheader("Image")
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])

    if image_file is not None:
        st.image(image_file, caption='Input Image', use_column_width=True)
        image_bytes = image_file.getvalue()
        st.subheader("Model output")

        with st.spinner("Waiting for the prediction..."):
            data = query(image_bytes)
            while "error" in data:
                time.sleep(4)
                data = query(image_bytes)
        st.success("Done!")

        scores = [e['score'] for e in data]

        labels = []
        for e in data:
            if e['label'] in links:
                labels.append(f"<a href='{links[e['label']]}' target='_blank'>{e['label']}</a>")
            else:
                labels.append(e['label'])

        df = pd.DataFrame({'scores': scores, 'labels': labels})
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        fig = px.bar(df, x='scores', y='labels', orientation='h', color='scores')
        st.write(fig)
        st.write("""
            The scores above represent the probability of having a skin cancer
            of a particular type. The higher the score, the higher the probability.
            Note that the model is not perfect, and one should see a doctor for
            a professional observation.

            Also, if the model returns a score of below 0.7 for all the classes, it means
            that the lesion is probably not a skin cancer.
        """)
