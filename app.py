import streamlit as st
import streamlit.components.v1 as components
import folium
from streamlit_folium import st_folium
import os

st.set_page_config(
    page_title="Catalogue des Aéroports Internationaux",
    page_icon="✈️",
    layout="wide"
)

# -----------------------------
# CSS Design - Thème Aviation
# -----------------------------
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Open+Sans:wght@400;600&display=swap');

    /* Background principal avec motif */
    .stApp {
        background-color: #0a0e1a;
        background-image:
            radial-gradient(circle at 20% 50%, rgba(0, 80, 160, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(0, 150, 255, 0.1) 0%, transparent 40%),
            linear-gradient(180deg, #0a0e1a 0%, #0d1526 100%);
        font-family: 'Open Sans', sans-serif;
    }

    /* Motif grille radar en fond */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image:
            linear-gradient(rgba(0, 120, 255, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 120, 255, 0.04) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1a2e 0%, #0a1220 100%);
        border-right: 1px solid rgba(0, 150, 255, 0.2);
    }
    [data-testid="stSidebar"] * {
        color: #c8d8f0 !important;
    }
    [data-testid="stSidebar"] .stTextInput input {
        background: rgba(0, 80, 160, 0.2) !important;
        border: 1px solid rgba(0, 150, 255, 0.3) !important;
        color: white !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebar"] .stSelectbox select {
        background: rgba(0, 80, 160, 0.2) !important;
        color: white !important;
    }

    /* Titres */
    h1, h2, h3 {
        font-family: 'Rajdhani', sans-serif !important;
        color: #ffffff !important;
        letter-spacing: 1px;
    }
    h1 {
        font-size: 2.4rem !important;
        background: linear-gradient(90deg, #00aaff, #ffffff, #00aaff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none !important;
    }

    /* Texte général */
    p, li, span, label {
        color: #b0c4de !important;
    }

    /* Carte aéroport */
    .airport-card {
        background: linear-gradient(135deg, rgba(13, 30, 60, 0.95) 0%, rgba(10, 20, 45, 0.95) 100%);
        border: 1px solid rgba(0, 150, 255, 0.25);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 100, 255, 0.15), inset 0 1px 0 rgba(255,255,255,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
        position: relative;
        overflow: hidden;
    }
    .airport-card::before {
        content: '✈';
        position: absolute;
        right: 15px;
        top: 10px;
        font-size: 40px;
        opacity: 0.06;
        color: #00aaff;
    }
    .airport-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0, 150, 255, 0.25);
        border-color: rgba(0, 180, 255, 0.5);
    }
    .airport-card h3 {
        color: #e8f4ff !important;
        margin-bottom: 4px;
        font-size: 1.1rem;
    }
    .airport-card p {
        color: #7aadcc !important;
        margin: 0;
        font-size: 0.85rem;
    }

    /* Badge IATA */
    .iata-badge {
        display: inline-block;
        background: linear-gradient(135deg, #0050a0, #0080d0);
        color: white !important;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin-top: 6px;
        border: 1px solid rgba(0, 180, 255, 0.4);
    }

    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #0050a0 0%, #0080d0 100%) !important;
        color: white !important;
        border: 1px solid rgba(0, 180, 255, 0.4) !important;
        border-radius: 10px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        padding: 8px 20px !important;
        transition: all 0.2s !important;
        box-shadow: 0 4px 15px rgba(0, 100, 200, 0.3) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #0070c0 0%, #00a0e0 100%) !important;
        box-shadow: 0 6px 20px rgba(0, 150, 255, 0.5) !important;
        transform: translateY(-1px) !important;
    }

    /* Info box */
    .info-box {
        background: linear-gradient(135deg, rgba(0, 50, 100, 0.6), rgba(0, 30, 70, 0.6));
        border: 1px solid rgba(0, 150, 255, 0.3);
        border-left: 4px solid #0080d0;
        border-radius: 12px;
        padding: 16px 20px;
        margin: 10px 0;
    }
    .info-box p {
        color: #c0d8f0 !important;
        margin: 4px 0;
        font-size: 0.95rem;
    }
    .info-box strong {
        color: #60b8ff !important;
    }

    /* Schéma aéroport */
    .schema-box {
        background: linear-gradient(135deg, rgba(0, 20, 50, 0.9), rgba(0, 10, 30, 0.9));
        border: 1px solid rgba(0, 150, 255, 0.2);
        border-radius: 16px;
        padding: 24px;
        font-family: monospace;
        color: #00ccff !important;
    }
    .schema-box pre {
        color: #00ccff !important;
        font-size: 14px;
        line-height: 1.8;
    }

    /* Feature tags */
    .feature-tag {
        display: inline-block;
        background: rgba(0, 80, 160, 0.3);
        border: 1px solid rgba(0, 150, 255, 0.3);
        color: #80c8ff !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        margin: 3px;
    }

    /* Séparateur */
    hr {
        border-color: rgba(0, 150, 255, 0.2) !important;
    }

    /* Images arrondies */
    [data-testid="stImage"] img {
        border-radius: 14px !important;
        border: 1px solid rgba(0, 150, 255, 0.2) !important;
        box-shadow: 0 4px 20px rgba(0, 80, 200, 0.3) !important;
    }

    /* Metric */
    [data-testid="stMetric"] {
        background: rgba(0, 50, 100, 0.3);
        border: 1px solid rgba(0, 150, 255, 0.2);
        border-radius: 12px;
        padding: 12px;
    }
    [data-testid="stMetricLabel"] {
        color: #60a8d0 !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    /* Titre sidebar */
    [data-testid="stSidebar"] h1 {
        background: linear-gradient(90deg, #00aaff, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.4rem !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a0e1a; }
    ::-webkit-scrollbar-thumb { background: #0050a0; border-radius: 3px; }

    /* Boutons rouges intro */
    #btn_intro1 + div button, #btn_intro2 + div button,
    span#btn_intro1 ~ div button, span#btn_intro2 ~ div button {
        background-color: #cc0000 !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }

    /* Boutons jaunes navigation */
    span#btn_avions ~ div button,
    span#btn_retour_cat1 ~ div button,
    span#btn_retour_cat2 ~ div button,
    span#btn_retour_fiche ~ div button {
        background-color: #e6a800 !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Données des aéroports avec images locales
# -----------------------------
AIRPORTS = [
    {
        "id": "dubai",
        "name": "Aéroport International de Dubaï",
        "country": "Émirats arabes unis",
        "city": "Dubaï",
        "type": "International",
        "image_local": "images/Dubai_Airport.webp",
        "image_fallback": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Dubai_International_Airport.jpg/1280px-Dubai_International_Airport.jpg",
        "video_url": "https://www.youtube.com/embed/m8n2o3Qx504",
        "lat": 25.2532,
        "lon": 55.3657,
        "description": "L'aéroport international de Dubaï est l'un des plus grands hubs aériens au monde. Il est connu pour son trafic international massif et pour être une base majeure d'Emirates.",
        "iata": "DXB",
        "icao": "OMDB",
        "terminals": 3,
        "runways": 2,
        "passengers": "86+ millions/an",
        "airlines": ["Emirates", "Flydubai", "Qantas", "British Airways"],
        "aircraft": ["Airbus A380", "Boeing 777", "Boeing 737", "Airbus A350"],
        "features": ["Hub mondial du trafic international", "Zones duty free très développées", "Base principale d'Emirates", "Infrastructure moderne"]
    },
    {
        "id": "doha",
        "name": "Aéroport International Hamad",
        "country": "Qatar",
        "city": "Doha",
        "type": "International",
        "image_local": "images/hamad.airport.webp",
        "image_fallback": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Hamad_International_Airport%2C_Doha%2C_Qatar.jpg/1280px-Hamad_International_Airport%2C_Doha%2C_Qatar.jpg",
        "video_url": "https://www.youtube.com/embed/NyD_G2_gDp8",
        "lat": 25.2731,
        "lon": 51.6081,
        "description": "L'aéroport international Hamad à Doha est l'un des aéroports les plus modernes du Moyen-Orient. Il est le principal hub de Qatar Airways.",
        "iata": "DOH",
        "icao": "OTHH",
        "terminals": 1,
        "runways": 2,
        "passengers": "45+ millions/an",
        "airlines": ["Qatar Airways", "Turkish Airlines", "Lufthansa", "Oman Air"],
        "aircraft": ["Boeing 777", "Airbus A350", "Airbus A320", "Boeing 787"],
        "features": ["Hub principal de Qatar Airways", "Design architectural haut de gamme", "Services premium pour transit", "Technologies avancées"]
    },
    {
        "id": "casablanca",
        "name": "Aéroport Mohammed V",
        "country": "Maroc",
        "city": "Casablanca",
        "type": "International",
        "image_local": "images/aeroport-Mohammed-V-de-Casablanca.png",
        "image_fallback": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Casablanca_Airport_Mohammed_V.jpg/1280px-Casablanca_Airport_Mohammed_V.jpg",
        "video_url": "https://www.youtube.com/embed/fycFuj4AGaw",
        "lat": 33.3675,
        "lon": -7.5898,
        "description": "L'aéroport Mohammed V est le plus important aéroport du Maroc. Il constitue une porte d'entrée majeure du pays et un hub clé pour Royal Air Maroc.",
        "iata": "CMN",
        "icao": "GMMN",
        "terminals": 2,
        "runways": 2,
        "passengers": "10+ millions/an",
        "airlines": ["Royal Air Maroc", "Air France", "Iberia", "Turkish Airlines"],
        "aircraft": ["Boeing 737", "Boeing 787", "ATR 72", "Airbus A320"],
        "features": ["Premier aéroport du Maroc", "Hub de Royal Air Maroc", "Connexion Afrique-Europe", "Services nationaux et internationaux"]
    },
    {
        "id": "marrakech",
        "name": "Aéroport Marrakech-Ménara",
        "country": "Maroc",
        "city": "Marrakech",
        "type": "International",
        "image_local": "images/Aeroport-Marrakech.webp",
        "image_fallback": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Marrakesh_Menara_Airport.jpg/1280px-Marrakesh_Menara_Airport.jpg",
        "video_url": "https://www.youtube.com/embed/K9bbhLfyaAs",
        "lat": 31.6069,
        "lon": -8.0363,
        "description": "L'aéroport Marrakech-Ménara dessert une destination touristique majeure. Il combine architecture marocaine et trafic international important.",
        "iata": "RAK",
        "icao": "GMMX",
        "terminals": 1,
        "runways": 1,
        "passengers": "6+ millions/an",
        "airlines": ["Ryanair", "easyJet", "Royal Air Maroc", "Transavia"],
        "aircraft": ["Boeing 737", "Airbus A320", "Airbus A321"],
        "features": ["Aéroport touristique stratégique", "Architecture élégante", "Fort trafic européen", "Accès direct à Marrakech"]
    },
    {
        "id": "paris",
        "name": "Aéroport Paris-Charles de Gaulle",
        "country": "France",
        "city": "Paris",
        "type": "International",
        "image_local": "images/aeroport-paris.webp",
        "image_fallback": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Paris_Charles_de_Gaulle_Airport.jpg/1280px-Paris_Charles_de_Gaulle_Airport.jpg",
        "video_url": "https://www.youtube.com/embed/vNZ9Ex8oDjo",
        "lat": 49.0097,
        "lon": 2.5479,
        "description": "Paris-CDG est un hub européen majeur et l'aéroport principal de la France pour le trafic international.",
        "iata": "CDG",
        "icao": "LFPG",
        "terminals": 3,
        "runways": 4,
        "passengers": "65+ millions/an",
        "airlines": ["Air France", "KLM", "Delta", "Lufthansa"],
        "aircraft": ["Airbus A320", "Boeing 777", "Airbus A350", "Boeing 787"],
        "features": ["Hub européen majeur", "Base d'Air France", "Trafic intercontinental dense", "Multiples terminaux"]
    },
    {
        "id": "istanbul",
        "name": "Aéroport d'Istanbul",
        "country": "Turquie",
        "city": "Istanbul",
        "type": "International",
        "image_local": "images/istanbuler.webp",
        "image_fallback": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Istanbul_Airport_Terminal.jpg/1280px-Istanbul_Airport_Terminal.jpg",
        "video_url": "https://www.youtube.com/embed/m-_-qa7DtW4",
        "lat": 41.2753,
        "lon": 28.7519,
        "description": "L'aéroport d'Istanbul est un immense hub reliant l'Europe, l'Asie et l'Afrique. Il est central pour Turkish Airlines.",
        "iata": "IST",
        "icao": "LTFM",
        "terminals": 1,
        "runways": 5,
        "passengers": "70+ millions/an",
        "airlines": ["Turkish Airlines", "Pegasus", "Qatar Airways", "Emirates"],
        "aircraft": ["Airbus A321", "Boeing 777", "Airbus A330", "Boeing 737"],
        "features": ["Hub intercontinental", "Grande capacité", "Infrastructure récente", "Connectivité mondiale"]
    },
    {
        "id": "heathrow",
        "name": "Aéroport de Londres Heathrow",
        "country": "Royaume-Uni",
        "city": "Londres",
        "type": "International",
        "image_local": "images/londre.jpg",
        "image_fallback": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Heathrow_Airport.jpg/1280px-Heathrow_Airport.jpg",
        "video_url": "https://www.youtube.com/embed/fu3p6S8Bjxs",
        "lat": 51.4700,
        "lon": -0.4543,
        "description": "Heathrow est le principal aéroport du Royaume-Uni et un des plus importants hubs internationaux du monde.",
        "iata": "LHR",
        "icao": "EGLL",
        "terminals": 4,
        "runways": 2,
        "passengers": "79+ millions/an",
        "airlines": ["British Airways", "Virgin Atlantic", "Lufthansa", "American Airlines"],
        "aircraft": ["Boeing 777", "Airbus A380", "Airbus A320", "Boeing 787"],
        "features": ["Hub majeur du Royaume-Uni", "Trafic international très dense", "Base importante de British Airways", "Services premium"]
    },
    {
        "id": "frankfurt",
        "name": "Aéroport de Francfort",
        "country": "Allemagne",
        "city": "Francfort",
        "type": "International",
        "image_local": "images/MG_21_0703.jpg",
        "image_fallback": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Frankfurt_Airport_Aerial_View.jpg/1280px-Frankfurt_Airport_Aerial_View.jpg",
        "video_url": "https://www.youtube.com/embed/FpvVDZcpeAQ",
        "lat": 50.0379,
        "lon": 8.5622,
        "iata": "FRA",
        "icao": "EDDF",
        "terminals": 2,
        "runways": 4,
        "passengers": "57+ millions/an",
        "airlines": ["Lufthansa", "Condor", "Ryanair", "United Airlines"],
        "aircraft": ["Airbus A380", "Boeing 747", "Airbus A320", "Boeing 777"],
        "features": ["Hub principal de Lufthansa", "Plus grand aéroport d'Allemagne", "Connexion Europe-Monde", "Cargo majeur"],
        "description": "L'aéroport de Francfort est le plus grand aéroport d'Allemagne et le hub principal de Lufthansa. Il est l'un des aéroports les plus fréquentés d'Europe avec un trafic cargo très important."
    },
    {
        "id": "amsterdam",
        "name": "Aéroport d'Amsterdam Schiphol",
        "country": "Pays-Bas",
        "city": "Amsterdam",
        "type": "International",
        "image_local": "images/amsterdam.webp",
        "image_fallback": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Schiphol_airport_2019.jpg/1280px-Schiphol_airport_2019.jpg",
        "video_url": "https://www.youtube.com/embed/qG44ddJa6po",
        "lat": 52.3105,
        "lon": 4.7683,
        "iata": "AMS",
        "icao": "EHAM",
        "terminals": 1,
        "runways": 6,
        "passengers": "71+ millions/an",
        "airlines": ["KLM", "Transavia", "EasyJet", "Delta"],
        "aircraft": ["Boeing 777", "Airbus A330", "Boeing 737", "Airbus A320"],
        "features": ["Hub de KLM", "Terminal unique très moderne", "6 pistes opérationnelles", "Connexion Europe-Amériques"],
        "description": "L'aéroport d'Amsterdam Schiphol est le principal aéroport des Pays-Bas et le hub de KLM. Avec un terminal unique et 6 pistes, il est l'un des aéroports les mieux organisés d'Europe."
    },
    {
        "id": "newyork",
        "name": "Aéroport JFK de New York",
        "country": "États-Unis",
        "city": "New York",
        "type": "International",
        "image_local": "images/new yor.jfif",
        "image_fallback": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/JFK_Airport_Aerial_2019.jpg/1280px-JFK_Airport_Aerial_2019.jpg",
        "video_url": "https://www.youtube.com/embed/tx2p2tNp8ME",
        "lat": 40.6413,
        "lon": -73.7781,
        "iata": "JFK",
        "icao": "KJFK",
        "terminals": 6,
        "runways": 4,
        "passengers": "62+ millions/an",
        "airlines": ["American Airlines", "Delta", "JetBlue", "Emirates"],
        "aircraft": ["Boeing 777", "Airbus A380", "Boeing 767", "Airbus A321"],
        "features": ["Porte d'entrée des États-Unis", "Hub international majeur", "6 terminaux indépendants", "Trafic transatlantique dense"],
        "description": "L'aéroport JFK de New York est la principale porte d'entrée internationale des États-Unis. Avec 6 terminaux et un trafic transatlantique massif, il est l'un des aéroports les plus importants du monde."
    },
    {
        "id": "singapore",
        "name": "Aéroport de Singapour Changi",
        "country": "Singapour",
        "city": "Singapour",
        "type": "International",
        "image_local": "images/Aeroport-Singapour.jpg.webp",
        "image_fallback": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/thirty/Changi_Airport_Singapore.jpg/1280px-Changi_Airport_Singapore.jpg",
        "video_url": "https://www.youtube.com/embed/5HVA7S2jcME",
        "lat": 1.3644,
        "lon": 103.9915,
        "iata": "SIN",
        "icao": "WSSS",
        "terminals": 4,
        "runways": 2,
        "passengers": "68+ millions/an",
        "airlines": ["Singapore Airlines", "Scoot", "Cathay Pacific", "Emirates"],
        "aircraft": ["Airbus A380", "Boeing 777", "Airbus A350", "Boeing 787"],
        "features": ["Élu meilleur aéroport du monde", "Jewel Changi intégré", "Jardins et cascades intérieurs", "Hub Asie-Pacifique"],
        "description": "L'aéroport de Singapour Changi est régulièrement élu meilleur aéroport du monde. Il abrite le Jewel Changi, un complexe avec jardins tropicaux et la plus grande cascade intérieure du monde."
    },
    {
        "id": "tokyo",
        "name": "Aéroport International de Tokyo Haneda",
        "country": "Japon",
        "city": "Tokyo",
        "type": "International",
        "image_local": "images/Tokyo-2.jpg",
        "image_fallback": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Haneda_Airport_Aerial_2020.jpg/1280px-Haneda_Airport_Aerial_2020.jpg",
        "video_url": "https://www.youtube.com/embed/2ctgeiayE8k",
        "lat": 35.5494,
        "lon": 139.7798,
        "iata": "HND",
        "icao": "RJTT",
        "terminals": 3,
        "runways": 4,
        "passengers": "85+ millions/an",
        "airlines": ["Japan Airlines", "ANA", "Delta", "Air France"],
        "aircraft": ["Boeing 777", "Boeing 787", "Airbus A350", "Boeing 737"],
        "features": ["Plus grand aéroport du Japon", "Ponctualité exemplaire", "Services haut de gamme", "Hub Asie-Pacifique"],
        "description": "L'aéroport de Tokyo Haneda est le plus grand aéroport du Japon et l'un des plus ponctuels au monde. Il est le hub principal de Japan Airlines et ANA avec des connexions vers toute l'Asie et le monde."
    }
]


# -----------------------------
# Helpers
# -----------------------------
def get_image(airport):
    """Retourne l'image locale si elle existe, sinon l'URL de fallback."""
    if os.path.exists(airport["image_local"]):
        return airport["image_local"]
    return airport["image_fallback"]

def find_airport_by_id(airport_id):
    for airport in AIRPORTS:
        if airport["id"] == airport_id:
            return airport
    return None

def airport_card(airport):
    st.markdown(f"""
    <div class="airport-card">
        <h3>{airport['name']}</h3>
        <p>📍 {airport['city']} &nbsp;•&nbsp; {airport['country']}</p>
        <span class="iata-badge">{airport['iata']}</span>
    </div>
    """, unsafe_allow_html=True)

def draw_airport_schema(airport=None):
    terminals = airport["terminals"] if airport else 1
    runways = airport["runways"] if airport else 2
    name = airport["name"] if airport else "Aéroport"
    st.markdown("### 🗺️ Schéma de l'aéroport")

    # Générer les pistes dynamiquement
    runway_svgs = ""
    runway_spacing = 280 // max(runways, 1)
    total_height = 100 + runways * 80 + 60

    for i in range(runways):
        y = 40 + i * (total_height - 80) // max(runways - 1, 1) if runways > 1 else total_height // 2 - 20
        runway_svgs += f"""
        <rect x="20" y="{y}" width="760" height="32" rx="4" fill="#0d1f3c" stroke="#00aaff" stroke-width="1.5"/>
        <text x="400" y="{y+21}" text-anchor="middle" fill="#00ccff" font-size="12" font-family="Arial" font-weight="bold">PISTE 0{i+1}</text>
        <line x1="50" y1="{y+16}" x2="750" y2="{y+16}" stroke="rgba(255,255,255,0.12)" stroke-width="1" stroke-dasharray="20,15"/>
        """

    # Terminaux dynamiques
    terminal_svgs = ""
    t_width = min(200, 600 // terminals)
    t_start = 400 - (terminals * (t_width + 10)) // 2
    for i in range(terminals):
        tx = t_start + i * (t_width + 10)
        terminal_svgs += f"""
        <rect x="{tx}" y="130" width="{t_width}" height="80" rx="6" fill="#0a2a5e" stroke="#00aaff" stroke-width="1.5"/>
        <text x="{tx + t_width//2}" y="168" text-anchor="middle" fill="#ffffff" font-size="11" font-family="Arial" font-weight="bold">T{i+1}</text>
        <text x="{tx + t_width//2}" y="184" text-anchor="middle" fill="#80c8ff" font-size="9" font-family="Arial">Terminal {i+1}</text>
        """
        # Passerelles sous chaque terminal
        for j in range(3):
            px = tx + 15 + j * (t_width // 3)
            terminal_svgs += f'<rect x="{px}" y="210" width="10" height="12" fill="#0060a0" stroke="#00aaff" stroke-width="1"/>'
            terminal_svgs += f'<text x="{px+5}" y="222" text-anchor="middle" fill="#00ffcc" font-size="12">✈</text>'

    components.html(f"""
    <div style="background:linear-gradient(135deg, rgba(0,20,50,0.9), rgba(0,10,30,0.9)); border:1px solid rgba(0,150,255,0.2); border-radius:16px; padding:24px; text-align:center;">
        <svg viewBox="0 0 800 350" xmlns="http://www.w3.org/2000/svg" style="width:100%; max-width:750px;">
            {runway_svgs}
            <rect x="20" y="110" width="760" height="10" rx="2" fill="#071428" stroke="#0060a0" stroke-width="1"/>
            <text x="22" y="108" fill="#406080" font-size="9" font-family="Arial">TAXIWAY A</text>
            <rect x="20" y="235" width="760" height="10" rx="2" fill="#071428" stroke="#0060a0" stroke-width="1"/>
            <text x="22" y="233" fill="#406080" font-size="9" font-family="Arial">TAXIWAY B</text>
            {terminal_svgs}
            <rect x="30" y="130" width="90" height="80" rx="5" fill="#071428" stroke="#0060a0" stroke-width="1.2"/>
            <text x="75" y="168" text-anchor="middle" fill="#60a8d0" font-size="10" font-family="Arial">PARKING</text>
            <rect x="680" y="130" width="90" height="80" rx="5" fill="#071428" stroke="#0060a0" stroke-width="1.2"/>
            <text x="725" y="168" text-anchor="middle" fill="#60a8d0" font-size="10" font-family="Arial">PARKING</text>
            <line x1="400" y1="280" x2="400" y2="320" stroke="#0060a0" stroke-width="2" stroke-dasharray="5,4"/>
            <rect x="365" y="320" width="70" height="22" rx="3" fill="#071428" stroke="#0060a0" stroke-width="1"/>
            <text x="400" y="335" text-anchor="middle" fill="#60a8d0" font-size="10" font-family="Arial">ACCES</text>
            <text x="400" y="15" text-anchor="middle" fill="#60b8ff" font-size="11" font-family="Arial">{runways} piste(s) - {terminals} terminal(aux)</text>
        </svg>
    </div>
    """, height=380)

def draw_aircraft_schema():
    st.markdown("### ✈️ Schéma d'un avion")
    components.html("""
    <div style="background:linear-gradient(135deg, rgba(0,20,50,0.9), rgba(0,10,30,0.9)); border:1px solid rgba(0,150,255,0.2); border-radius:16px; padding:24px; text-align:center;">
        <svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg" style="width:100%; max-width:750px;">
            <ellipse cx="400" cy="150" rx="280" ry="38" fill="#0a2a5e" stroke="#00aaff" stroke-width="2"/>
            <path d="M680,150 Q740,150 760,150 Q740,138 680,132 Z" fill="#0d3a7a" stroke="#00aaff" stroke-width="1.5"/>
            <path d="M120,150 Q100,150 90,150 Q100,140 120,136 Z" fill="#0d3a7a" stroke="#00aaff" stroke-width="1.5"/>
            <path d="M380,155 L280,240 L320,242 L430,160 Z" fill="#0d3a7a" stroke="#00aaff" stroke-width="1.5"/>
            <path d="M380,145 L280,60 L320,58 L430,140 Z" fill="#0d3a7a" stroke="#00aaff" stroke-width="1.5"/>
            <path d="M140,148 L130,90 L160,95 L165,148 Z" fill="#0d3a7a" stroke="#00aaff" stroke-width="1.5"/>
            <path d="M155,152 L110,185 L130,186 L168,156 Z" fill="#0d3a7a" stroke="#00aaff" stroke-width="1.5"/>
            <path d="M155,148 L110,115 L130,114 L168,144 Z" fill="#0d3a7a" stroke="#00aaff" stroke-width="1.5"/>
            <ellipse cx="360" cy="210" rx="45" ry="14" fill="#051a3a" stroke="#0080d0" stroke-width="1.5"/>
            <ellipse cx="405" cy="210" rx="8" ry="14" fill="#0a2a5e" stroke="#0080d0" stroke-width="1"/>
            <ellipse cx="360" cy="90" rx="45" ry="14" fill="#051a3a" stroke="#0080d0" stroke-width="1.5"/>
            <ellipse cx="405" cy="90" rx="8" ry="14" fill="#0a2a5e" stroke="#0080d0" stroke-width="1"/>
            <circle cx="580" cy="145" r="7" fill="#001a3a" stroke="#00ccff" stroke-width="1.5"/>
            <circle cx="555" cy="145" r="7" fill="#001a3a" stroke="#00ccff" stroke-width="1.5"/>
            <circle cx="530" cy="145" r="7" fill="#001a3a" stroke="#00ccff" stroke-width="1.5"/>
            <circle cx="505" cy="145" r="7" fill="#001a3a" stroke="#00ccff" stroke-width="1.5"/>
            <circle cx="480" cy="145" r="7" fill="#001a3a" stroke="#00ccff" stroke-width="1.5"/>
            <circle cx="455" cy="145" r="7" fill="#001a3a" stroke="#00ccff" stroke-width="1.5"/>
            <circle cx="430" cy="146" r="7" fill="#001a3a" stroke="#00ccff" stroke-width="1.5"/>
            <circle cx="405" cy="147" r="7" fill="#001a3a" stroke="#00ccff" stroke-width="1.5"/>
            <circle cx="380" cy="148" r="7" fill="#001a3a" stroke="#00ccff" stroke-width="1.5"/>
            <circle cx="355" cy="148" r="7" fill="#001a3a" stroke="#00ccff" stroke-width="1.5"/>
            <circle cx="330" cy="148" r="7" fill="#001a3a" stroke="#00ccff" stroke-width="1.5"/>
            <circle cx="305" cy="148" r="7" fill="#001a3a" stroke="#00ccff" stroke-width="1.5"/>
            <circle cx="280" cy="148" r="7" fill="#001a3a" stroke="#00ccff" stroke-width="1.5"/>
            <line x1="120" y1="150" x2="680" y2="150" stroke="rgba(0,180,255,0.15)" stroke-width="1" stroke-dasharray="6,4"/>
            <text x="400" y="275" text-anchor="middle" fill="#60b8ff" font-size="12" font-family="Arial">FUSELAGE</text>
            <text x="300" y="258" text-anchor="middle" fill="#60b8ff" font-size="11" font-family="Arial">AILE</text>
            <text x="370" y="232" text-anchor="middle" fill="#60b8ff" font-size="10" font-family="Arial">REACTEUR</text>
            <text x="140" y="80" text-anchor="middle" fill="#60b8ff" font-size="10" font-family="Arial">EMPENNAGE</text>
            <text x="590" y="130" text-anchor="middle" fill="#60b8ff" font-size="10" font-family="Arial">HUBLOTS</text>
        </svg>
    </div>
    """, height=320)

def render_features(features):
    tags = "".join([f'<span class="feature-tag">✓ {f}</span>' for f in features])
    st.markdown(f'<div style="margin: 10px 0;">{tags}</div>', unsafe_allow_html=True)

# -----------------------------
# Session state
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "intro1"
if "selected_airport" not in st.session_state:
    st.session_state.selected_airport = None

# -----------------------------
# Sidebar
# -----------------------------
# Sidebar — masquée sur les pages d'intro
search = ""
country_filter = "Tous"
type_filter = "Tous"
if st.session_state.page in ("intro1", "intro2"):
    st.markdown("<style>[data-testid='stSidebar']{display:none}</style>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("## ✈️ Navigation")
    search = st.sidebar.text_input("🔍 Rechercher un aéroport")
    country_filter = st.sidebar.selectbox(
        "🌍 Filtrer par pays",
        ["Tous"] + sorted(list(set(a["country"] for a in AIRPORTS)))
    )
    type_filter = st.sidebar.selectbox("🏷️ Type", ["Tous", "National", "International"])
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
<div style="background:rgba(0,80,160,0.2); border:1px solid rgba(0,150,255,0.2); border-radius:10px; padding:12px; font-size:0.82rem; color:#80b8d8 !important;">
    ✈️ Catalogue mondial des aéroports<br>
    Explorez les plus grands hubs aériens internationaux.
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Page Intro 1 — Bienvenue
# -----------------------------
if st.session_state.page == "intro1":
    st.markdown("""
    <style>
        .stApp { background: linear-gradient(135deg, #0a1a6e 0%, #0d2080 100%) !important; }
        .stApp::before { display: none; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; color:white; font-size:3rem; letter-spacing:2px;'>✈️ Bienvenue sur ce site</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#a0c4ff; font-size:1.2rem;'>Découvrez le catalogue des plus grands aéroports internationaux du monde.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.image("images/emirates.jpg", use_container_width=True)
        st.markdown("<p style='text-align:center; color:#a0c4ff;'>Emirates</p>", unsafe_allow_html=True)
    with c2:
        st.image("images/Air-France.jpg", use_container_width=True)
        st.markdown("<p style='text-align:center; color:#a0c4ff;'>Air France</p>", unsafe_allow_html=True)
    with c3:
        st.image("images/royal-air-maroc.jpg", use_container_width=True)
        st.markdown("<p style='text-align:center; color:#a0c4ff;'>Royal Air Maroc</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.markdown("""
        <style>
        #btn_intro1 ~ div button, div:has(> #btn_intro1) button {
            background-color: #cc0000 !important;
            color: white !important;
            border: none !important;
            font-size: 1.1rem !important;
            font-weight: bold !important;
            border-radius: 10px !important;
            padding: 12px 40px !important;
        }
        </style>
        <span id="btn_intro1"></span>
        """, unsafe_allow_html=True)
        if st.button("Suivant →", key="btn_intro1"):
            st.session_state.page = "intro2"
            st.rerun()

# -----------------------------
# Page Intro 2 — Présentation
# -----------------------------
elif st.session_state.page == "intro2":
    st.markdown("""
    <style>
        .stApp { background: #0a1a6e !important; }
        .stApp::before { display: none; }
    </style>
    """, unsafe_allow_html=True)
    components.html("""
    <div style="
        min-height: 90vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #0a1a6e 0%, #0d2080 100%);
        font-family: 'Arial', sans-serif;
        text-align: center;
        padding: 60px 40px;
    ">
        <div style="font-size: 70px; margin-bottom: 30px;">🌍</div>
        <h1 style="color: white; font-size: 2.5rem; margin-bottom: 24px; letter-spacing: 1px;">
            Sur ce site web
        </h1>
        <p style="color: #a0c4ff; font-size: 1.25rem; max-width: 650px; line-height: 1.9;">
            Vous allez rencontrer <strong style="color:white;">plein d'aéroports</strong> et toutes leurs informations :
            vidéos, cartes interactives, terminaux, compagnies aériennes, avions et bien plus encore.
        </p>
        <div style="margin-top: 30px; display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
            <span style="background:rgba(255,255,255,0.1); color:#a0c4ff; padding:10px 20px; border-radius:20px; font-size:1rem;">📍 Localisation GPS</span>
            <span style="background:rgba(255,255,255,0.1); color:#a0c4ff; padding:10px 20px; border-radius:20px; font-size:1rem;">🎬 Vidéos</span>
            <span style="background:rgba(255,255,255,0.1); color:#a0c4ff; padding:10px 20px; border-radius:20px; font-size:1rem;">✈️ Avions & Compagnies</span>
            <span style="background:rgba(255,255,255,0.1); color:#a0c4ff; padding:10px 20px; border-radius:20px; font-size:1rem;">🗺️ Plans détaillés</span>
        </div>
    </div>
    """, height=550)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.markdown("""
        <span id="btn_intro2"></span>
        """, unsafe_allow_html=True)
        if st.button("Suivant →", key="btn_intro2"):
            st.session_state.page = "home"
            st.rerun()

# -----------------------------
# Page Accueil
# -----------------------------
elif st.session_state.page == "home":
    st.markdown("# ✈️ Catalogue des Aéroports Internationaux")
    st.markdown('<p style="color:#7aadcc; font-size:1.05rem; margin-bottom:30px;">Explorez les plus grands hubs aériens du monde — cliquez sur un aéroport pour sa fiche complète.</p>', unsafe_allow_html=True)

    filtered_airports = []
    for airport in AIRPORTS:
        if search and search.lower() not in airport["name"].lower() and search.lower() not in airport["city"].lower():
            continue
        if country_filter != "Tous" and airport["country"] != country_filter:
            continue
        if type_filter != "Tous" and airport["type"] != type_filter:
            continue
        filtered_airports.append(airport)

    cols = st.columns(2)
    for i, airport in enumerate(filtered_airports):
        with cols[i % 2]:
            st.image(get_image(airport), use_container_width=True)
            airport_card(airport)
            if st.button(f"Voir {airport['name']}", key=f"btn_{airport['id']}"):
                st.session_state.selected_airport = airport["id"]
                st.session_state.page = "airport"
                st.rerun()

# -----------------------------
# Page Aéroport
# -----------------------------
elif st.session_state.page == "airport":
    airport = find_airport_by_id(st.session_state.selected_airport)

    if airport is None:
        st.error("Aéroport introuvable.")
    else:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"# ✈️ {airport['name']}")
            st.components.v1.iframe(airport["video_url"], height=380)
        with col2:
            st.markdown("### 📋 Informations")
            st.markdown(f"""
            <div class="info-box">
                <p><strong>📍 Ville :</strong> {airport['city']}</p>
                <p><strong>🌍 Pays :</strong> {airport['country']}</p>
                <p><strong>🏷️ Type :</strong> {airport['type']}</p>
                <p><strong>🔤 IATA :</strong> {airport['iata']}</p>
                <p><strong>🔤 ICAO :</strong> {airport['icao']}</p>
                <p><strong>🏢 Terminaux :</strong> {airport['terminals']}</p>
                <p><strong>🛬 Pistes :</strong> {airport['runways']}</p>
                <p><strong>👥 Passagers :</strong> {airport['passengers']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📖 Description")
        st.markdown(f'<p style="color:#b0c8e8; font-size:1rem; line-height:1.7;">{airport["description"]}</p>', unsafe_allow_html=True)

        st.markdown("### ⭐ Caractéristiques")
        render_features(airport["features"])

        # Carte de localisation
        st.markdown("### 🗺️ Localisation & Plan de l'aéroport")
        st.markdown(f"""
        <div class="info-box">
            <p><strong>📍 Coordonnées :</strong> {airport['lat']}° N, {airport['lon']}° E</p>
        </div>
        """, unsafe_allow_html=True)
        m = folium.Map(location=[airport["lat"], airport["lon"]], zoom_start=15)
        # Couche satellite avec détails (terminaux, parkings visibles)
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri",
            name="Satellite",
            overlay=False,
            control=True
        ).add_to(m)
        # Couche OpenStreetMap par dessus pour les labels
        folium.TileLayer(
            tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            attr="OpenStreetMap",
            name="Plan OSM",
            overlay=False,
            control=True
        ).add_to(m)
        folium.Marker(
            [airport["lat"], airport["lon"]],
            popup=folium.Popup(f"<b>✈ {airport['name']}</b><br>IATA: {airport['iata']}<br>📍 {airport['city']}, {airport['country']}", max_width=200),
            tooltip=f"✈ {airport['name']}",
            icon=folium.Icon(color="blue", icon="plane", prefix="fa")
        ).add_to(m)
        folium.LayerControl().add_to(m)
        st_folium(m, width=None, height=500, use_container_width=True)

        draw_airport_schema(airport)

        st.markdown("### 🛫 Compagnies présentes")
        airlines_html = "".join([f'<span class="feature-tag">🛫 {a}</span>' for a in airport["airlines"]])
        st.markdown(f'<div style="margin:10px 0;">{airlines_html}</div>', unsafe_allow_html=True)

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<span id="btn_avions"></span>', unsafe_allow_html=True)
            if st.button("✈️ Voir les avions utilisés", key="btn_voir_avions"):
                st.session_state.page = "aircraft"
                st.rerun()
        with c2:
            st.markdown('<span id="btn_retour_cat1"></span>', unsafe_allow_html=True)
            if st.button("🏠 Retour au catalogue", key="btn_retour_cat1"):
                st.session_state.page = "home"
                st.rerun()

# -----------------------------
# Page Avions
# -----------------------------
elif st.session_state.page == "aircraft":
    airport = find_airport_by_id(st.session_state.selected_airport)

    if airport is None:
        st.error("Aéroport introuvable.")
    else:
        st.markdown(f"# ✈️ Avions à {airport['name']}")
        st.components.v1.iframe(airport["video_url"], height=380)

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🛩️ Appareils utilisés")
            for plane in airport["aircraft"]:
                st.markdown(f'<span class="feature-tag">✈ {plane}</span>', unsafe_allow_html=True)
        with col2:
            st.markdown("### 🛫 Compagnies exploitantes")
            for airline in airport["airlines"]:
                st.markdown(f'<span class="feature-tag">🏢 {airline}</span>', unsafe_allow_html=True)

        draw_aircraft_schema()

        st.markdown("""
        <div class="info-box">
            <p>Les appareils affichés représentent les types fréquemment observés ou associés aux compagnies exploitant cet aéroport.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<span id="btn_retour_fiche"></span>', unsafe_allow_html=True)
            if st.button("📋 Retour à la fiche aéroport", key="btn_retour_fiche"):
                st.session_state.page = "airport"
                st.rerun()
        with c2:
            st.markdown('<span id="btn_retour_cat2"></span>', unsafe_allow_html=True)
            if st.button("🏠 Retour au catalogue", key="btn_retour_cat2"):
                st.session_state.page = "home"
                st.rerun()
