import streamlit as st
from PIL import Image
import numpy as np
import requests
import io
import pandas as pd
API_PLANT = st.secrets["API_CUR"]
dfe = pd.read_csv('plant_name.csv')

img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    # Convert PIL Image to bytes
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='JPEG')
    img_byte_array = img_byte_array.getvalue()
    
    url = 'https://my-api.plantnet.org/v2/identify/all'

    # API parameters
    params = {
        'include-related-images': 'True',
        'no-reject': 'false',
        'lang': 'en',
        'api-key': API_PLANT
    }

    
    # Headers
    headers = {
        'accept': 'application/json',
    }

    # Files to be uploaded
    files = {
        'images': ('resim.jpg', img_byte_array, 'image/jpeg')
    }

    # Make the POST request
    response = requests.post(url, headers=headers, params=params, files=files)
    rj = response.json()
#    st.write(rj)
    commonNames = 'no plants found in picture or it is not our database'
    if 'results' in rj.keys():
        if len(rj['results'] ) > 0:
            if len(response.json()['results'][0]['species']['commonNames']) > 0:
                commonNames = response.json()['results'][0]['species']['commonNames'][0].title()             
                names = commonNames.split()
                st.write(commonNames)
                for name in names:
                    
                    commonNames_df = dfe[dfe['Plant Name'].str.contains(name)]
                    if len(commonNames_df) > 0:
                        st.subheader(name)
                        for index, row in commonNames_df.iterrows():
                            with st.expander(f"{row['Title']}"):
                                st.write(row['Description'])
                

        
    st.write(commonNames)