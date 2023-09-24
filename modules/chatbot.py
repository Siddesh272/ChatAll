import re
import random
import speech_recognition as sr
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

chatbot = pipeline("conversational",model="distilbert-base-uncased")

faq_responses = {}
with open("static/faq_responses.txt", "r") as faq_file:
    lines = faq_file.readlines()
    for line in lines:
        q, a = line.strip().split("#")
        faq_responses[q] = a

sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2',embedding_dim=128)
def text_chatbot(user_input):
    response = pipeline("conversational")(user_input)[0]['generated_text']
    return response

import faiss

def semantic_search(query, faq_responses, threshold=0.7):
  query_embedding = sentence_model.encode([query], convert_to_tensor=True)

  # Create a Faiss index
  index = faiss.IndexFlatL2(128)

  # Add the FAQ embeddings to the index
  index.add(sentence_model.encode(list(faq_responses.keys())))

  # Search for the most similar FAQ questions
  distances, indices = index.search(query_embedding, k=10)

  similar_questions = []
  for i in indices[0]:
    if distances[0][i] < threshold:
      similar_questions.append(list(faq_responses.keys())[i])  

  return similar_questions


def get_response(user_input):
    user_input = user_input.strip().lower()
    if user_input == "exit":
        print("Goodbye!")
        return "Goodbye!"
    similar_questions = semantic_search(user_input, faq_responses)
    if similar_questions:
        response = faq_responses[similar_questions[0]]
        return response
    return "I'm sorry, I don't have an answer for that."
