import streamlit as st
import requests
import random

# A/B test ############################################################################### kan ook in session state TO DO 
group = random.choice(['transparant_A', 'opaque_B'])
st.write(f"Group test: {group}")

#TEST session state gegevens zien
st.write("**SESSION DATA**")
st.write(st.session_state)

if "privacy_accepted" not in st.session_state:
    st.session_state["privacy_accepted"] = False
if "personal_data" not in st.session_state:
    st.session_state["personal_data"] = None
if "selected_books" not in st.session_state:
    st.session_state["selected_books"] = []

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

# Bevestig privacy en deelnname onderzoek
def show_privacy():
    st.title("Onderzoek aanbevelingssysteem OBA")
    st.subheader("Onderzoek & Privacy voorwaarden")
    st.write("Lees hier de informatie over het onderzoek en de privacyvoorwaarden.")

# #TestXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#     st.session_state["privacy_accepted"] = True
#     st.rerun()

    if st.checkbox("Ik ga akkoord met de privacyvoorwaarden"):
        st.session_state["privacy_accepted"] = True
        st.rerun()

# Verkrijg gegevens gebruiker
def collect_personal_data():
    st.subheader("Gegevens")
    leeftijd = st.text_input("Wat is je leeftijd?", placeholder="Vul een getal in tussen 18 en 120")
    geslacht = st.selectbox("Wat is je geslacht?", ["", "Man", "Vrouw", "Anders", "Zeg ik liever niet"])
    opleiding = st.selectbox("Wat is je hoogste opleidingsniveau", ["", "Geen diploma", "Middelbare school", "MBO", "HBO", "Universiteit"])
    regio = st.selectbox("In welke regio/stad/provincie woon je", ["", "x", "y", "z", "r", "t"])
    genres = st.multiselect("Welke genres lees je graag?", genres_OBA)
    bevestig = st.button("Bevestig gegevens")

# #TestXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#     leeftijd = "26"
#     geslacht = "Vrouw"
#     opleiding = "Universiteit"
#     regio = "c'"
#     genres = ["Kerst","Biografie"]
#     bevestig = True

    # controleer of alle gegevens (correct) zijn ingevoerd
    if bevestig:
        errors = []
        if not leeftijd.strip():
            errors.append("Leeftijd is vereist.")
        elif not leeftijd.isdigit() or not (18 <= int(leeftijd) <= 120):
            errors.append("Leeftijd moet een getal tussen 18 en 120 zijn.")
        if not geslacht:
            errors.append("Geslacht is vereist.")
        if not opleiding:
            errors.append("Opleidingsniveau is vereist.")
        if not regio:
            errors.append("Regio is vereist.")
        if not genres:
            errors.append("Selecteer ten minste één genre.")
        if errors:
            st.error("De volgende gegevens ontbreken of zijn onjuist:")
            for error in errors:
                st.write(error)
        else:
            # sla gegevens op in sessie
            st.session_state["personal_data"] = {
                "leeftijd": leeftijd,
                "geslacht": geslacht,
                "opleiding": opleiding,
                "regio": regio,
                "genres": genres
            }
            st.rerun()

# Boek toevoegen aan selectie, gebruikt door reading_history()
def add_book_to_selection(book):
    if book not in st.session_state["selected_books"]:
        st.session_state["selected_books"].append(book)

# Boek verwijderen uit selectie, gebruikt door select_and_rate_book()
def remove_book_from_selection(book):
    if book in st.session_state["selected_books"]:
        st.session_state["selected_books"].remove(book)

# Toon samenvatting persoonlijke gegevens en bewerkknop
def show_personal_data():
        st.header("Profiel")
        st.write("Je hebt de volgende gegevens ingevuld:")
        st.write(f"Leeftijd: {st.session_state['personal_data']['leeftijd']}")
        st.write(f"Geslacht: {st.session_state['personal_data']['geslacht']}")
        st.write(f"Opleiding: {st.session_state['personal_data']['opleiding']}")
        st.write(f"Regio: {st.session_state['personal_data']['regio']}")
        st.write(f"Genres: {', '.join(st.session_state['personal_data']['genres'])}")

        # voeg een knop toe om gegevens te bewerken, gaat terug naar de vorige pagina
        if st.button("Bewerk gegevens"):
            st.session_state["personal_data"] = None  
            st.rerun() 

