import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster


# ============================================================
# 1. DONNEES
# ============================================================

donnees = pd.DataFrame({
    "nom": [
        "Jardin du Luxembourg",
        "Parc des Buttes-Chaumont",
        "Jardin des Tuileries",
        "Champ de Mars",
        "Parc Monceau",
        "Bois de Vincennes",
        "Bois de Boulogne",
        "Parc de la Villette",
        "Parc Montsouris",
        "Parc André-Citroën"
    ],

    "latitude": [
        48.8462,
        48.8809,
        48.8634,
        48.8556,
        48.8799,
        48.8331,
        48.8637,
        48.8937,
        48.8214,
        48.8414
    ],

    "longitude": [
        2.3372,
        2.3828,
        2.3275,
        2.2986,
        2.3098,
        2.4330,
        2.2530,
        2.3937,
        2.3389,
        2.2759
    ],

    "type": [
        "Jardin",
        "Parc",
        "Jardin",
        "Espace vert",
        "Parc",
        "Bois",
        "Bois",
        "Parc",
        "Parc",
        "Parc"
    ]
})


# ============================================================
# 2. ANALYSE DES DONNEES
# ============================================================

nombre_total = len(donnees)

nombre_par_type = donnees["type"].value_counts()


# ============================================================
# 3. GEODATAFRAME
# ============================================================

gdf = gpd.GeoDataFrame(
    donnees,
    geometry=gpd.points_from_xy(
        donnees["longitude"],
        donnees["latitude"]
    ),
    crs="EPSG:4326"
)


# ============================================================
# 4. CARTE
# ============================================================

carte = folium.Map(
    location=[48.8566, 2.3522],
    zoom_start=12,
    tiles="OpenStreetMap"
)


# ============================================================
# 5. GROUPES
# ============================================================

parcs = folium.FeatureGroup(
    name="🌳 Parcs"
)

jardins = folium.FeatureGroup(
    name="🌷 Jardins"
)

bois = folium.FeatureGroup(
    name="🌲 Bois"
)

autres = folium.FeatureGroup(
    name="🌿 Autres espaces verts"
)


# ============================================================
# 6. CLUSTER
# ============================================================

cluster = MarkerCluster(
    name="📍 Espaces verts"
).add_to(carte)


# ============================================================
# 7. AJOUT DES MARQUEURS
# ============================================================

for _, lieu in gdf.iterrows():

    if lieu["type"] == "Parc":
        couleur = "green"

    elif lieu["type"] == "Jardin":
        couleur = "blue"

    elif lieu["type"] == "Bois":
        couleur = "darkgreen"

    else:
        couleur = "purple"


    popup = f"""
    <div style="width:230px">

        <h4>{lieu["nom"]}</h4>

        <b>Type :</b> {lieu["type"]}<br><br>

        <b>Latitude :</b> {lieu["latitude"]}<br>

        <b>Longitude :</b> {lieu["longitude"]}

    </div>
    """


    marqueur = folium.Marker(
        location=[
            lieu["latitude"],
            lieu["longitude"]
        ],

        popup=folium.Popup(
            popup,
            max_width=300
        ),

        tooltip=lieu["nom"],

        icon=folium.Icon(
            color=couleur,
            icon="tree",
            prefix="fa"
        )
    )


    # Le marqueur est ajouté au cluster
    marqueur.add_to(cluster)


# ============================================================
# 8. AJOUT DES GROUPES
# ============================================================

parcs.add_to(carte)
jardins.add_to(carte)
bois.add_to(carte)
autres.add_to(carte)


# ============================================================
# 9. CONTROLE DES COUCHES
# ============================================================

folium.LayerControl().add_to(carte)


# ============================================================
# 10. TITRE
# ============================================================

titre = f"""
<div style="
    position: fixed;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;
    background-color: white;
    padding: 12px 20px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3);
">

    <h3 style="margin:0;">
        🌳 Espaces verts à Paris
    </h3>

    <p style="margin:5px 0 0 0;">
        <b>{nombre_total}</b>
        espaces verts représentés
    </p>

</div>
"""

carte.get_root().html.add_child(
    folium.Element(titre)
)


# ============================================================
# 11. STATISTIQUES
# ============================================================

statistiques = ""

for type_espace, nombre in nombre_par_type.items():

    statistiques += f"""
    <li>
        <b>{type_espace}</b> : {nombre}
    </li>
    """


legende = f"""
<div style="
    position: fixed;
    bottom: 30px;
    left: 30px;
    width: 220px;
    background-color: white;
    border: 2px solid grey;
    z-index: 9999;
    padding: 12px;
    border-radius: 8px;
">

    <h4>📊 Statistiques</h4>

    <p>
        <b>Total :</b> {nombre_total}
    </p>

    <ul>
        {statistiques}
    </ul>

</div>
"""

carte.get_root().html.add_child(
    folium.Element(legende)
)


# ============================================================
# 12. SAUVEGARDE
# ============================================================

nom_fichier = "carte_espaces_verts_paris.html"

carte.save(nom_fichier)


# ============================================================
# 13. RESULTAT
# ============================================================

print("======================================")
print("       PROJET SIG - PARIS")
print("======================================")

print(f"Nombre total : {nombre_total}")

print("\nRépartition :")

for type_espace, nombre in nombre_par_type.items():
    print(f"- {type_espace} : {nombre}")

print("\nCarte créée avec succès !")
print(f"Fichier : {nom_fichier}")