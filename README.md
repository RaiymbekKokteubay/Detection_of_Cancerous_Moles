# Formality Classifier

This is a machine learning project that can distinguish the level of formality of a given text. The model is fine-tuned on top of the BERT language model and hosted on [Hugging Face](https://huggingface.co/Raiymbek/formality_classifier_bert).

The fine-tuned model can classify text into two categories: formal and informal.

## Usage

You can use the model in your Python projects by installing the transformers library and loading the pre-trained model from Hugging Face:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("Raiymbek/formality_classifier_bert")
model = AutoModelForSequenceClassification.from_pretrained("Raiymbek/formality_classifier_bert")

text = "The meeting is scheduled for tomorrow at 10 am."
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)
predicted_class = torch.argmax(outputs.logits).item()
predicted_label = model.config.id2label[predicted_class]

print(f"The predicted formality level for the text '{text}' is '{predicted_label}'.")
```

Alternatively, you can use the deployed Streamlit app by following the link: https://formality-classificator-raiymbek-kokteubay.streamlit.app. You can input text into the app and it will classify it into one of the two formality levels.