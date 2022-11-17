import streamlit as st
from PIL import Image
import requests
import json

API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/gianlab/swin-tiny-patch4-window7-224-finetuned-skin-cancer"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

def load_image(image_file):
    img = Image.open(image_file)
    return img

if __name__ == '__main__':

    page_title = "Skin cancer detection"
    page_icon = ":monkey:"
    layout = "centered"

    st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
    st.title(page_title + " " + page_icon)

    st.subheader("Image")
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])

    if image_file is not None:

              # To View Uploaded Image
        st.image(load_image(image_file),width=250)

        data = query(
            {
                "inputs": image_file,
                # "parameters": {"do_sample": False},
            }
        )
