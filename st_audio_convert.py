#!/usr/bin/env python3

import sys
import tempfile
import zipfile
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

import streamlit as st
from stqdm import stqdm

from audio_convert import AudioConvert, codecExt, ext_lower

codec_options = tuple(ext_lower)

def run(output_codec, input_data):
    """
    *** Run audio conversion process, using AudioConvert class*** 

    OUTPUTS:
    * list of converted file paths
    * output file extension
    """
    
    with st.container():
        ext = codecExt.get(output_codec) if output_codec in codecExt.keys() else output_codec
        temp_dir = tempfile.TemporaryDirectory()

        c = AudioConvert(
            output_codec, 
            output_dir=Path(temp_dir.name)
            )
        
        converted_files = []
        for uploaded_file in input_data:
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(uploaded_file.getvalue())
                converted_files.append(Path(f.name))
        
        for file in stqdm(converted_files, desc="Converting"):
            c.convert([file])
        
        st.success("Done!")
    
    return converted_files, ext

def download_zip(converted_files, input_data, ext):
    """
    Stores converted files in zip file
    Download zip file with a single button
    """
    zf = zipfile.ZipFile("converted.zip", "w")
    for i,file in enumerate(converted_files):
        file_path = str(file)  
        arcname = Path(input_data[i].name).stem + "." + ext
        zf.write(filename=file_path, arcname=arcname, compress_type=zipfile.ZIP_DEFLATED)
    zf.close()
    
    with open("converted.zip", "rb") as converted_zip:
        st.download_button(
            label=f"Download converted files",
            data=converted_zip,
            file_name="converted.zip",
            mime="application/octet-stream"
        )
        
# ––––––––––––––––––––––––––––––––––––––––––––––––––– 
# Headers
TITLE = "AudioConvert"
SUBTITLE = "Batch audio conversion powered by `FFmpeg`"
st.set_page_config(page_title=TITLE)
st.title(TITLE)
st.subheader(SUBTITLE)

# Main submission form
with st.form(key="my-form") as form:
    output_codec = st.selectbox("Select output codec", 
    codec_options)

    input_data = st.file_uploader(label = "Select files to convert", accept_multiple_files = True)

    submit = st.form_submit_button("Submit")

# Upon user submission
if submit:
    converted_files, ext = run(output_codec, input_data)
    download_zip(converted_files, input_data, ext)