# Jahechá app
Tool for the mass cross-referencing of public procurement data in Paraguay.


**Jahechá** (which means *"Let's see"* or *"To look"* in Guaraní) is a Streamlit-based web application designed to simplify and accelerate public procurement auditing in Paraguay. 

The tool enables users to easily download bulk contract data by year and institution, and immediately cross-reference it with the official beneficial ownership database from the Ministry of Finance (*Ministerio de Hacienda*). It automates a process that manually takes days into a matter of seconds.

## Live Demo
You can access the live application here: **https://jahecha.streamlit.app/**

## Project Components
* **app.py:** Main source code that runs the application logic and the user interface.
* **requirements.txt:** Text file detailing the necessary libraries (Streamlit and Pandas) for the cloud server.
* **first_analysis.py:** Python script or notebook used to analyze Paraguayan public procurement data from 2013 to July 2026, utilizing the items awarded dataset and the awarded suppliers list.
* **awards.csv:** Raw or processed dataset containing the official records of public procurement awards.
* **awa_suppliers.csv:** Reference dataset listing the specific companies and suppliers associated with the procurement awards.
* **datos_web_limpios.csv:** Cleaned database containing public procurement and contract records from Paraguay.
* **2. Beneficiarios_finales.csv:** Official database used to cross-reference and verify supplier identities.
* **static/:** Folder storing the four MP4 video assets that play in the background of the header.
