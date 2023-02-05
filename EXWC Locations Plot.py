# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 17:46:36 2023

@author: Scott2
"""

import pandas as pd
import plotly.graph_objects as go
import requests
import urllib.parse

locations = pd.DataFrame(
    {
        "Name": [
            "EXWC Headquarters",
            "East Coast Det",
            "Equipment Maintenance Center Det",
            "Ocean Equipment Det",
            "Maritime Prepositioning Forces Det",
            "COSO Geothermal Plant",
            "PACFLT LNO",
            "WARTEC",
            "WETS",
        ],
        "Type": [
            "Headquarters",
            "Detachment",
            "Detachment",
            "Detachment",
            "Detachment",
            "Detachment",
            "Detachment",
            "Site",
            "Site",
        ],
        "Location": [
            "Port Hueneme, CA",
            "Washington, DC",
            "Gulfport, MS",
            "St. Juliens Creek",
            "Blount Island, FL",
            "China Lake, CA",
            "Pearl Harbor, HI",
            "Twentynine Palms, CA",
            "Kaneohe, HI",
        ],
        "TextPosition": [
            "bottom left",
            "middle left",
            "middle left",
            "middle left",
            "top left",
            "top left",
            "middle left",
            "bottom right",
            "bottom right",
        ],
    }
)

FEC_locations = pd.DataFrame(
    {
        ("NORTHWEST", "Silverdale, WA"),
        ("SOUTHWEST", "San Diego, CA"),
        ("SOUTHEAST", "Jacksonville, CA"),
        ("MIDLANT", "Norfolk, VA"),
        ("WASHINGTON", "Washington, DC"),
    },
    columns=["Name", "Location"],
)

# Get lat/long from OSM using Nominatim API
# https://nominatim.org/release-docs/develop/api/Search/
lat = []
lon = []
for i in range(len(locations)):
    url = (
        "https://nominatim.openstreetmap.org/search/"
        + urllib.parse.quote(locations.iloc[i]["Location"])
        + "?format=json"
    )
    response = requests.get(url).json()
    lat.append(response[0]["lat"])
    lon.append(response[0]["lon"])
locations["lat"] = lat
locations["lon"] = lon

lat = []
lon = []
for i in range(len(FEC_locations)):
    url = (
        "https://nominatim.openstreetmap.org/search/"
        + urllib.parse.quote(FEC_locations.iloc[i]["Location"])
        + "?format=json"
    )
    response = requests.get(url).json()
    lat.append(response[0]["lat"])
    lon.append(response[0]["lon"])
FEC_locations["lat"] = lat
FEC_locations["lon"] = lon

# create df that counts each category and creates summary string
loc_types = locations.groupby("Type").agg(Count=("Name", "count"))
loc_types = loc_types.reset_index()

# Create figure
fig = go.Figure()
SCALE = 10
# detachment, headquarters, site
legend_ranks = [1001, 1000, 1002]
colors = ["lightsteelblue", "lightsteelblue", "lightsteelblue"]
symbols = ["circle-dot", "star-dot", "triangle-up-dot"]
sizes = [30, 40, 30]

# annos = []

# add a trace for each loc_type
for i in range(len(loc_types)):
    df_sub = locations[locations["Type"] == loc_types.iloc[i, 0]]
    fig.add_trace(
        go.Scattergeo(
            locationmode="USA-states",
            text="<b>" + df_sub["Name"] + "</b><BR>" + df_sub["Location"],
            hoverinfo="text",
            mode="markers",
            textposition=df_sub["TextPosition"],
            textfont=dict(
                size=18,
                family="Arial",
            ),
            lon=df_sub["lon"],
            lat=df_sub["lat"],
            marker=dict(
                symbol=symbols[i],
                size=sizes[i],
                color=colors[i],
                opacity=0.65,
                line_color="rgb(40,40,40)",
                line_width=0.5,
                sizemode="area",
            ),
            name=loc_types.iloc[i, 0],
            legendrank=legend_ranks[i],
        )
    )
    # for index, row in df_sub.iterrows():
    #     anno = dict(
    #         x=row[0],
    #         text="<b>" + df_sub.loc[index]["Name"] + "</b><BR>" + df_sub.loc[index]["Location"],
    #         showarrow=True,
    #         arrowhead=0,
    #         font=dict(color="red"),
    #         # ax=0,
    #         # ay=-20,
    #         bgcolor="white",
    #         opacity=0.85,
    #     )
    #     annos.append(anno)

fig.update_layout(
    # title_text="EXWC Locations",
    showlegend=True,
    legend=dict(title_font_family="Arial", font=dict(size=38), x=0.65, y=0.9),
    geo=dict(
        scope="usa",
        landcolor="rgb(10, 82, 147)",
        # landcolor="rgb(217, 217, 217)",
    ),
    # scene=dict(annotations=annos),
    # autosize=False,
    width=1500,
    height=1200,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=0,
    ),
)

fig.show()

fig.write_html("plot.html", auto_open=True)
fig.write_image("images/EXWC Locations1.png", width=1500, height=1200, scale=1)