# Boeken zoeken via Google Books API voor zoekresulaten en opslaan gegevens boek
def search_and_extract_books(query):
    # url voor API
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=10"
    response = requests.get(url)
    
    # controleer of API reageert
    if response.status_code != 200:
        return []

    # haal bookinformatie op uit API-respons
    books = response.json().get('items', [])
    book_list = []
    for book in books:
        info = book.get('volumeInfo', {})
        isbn = None 

        # haal isbn op indien beschikbaar (isbn10 == isbn bookcrossing)
        if 'industryIdentifiers' in info:
            for id in info['industryIdentifiers']:
                if id['type'] == 'ISBN_10':
                    isbn = id['identifier']

        # haal thumbnail op indien beschikbaar
        thumbnail = info.get('imageLinks', {}).get('thumbnail', None)
        
    #sommige boeken hebben geen auteurs##############################################################################################TO DO 
        # toon alleen de boeken met thumbnail en isbn
        if thumbnail and isbn:
            book_list.append({'title': info.get('title'), 
                              'authors' : ', '.join(info.get('authors', [])),
                              'thumbnail' : thumbnail,
                              'isbn' : isbn})
    return book_list     

# Vraag leesgeschiedenis op van de gebruiker
def reading_history():
    st.header("Leesgeschiedenis")

    # Minimaal 3 boeken 
    if len(st.session_state["selected_books"]) < 3:
        remaining = 3 - len(st.session_state["selected_books"])
        st.write(f"Kies minimaal **{remaining}** boek{'en' if remaining > 1 else ''} die je hebt gelezen en kunt beoordelen.")
    else:
        st.write(f"Je hebt ***{len(st.session_state['selected_books'])}*** boeken geselecteerd. Je kunt doorgaan of meer boeken toevoegen.")

    # Genereer en toon zoekresultaten 
    search_query = st.text_input("Typ een zoekterm (resultaten worden automatisch bijgewerkt):")

    # Zoekresultaten moeten verdwijnen na kiezen boek ##################################################################### TO DO
    if search_query:
        book_results = search_and_extract_books(search_query)
        if book_results:
            st.write("Zoekresultaten:")
            for book in book_results:
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image(book['thumbnail'], width=80)
                with col2:
                    st.write(f"Titel: {book['title']}")
                    st.write(f"Auteur(s): {book['authors']}")
                    if st.button("Kies boek", key=f"add-{book['isbn']}"):
                        add_book_to_selection(book)
                        st.rerun()
        else:
            st.write("Geen resultaten gevonden voor deze zoekterm.")

# Geselecteerde boeken raten en tonen
def select_and_rate_books():
    st.subheader("Beoordeel de selecteerde boeken:")
    if st.session_state["selected_books"]:
        for i in range(0, len(st.session_state["selected_books"]), 4):  
            cols = st.columns(4)  
            for j, book in enumerate(st.session_state["selected_books"][i:i + 4]):
                with cols[j]:
                    st.markdown(
                        f"""
                        <div style="text-align: center;">
                            <img src="{book['thumbnail']}" style="max-height: 150px; object-fit: cover"/>
                            <div style="height: 44px; overflow: hidden; text-align: center; font-weight: bold; font-size: 14px;">
                                {book['title']}
                            </div>
                            <div style="height: 40px; overflow: hidden; text-align: center; color: gray; font-size: 12px;">
                                {book['authors']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    
                    with st.container():
                        # beoordeel boek 
                        rating = st.feedback("stars", key=f"rating-{book['isbn']}")
                        if rating:
                            book["rating"] = rating

                        # verwijder boek uit selectie 
                        if st.button("Verwijder boek", key=f"remove-{book['isbn']}"):
                            remove_book_from_selection(book)
                            st.rerun()
    else:
        st.write("Je hebt nog geen boeken geselecteerd.")
        
# Profiel en beoordeelde boeken bevestigen en checken
# def confirm_and_check_data():
#     if len(st.session_state['selected_books']) >= 3:
#         st.warning("Controleer profielgegevens en gekozen boeken alvorens te bevestigen. Bewerken is hierna niet meer mogelijk.")
#         bevestig_final = st.button("Bevestig")
    
# # uitleg genereren per aanbeveling
# def generate_uitleg(book, leeftijd, geslacht, opleiding, regio, genres):
#         uitleg = 'uitleg'
#         return uitleg

# Welk "venster" krijgt de gebruiker te zien?
if not st.session_state['privacy_accepted']:
    show_privacy()
elif not st.session_state['personal_data']:
    collect_personal_data()
else:
    show_personal_data()
    reading_history()
    select_and_rate_books()
    # confirm_and_check_data()





