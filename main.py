import streamlit as st
import requests
import json
import time

API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/gianlab/swin-tiny-patch4-window7-224-finetuned-skin-cancer"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(data):
    """Send a request to the API and return the response."""
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

if __name__ == '__main__':

    page_title = "Skin cancer detection"
    page_icon = ":monkey:"
    layout = "centered"

    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    st.title(page_title + " " + page_icon)

    st.subheader("Image")
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])

    if image_file is not None:
        st.image(image_file, caption='Input Image', use_column_width=True)
        image_bytes = image_file.getvalue()

        st.subheader("Prediction")

        while True:
            data = query(image_bytes)
            if "error" in data:
                est_time = data["estimated_time"]
                st.error(f"Model is loading. Please wait {est_time} seconds.")
                time.sleep(4)
            else:
                st.write(data)
                break