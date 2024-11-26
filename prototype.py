import streamlit as st
import pandas as pd
import random

# A/B test 
group = random.choice(['transparant_A', 'opaque_B'])
st.write(f"Group test: {group}")

# Genres uit de OBA catalogus
genres_OBA = [
    "Avonturenroman", "Bijbelse roman", "Biografie", "Boekstart", "Detectiveroman", "Dierenleven", 
    "Dokters-, verpleegsters- en ziekenhuisroman", "Erotische verhalen", "Experimentele roman",
    "Familieroman", "Feministische verhalen", "Griezelverhaal", "Historische roman", "Humoristische roman", 
    "Indisch milieu", "Islamitisch milieu", "Joods milieu", "Kerst", "Kinderleven", "Meisjesroman", 
    "Oorlog en verzet", "Paarden/pony’s", "Paasverhaal", "Politieke roman", "Protestants milieu", 
    "Psychologisch verhaal", "Roman over het rassenvraagstuk","Romantisch verhaal", "School",
    "Sciencefiction", "Sinterklaas", "Sociaal/politiek verhaal", "Spionageroman", "Sport",
    "Sprookjes", "Streek- en boerenroman", "Thriller", "Verhalenbundel", "Wild-westroman"
]

# Boekenlijst 
titles = ["A", "B", "C"]
images = ['x','xx', 'xxx']
authors = ['1','2', '3']
books = pd.DataFrame({'Title': titles, 'Image': images, 'Author': authors})

# Uitleg genereren per aanbeveling
def generate_uitleg(book, leeftijd, geslacht, opleiding, regio, genres):
        uitleg = 'uitleg'
        return uitleg

# Titel & privacyvoorwaarden
st.title("Onderzoek aanbevelingssysteem OBA")
st.subheader("Onderzoek & Privacy voorwaarden")
st.text("Onderzoek info, Privacy blabla Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent sollicitudin lacinia lorem at scelerisque. Phasellus sed iaculis velit, eu tempor quam. Donec accumsan arcu vitae eleifend sollicitudin. Pellentesque rutrum volutpat finibus. Curabitur suscipit auctor nisl, ac feugiat quam ullamcorper ut. Etiam ex nisi, scelerisque non sodales quis, accumsan sed ipsum. Aenean id tempor mauris, nec eleifend ex. Nam varius dolor nunc, nec venenatis sapien volutpat non. Donec turpis mauris, interdum ac neque vehicula, bibendum consectetur eros. In nec ex nisl. Mauris et augue tincidunt, sodales leo id, interdum leo. ")
accept_privacy = st.checkbox("Ik ga akkoord met de privacyvoorwaarden")

# test
# accept_privacy = True

# Verzamel gebruikersinformatie
if accept_privacy:
    st.subheader("Gegevens")
    leeftijd = st.number_input("Wat is je leeftijd?",18,120,step=1)
    geslacht = st.selectbox("Wat is je geslacht?", ["Man", "Vrouw", "Anders", "Zeg ik liever niet"])
    opleiding = st.selectbox("Wat is je hoogsteopleidingsniveau",["Geen diploma", "Middelbare school", "MBO", "HBO", "Universiteit"])
    regio = st.selectbox("In welke regio/stad/provincie woon je",["x", "y", "z", "r", "t"])
    genres = st.multiselect("Welke genres lees je graag?", genres_OBA)
    bevestig = st.button("Bevestig gegevens")

    #test
    bevestig = True

    #Geef samenvatting weer van de gegevens
    if bevestig:
        st.write("Samenvatting van je gegevens:")
        st.write(f"Leeftijdsgroep: {leeftijd}")
        st.write(f"Geslacht: {geslacht}")
        st.write(f"Opleidingsniveau: {opleiding}")
        st.write(f"Regio: {regio}")
        st.write(f"Genres: {genres}")

        st.subheader("Aanbevolen boeken:")
        for index, row in books.iterrows():
            # st.image(row['Image'])
            st.write(row['Image'])
            st.write(row['Title'])
            st.write(row['Author'])

        # if group == 'transparant_A':
        # if group == 'opaque_B':


        # def recommend_random_books():
        #     books = ["A", "B", "C", "D", "E", "F"]
        #     return random.sample(books, 6)

