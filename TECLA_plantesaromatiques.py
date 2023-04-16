import openai
import streamlit as st
import re
import os
from gtts import gTTS
from io import BytesIO
import json
import requests
import mysql.connector
from googleapiclient.discovery import build
import requests
from datetime import datetime


# Set the model engine and your OpenAI API key
model_engine = "text-davinci-003"

# Define la clave de API y el ID de búsqueda personalizada

api_key = st.secrets["auto_julia"]
cx = st.secrets["auto_patricia"]

db_host = st.secrets["DB_HOST"]
db_port = st.secrets["DB_PORT"]
db_name = st.secrets["DB_NAME"]
db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]

openai.api_key = st.secrets["auto_pau"]



st.markdown("""
<style>
body {
    font-size:75px !important;
}
</style>
""", unsafe_allow_html=True)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("Parlant amb la Maria, experta en plantes aromàtiques")
st.sidebar.header("Instruccions")
st.sidebar.info(
    '''Aquesta és una aplicació web pel projecte TECLA del [IAAC Fab Lab Barcelona](https://fablabbcn.org) i la [Fundación Diverse](https://fpdiverse.org/) on els nens i nenes poden fer preguntes sobre plantes aromàtiques.
       La Maria sap molt de Plantes Aromàtiques'.
       Escriu la pregunta i t'explicarà moltes coses.
       Coded with love by @xavidominguez
       '''
    )


def main():
    '''
    This function gets the user input, pass it to ChatGPT function and
    displays the response
    '''
    history_chat = 'Fem un joc i imaginem que et dius Maria i ets la millor experta en plantes aromàtiques. Només contesta preguntes sobre plantes aromàtiques.' \
                   'Necessito que em parlis com si tingues 8 anys i la resposta ha de ser 4 frases. Aquesta és la pregunta...'
    back_chat = 'Contesta si la pregunta està relacionada amb plantes aromàtiques. Contesta en català.'
    # Get user input
    user_query = st.text_input("Escriu la teva pregunta aquí :q", "Què son les plantes aromàtiques?")

    if user_query != ":q" or user_query != "":
        # Pass the query to the ChatGPT function
        history_chat_question = history_chat +' '+ user_query + ''+back_chat

        response = ChatGPT(history_chat_question)
        #history_chat = history_chat + response
        sound_file = BytesIO()
        tts = gTTS(f"{response}", lang='ca')
        tts.write_to_fp(sound_file)
        #response_pict = requests.get('https://api.arasaac.org/api/pictograms/32614?url=true&download=false')
        #imatgepict = json.loads(response_pict.text)
       # '''
        st.audio(sound_file)

        # Crea una conexión con la base de datos
        conn = mysql.connector.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)

        # Crea un cursor para ejecutar comandos SQL
        cur = conn.cursor()

        # Ejecuta una consulta SQL
        sql = "INSERT INTO iesrafaelalberti_plantes (pregunta, respuesta) VALUES (%s,%s)"
        valores = (user_query, response)
        cur.execute(sql,valores)

        # Obtiene los resultados de la consulta
        results_database = cur.fetchall()
        conn.commit()

        # Cierra la conexión con la base de datos
        cur.close()
        conn.close()
        st.write(f"{response}")
        # Define la consulta de búsqueda
        query = ChatGPT( "Quines son les paraules clau de:"+response)

        # Crea un servicio de búsqueda de Google
        # service = build('customsearch', 'v1', developerKey=api_key)
        image_url = "https://avivacocentaina.files.wordpress.com/2020/06/image.png"
        # Realiza la búsqueda
        #res = service.cse().list(q=query, cx=cx, searchType='image', imgSize='LARGE',imgType="photo",siteSearch="https://ca.wikipedia.org",siteSearchFilter='i').execute()
        #if "items" in res.keys():
            #image_url = res['items'][0]['link']
        #    image_url = "https://avivacocentaina.files.wordpress.com/2020/06/image.png"
        #else:
        #    image_url = "https://avivacocentaina.files.wordpress.com/2020/06/image.png"

        return st.image(
            image_url,
            width=600,  # Manually Adjust the width of the image as per requirement
        )
        #return st.write(f"{user_query} {response}")

def ChatGPT(user_query):
    '''
    This function uses the OpenAI API to generate a response to the given
    user_query using the ChatGPT model
    '''
    # Use the OpenAI API to generate a response
    completion = openai.Completion.create(
                                  engine = model_engine,
                                  prompt = user_query,
                                  n = 1,
                                  max_tokens=500,
                                  temperature = 0.4,
                                      )
    response = completion.choices[0].text
    return response

main()
