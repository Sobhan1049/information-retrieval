import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# مسیر فولدر حاوی فایل‌های متنی
folder_path = "results"

# خواندن فایل‌های متنی از فولدر
documents = []
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            documents.append(file.read())

# query
query = "Web scraping"


# توکنایزر و شاخص وارون
def tokenize(text):
    stop_words = set(stopwords.words('English'))
    ps = PorterStemmer()
    words = word_tokenize(text)
    words = [ps.stem(word) for word in words if word.isalnum() and word not in stop_words]
    return words


# محاسبه tf-idf برای اسناد

vectorizer = TfidfVectorizer(tokenizer=None)
tfidf_matrix = vectorizer.fit_transform(documents)

# محاسبه tf-idf برای query
query_vector = vectorizer.transform([query])

# محاسبه شباهت کسینوسی بین بردار query و بردارهای اسناد
similarities = cosine_similarity(tfidf_matrix, query_vector)

# نمایش عناوین اسناد مشابه به ترتیب نزولی شباهت
result_indices = similarities.flatten().argsort()[::-1]
for idx in result_indices:
    print(f"Title: {os.listdir(folder_path)[idx]},  Similarity: {similarities[idx][0]}")
