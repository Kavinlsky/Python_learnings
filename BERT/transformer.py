from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# Example text data
corpus = ["This is the first document.",
          "This document is the second document.",
          "And this is the third one.",
          "Is this the first document?"]

# Create a CountVectorizer
count_vectorizer = CountVectorizer()
count_matrix = count_vectorizer.fit_transform(corpus)

# Create a TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

print("Count Vectorizer:")
print(count_matrix.toarray())
print(count_vectorizer.get_feature_names_out())

print("\nTF-IDF Vectorizer:")
print(tfidf_matrix.toarray())
print(tfidf_vectorizer.get_feature_names_out())
