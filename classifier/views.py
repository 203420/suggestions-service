from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from pathlib import Path
from unidecode import unidecode
import pickle

from classifier.serializers import wordsListSerializer

BASE_DIR = Path(__file__).resolve().parent.parent
path = str(BASE_DIR)
path = path.replace('\\', '/')

with open('vectorizador.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

with open('clasificador.pkl', 'rb') as classifier_file:
    classifier = pickle.load(classifier_file)

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Create your views here.
class classifierView(APIView):
    def process_text(self, text):
        text = unidecode(str(text))
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('spanish'))
        new_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(word) for word in new_tokens]
        final_text = ' '.join(lemmatized_tokens)
        return final_text


    def format_response(self, input_text):
        key_words = []
        new_text = self.process_text(input_text)
        vectorized_text = vectorizer.transform([new_text])
        predicted_probs = classifier.predict_proba(vectorized_text)

        for i in range(len(predicted_probs[0])):
            if predicted_probs[0][i] > 0.105:
                if "/" in str(classifier.classes_[i]):
                    words = classifier.classes_[i].split("/")
                    for word in words:
                        if word not in key_words:
                            key_words.append(word)
        return key_words


    def post(self, request):
        serializer = wordsListSerializer(data=request.data)
        if serializer.is_valid():
            words = self.format_response(serializer.data['text'])
            return Response(words, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
