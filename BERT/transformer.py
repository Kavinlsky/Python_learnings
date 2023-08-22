from transformers import pipeline

# Load the text classification pipeline
classifier = pipeline("sentiment-analysis")

# Classify a piece of text
result = classifier("I satisfy by learning the css")
print(result)
