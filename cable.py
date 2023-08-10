import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

# Function to extract text from URL
def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    return text

# Function to paraphrase text using OpenAI
def paraphrase_text(text, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You are a professional journalist writing for Reuters."
            },
            {
                "role": "user",
                "content": f"Write an article in Spanish, following this style of Reuters, writing style is characterized by its objectivity, clarity, and conciseness. It focuses on presenting the most relevant facts in an unbiased and accurate manner, using simple, direct language with the text: {text} Also, start each sentence with a capital letter and end it with a period. Add a SEO Friendly title and end the article with 10 SEO Keywords."
            }
        ],
    )
    paraphrased_text = response['choices'][0]['message']['content']
    return paraphrased_text

# Streamlit UI
st.title('Reinterpretación de artículos')
with st.sidebar:
    st.header("Configuración de clave")
    openai_api_key = st.text_input('Ingresa la clave que recibiste:')

url_input = st.text_input('Ingrese la URL:')
if st.button('Cargar URL'):
    text = extract_text_from_url(url_input)
    st.text_area("Texto original:", value=text, height=200)  # Preview of extracted text
    st.session_state.text_to_paraphrase = text

if st.button('Reinterpretar'):
    if 'text_to_paraphrase' in st.session_state:
        with st.spinner('Procesando...'):
            paraphrased_text = paraphrase_text(st.session_state.text_to_paraphrase, openai_api_key)
            st.text_area("Texto reinterpretado:", value=paraphrased_text, height=600)  # Display paraphrased text in text area
    else:
        st.warning('Por favor, primero haga clic en "Cargar URL" antes de reinterpretar.')

