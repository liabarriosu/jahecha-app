import streamlit as st
import pandas as pd
import json
import time

    # Usaremos streamlit para crear una página interativa
st.set_page_config(
    page_title="Jahechá",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo para ocultar la barra superior gris de Streamlit y forzar fondo oscuro detrás
st.markdown("""
    <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 2rem !important;
                background-color: #000000;
            }
        /* Estilizamos los inputs nativos de Streamlit para que combinen con el.  diseño */
        div[data-baseweb="select"] {
            background-color: #ffffff !important;
            border-radius: 6px !important;
    }
        .stSelectbox label {
            color: #ffffff !important;
            font-weight: 600 !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        }
        /* botón de descarga*/
        div.stDownloadButton > button {
            width: 100% !important;
            padding: 14px !important;
            background-color: #0c4b40 !important;
            color: white !important;
            border: none !important;
            border-radius: 0px !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            transition: filter 0.2s !important;
        }
        div.stDownloadButton > button:hover {
            filter: brightness(1.2) !important;
        }
    </style>
""", unsafe_allow_html=True)

# Cargar base de datos limpia
@st.cache_data

def cargar_datos():
    try:
        return pd.read_csv('datos_web_limpios.csv')
    except (FileNotFoundError, Exception) as e:
    
        print(f"Error: No se pudieron cargar los datos. Puedes contactar a Paraguay Data para informar de este problema.")
        return None
        

df = cargar_datos()

# Título, Subtítulo y Videos
html_cabecera = """
<div class="video-background-container">
    <video class="video-item" autoplay muted loop src="./static/video1.mp4"></video>
    <video class="video-item" autoplay muted loop src="./static/video2.mp4"></video>
    <video class="video-item" autoplay muted loop src="./static/video3.mp4"></video>
    <video class="video-item" autoplay muted loop src="./static/video4.mp4"></video>
</div>

<style>
    .video-background-container {
       position: fixed;
top: 0; left: 0; width: 100vw; height: 100%;
display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 5px;
        z-index: -1;
        opacity: 0.25; /* Bajado levemente para mejorar el contraste del texto */
    }
    .video-item {
        width: 100%; height: 100%; object-fit: cover; background: #0f172a;
    }
   .main-header {
        text-align: center;
        max-width: 680px;
        font-family: 'Segoe UI', sans-serif;
        
        /* Nuevas propiedades para centrar verticalmente */
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin: 0 auto; 
    }
    .brand-title-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        margin-bottom: 8px;
    }
    .brand-icon-logo {
        width: 32px;
        height: 32px;
        stroke: #e06b00; /* Tu naranja oscuro distintivo */
        stroke-width: 2.5;
        stroke-linecap: round;
        stroke-linejoin: round;
        fill: none;
    }
    .main-header h1 { 
        color: #ffffff; 
        font-size: 2.6rem; 
        margin: 0; 
        font-weight: 700;
        letter-spacing: 0.5px;
        text-shadow: 0 4px 12px rgba(0,0,0,0.5); 
    }
    .description-text { 
        color: #ffffff; 
        font-size: 1.15rem; 
        margin-bottom: 24px; 
        font-weight: 400;
        opacity: 0.95;
        text-shadow: 0 2px 6px rgba(0,0,0,0.5);
    }
    .instructions-text { 
        color: rgba(255, 255, 255, 0.8); 
        font-size: 0.95rem; 
        line-height: 1.6;
        margin: 0 auto;
        padding: 0 10px;
        text-align: justify; /* Justificado sutil para bloques de texto largos */
        text-shadow: 0 1px 4px rgba(0,0,0,0.4);
    }
</style>

<div class="main-header">
    <div class="brand-title-container">
        <!-- Icono de marca: Lupa analítica que engloba el concepto Jahechá (Ver) -->
        <svg class="brand-icon-logo" viewBox="0 0 24 24">
            <circle cx="11" cy="11" r="7"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <h1>Jahechá</h1>
    </div>
    <div class="description-text">Herramienta para cruce masivo de datos de compras públicas.</div>
    <div class="instructions-text">
        En Jahechá podés descargar con un solo click la información masiva de contratos en Paraguay por año e institución. Luego, podés cruzarla con la base de datos oficial de beneficiarios finales del Ministerio de Hacienda. Elegí hacer el cruce de manera manual o de forma masiva. El objetivo es simplificar una tarea que podría llevar días y hacerla en segundos.
    </div>
</div>
"""
st.components.v1.html(html_cabecera := html_cabecera, height=800)

# PANEL DE CONTROL 

col_izq, col_centro, col_der = st.columns([1, 2, 1])

with col_centro:
    st.markdown('<div style="background-color: rgba(255,255,255,0.05); padding: 20px; border-radius: 0px; border: 1px solid rgba(255,255,255,0.1);">', unsafe_allow_html=True)
    
# Filtros reales dinámicos procesados por Streamlit
    listado_anhos = ["Todos"] + sorted([str(int(a)) for a in df['anho_adjudicacion'].dropna().unique()], reverse=True)
    anho_sel = st.selectbox("Seleccioná el año:", listado_anhos)
    
    listado_inst = ["Todas"] + sorted(df['nombre_institucion'].dropna().unique().tolist())
    inst_sel = st.selectbox("Seleccioná la institución a auditar:", listado_inst)
    
    # Procesar filtros en Pandas
    df_filtrado = df.copy()
    if anho_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado['anho_adjudicacion'] == int(anho_sel)]
    if inst_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado['nombre_institucion'] == inst_sel]
        
    #Botón de Descarga Nativo de Streamlit (¡No falla nunca!)
    csv_bytes = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar los datos filtrados (En formato CSV)",
        data=csv_bytes,
        file_name=f"jahecha_{inst_sel.replace(' ', '_')}_{anho_sel}.csv",
        mime="text/csv"
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Aquí van los gráficos interactivos
# Calculamos el top 5 para el gráfico
top_proveedores = (
    df_filtrado.groupby('nombre_proveedor')['monto_adjudicado']
    .sum()
    .reset_index()
    .sort_values(by='monto_adjudicado', ascending=False)
    .head(5)
)

nombres_js = top_proveedores['nombre_proveedor'].tolist()
montos_js = (top_proveedores['monto_adjudicado'] / 1_000_000).round(2).tolist()

# Generamos el gráfico
html_grafico = f"""
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
    .analytics-box {{
        background: transparent; /* Sin fondo de ningún color */
        border-radius: 0px;
        padding: 10px;
        color: #ffffff; /* Letras blancas para el contenedor */
        font-family: 'Segoe UI', sans-serif;
        max-width: 650px;
        margin: 20px auto;
        box-shadow: none; /* Sin sombras */
    }}
    .analytics-box h3 {{ 
        font-size: 1.1rem; 
        color: #ffffff; /* Título en blanco */
        margin-bottom: 15px; 
        text-align: center; 
        border-bottom: 1px solid rgba(255, 255, 255, 0.2); /* Línea sutil blanca */
        padding-bottom: 5px; 
    }}
    .chart-wrapper {{ position: relative; height: 220px; }}
</style>

<div class="analytics-box">
    <h3> Ranking de proveedores según total de adjudicaciones (En millones de guaraníes)</h3>
    <div class="chart-wrapper">
        <canvas id="chartProveedores"></canvas>
    </div>
</div>

<script>
    const nombres = {json.dumps(nombres_js)};
    const montos = {json.dumps(montos_js)};
    
    if (nombres.length > 0) {{
        const ctx = document.getElementById('chartProveedores').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: nombres,
                datasets: [{{
                    label: 'Monto de Contratos (Millones ₲)',
                    data: montos,
                    backgroundColor: '#e06b00', /* Naranja levemente más oscuro */
                    borderWidth: 0
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ 
                    legend: {{ display: false }} 
                }},
                scales: {{
                    x: {{
                        ticks: {{ color: '#ffffff' }}, /* Letras del eje X blancas */
                        grid: {{ color: 'rgba(255, 255, 255, 0.1)' }} /* Líneas de fondo tenues */
                    }},
                    y: {{
                        ticks: {{ color: '#ffffff' }}, /* Letras del eje Y blancas */
                        grid: {{ display: false }} /* Quitamos líneas verticales que estorben */
                    }}
                }}
            }}
        }});
    }}
</script>
"""

# Solo mostramos el gráfico si el usuario filtró alguna institución específica
if inst_sel != "Todas" or anho_sel != "Todos":
    st.components.v1.html(html_grafico, height=300)


# TABLA DE PREVISUALIZACIÓN INTERACTIVA
st.markdown("""
    <style>
        .preview-box {
            background: transparent; /* Sin fondo, se integra con tu sitio */
            border-radius: 0px;
            padding: 10px 0px;
            color: #ffffff; /* Letras principales blancas */
            font-family: 'Segoe UI', sans-serif;
            max-width: 650px;
            margin: 20px auto;
            box-shadow: none; /* Sin sombras */
        }
        .preview-title-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px; /* Separación entre el icono de tabla y el texto */
            margin-bottom: 12px;
        }
        .preview-icon-table {
            width: 22px;
            height: 22px;
            stroke: #e06b00; /* Tu naranja oscuro en las líneas */
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
            fill: none;
        }
        .preview-box h3 { 
            font-size: 1.1rem; 
            color: #ffffff; /* Título en blanco puro */
            margin: 0;
            letter-spacing: 0.5px;
        }
        .preview-box p {
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.75); /* Blanco suavizado para la descripción */
            text-align: center;
            margin-bottom: 15px;
            padding: 0px 5px;
        }
    </style>
    
    <div class="preview-box">
        <div class="preview-title-container">
            <!-- Dibujo lineal de una cuadrícula/tabla en SVG -->
            <svg class="preview-icon-table" viewBox="0 0 24 24">
                <rect x="3" y="3" width="18" height="18" rx="0"></rect>
                <line x1="3" y1="9" x2="21" y2="9"></line>
                <line x1="3" y1="15" x2="21" y2="15"></line>
                <line x1="10" y1="3" x2="10" y2="21"></line>
            </svg>
            <h3>Previsualización de contratos</h3>
        </div>
        <p>Explorá y ordená las columnas directamente. Usá el buscador interno para encontrar proveedores específicos.</p>
    </div>
""", unsafe_allow_html=True)

#Creamos un contenedor centrado para la tabla 
col_izq_t, col_centro_t, col_der_t = st.columns([1, 2, 1])

with col_centro_t:
    # Seleccionamos y ordenamos las columnas que queremos mostrar, para no saturar la pantalla
    
    df_vista = df_filtrado[[
        'anho_adjudicacion', 
        'nombre_proveedor', 
        'monto_adjudicado', 
        'ruc_proveedor'
    ]].copy()
    
    # Renombramos las columnas para que el usuario las lea de forma amigable
    df_vista.columns = ['Año', 'Proveedor', 'Monto en guaraníes', 'RUC']
    
    # Renderizamos la tabla interactiva
    st.dataframe(
        df_vista,
        use_container_width=True, # Hace que se adapte al ancho del contenedor
        hide_index=True,          # Oculta la columna de índices de pandas que no aporta valor
        height=380                # Altura ideal para mostrar alrededor de 10 filas cómodamente
    )


######
#  MÓDULO 2: INVESTIGACIÓN DE BENEFICIARIOS FINALES 

# Cargamos la segunda base de datos
@st.cache_data
def cargar_beneficiarios():

    # Se añade el delimitador ';' y la codificación 'latin-1' para compatibilidad real
    df_b = pd.read_csv('2. Beneficiarios_finales.csv', sep=';', encoding='latin-1')
    
    
    # hOMOLOGACIÓN DE COLUMNAS CLAVE
    if 'beneficiario_final' in df_b.columns and 'nombres_apellidos' not in df_b.columns:
        df_b = df_b.rename(columns={'beneficiario_final': 'nombres_apellidos'})
        
    # Limpieza de valores nulos críticos
    if 'denominacion' in df_b.columns:
        df_b['denominacion'] = df_b['denominacion'].fillna("").astype(str)
    else:
        df_b['denominacion'] = ""

    if 'nombres_apellidos' in df_b.columns:
        df_b['nombres_apellidos'] = df_b['nombres_apellidos'].fillna("").astype(str)
    else:
        df_b['nombres_apellidos'] = ""
        
    return df_b

df_beneficiarios = cargar_beneficiarios()

# Función inteligente para normalizar texto
def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    import unicodedata
     # Convertimos a minúsculas
    t = texto.lower()
    # Removemos acentos
    t = "".join(c for c in unicodedata.normalize('NFD', t) if unicodedata.category(c) != 'Mn')
    # Eliminamos espacios en blanco extra
    return " ".join(t.split())


# Buscador de Beneficiarios
st.markdown("""
    <style>
        .beneficiarios-box {
            background: transparent; /* Sin fondo, se integra con tus videos */
            border-radius: 0px;
            padding: 10px 0px;
            color: #ffffff; /* Letras blancas principales */
            font-family: 'Segoe UI', sans-serif;
            max-width: 650px;
            margin: 40px auto 10px auto;
            box-shadow: none; /* Sin sombras */
        }
        .beneficiarios-title-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px; /* Separación entre la lupa y el texto */
            margin-bottom: 25px;
        }
        .beneficiarios-icon-lupa {
            width: 24px;
            height: 24px;
            stroke: #e06b00; /* Tu naranja oscuro en las líneas del dibujo */
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
            fill: none; /* Interior transparente */
        }
        .beneficiarios-box h2 { 
            font-size: 1.3rem; 
            color: #ffffff; 
            margin: 0;
            letter-spacing: 0.5px;
        }
        .explicacion-text {
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.75); /* Blanco suave/atenuado */
            line-height: 1.5;
            margin-bottom: 20px;
            padding: 0px 5px;
            background-color: transparent;
        }
    </style>
    
    <div class="beneficiarios-box">
        <div class="beneficiarios-title-container">
            <!-- Dibujo lineal y artístico de una lupa en SVG -->
            <svg class="beneficiarios-icon-lupa" viewBox="0 0 24 24">
                <circle cx="11" cy="11" r="7"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <h2>Rastreador de Beneficiarios Finales</h2>
        </div>
        <div class="explicacion-text">
            <strong>¿Cómo funciona el cruce inteligente?</strong><br>
            Este sistema conecta las empresas adjudicadas con el registro oficial de sus beneficiarios finales (verdaderos accionistas). 
            La búsqueda utiliza un algoritmo de coincidencia flexible, ignorando mayúsculas, minúsculas, puntos, comas y acentos. 
            Esto te permite encontrar posibles coincidencias reales aunque los nombres hayan sido escritos de forma ligeramente diferente en los distintos registros del Estado.
            Puedes buscar a una empresa en específico o realizar el cruce automático de todas las empresas.
        </div>
    </div>
""", unsafe_allow_html=True)
# Contenedor centrado para los controles del buscador
col_izq_b, col_centro_b, col_der_b = st.columns([1, 2, 1])

with col_centro_b:
    # Opción de método de búsqueda: "Escribir/Pegar" o "Cruce automático masivo"
    metodo_busqueda = st.radio(
        "Elige cómo buscar:",
        [
            "Escribir/Pegar nombre de empresa manualmente",
            "Cruce automático masivo (con todo el ranking de arriba)"
        ]
    )
    
    # Caso 1: Búsqueda Manual individual
    if metodo_busqueda == "Escribir/Pegar nombre de empresa manualmente":
        empresa_a_buscar = st.text_input("Escribe o pega el nombre de la empresa de tu interés aquí:")
        
        if empresa_a_buscar.strip():
            busqueda_normalizada = normalizar_texto(empresa_a_buscar)
            
            # Generamos filtros sobre denominación y nombres_apellidos
            denominaciones_normalizadas = df_beneficiarios['denominacion'].apply(normalizar_texto)
            mascara_empresa = denominaciones_normalizadas.apply(
                lambda x: busqueda_normalizada in x or x in busqueda_normalizada if x else False
            )
            
            mascara_persona = pd.Series(False, index=df_beneficiarios.index)
            if 'nombres_apellidos' in df_beneficiarios.columns:
                personas_normalizadas = df_beneficiarios['nombres_apellidos'].apply(normalizar_texto)
                mascara_persona = personas_normalizadas.apply(
                    lambda x: busqueda_normalizada in x or x in busqueda_normalizada if x else False
                )
            
            resultados_beneficiarios = df_beneficiarios[mascara_empresa | mascara_persona]
            
            # Mostrar resultados de la búsqueda manual
            if not resultados_beneficiarios.empty:
                st.success(f"Se encontraron {len(resultados_beneficiarios)} coincidencias asociadas a tu búsqueda:")
                
                columnas_existentes = df_beneficiarios.columns.tolist()
                renombrar_dict = {
                    'denominacion': 'Empresa / Razón Social',
                    'nombres_apellidos': 'Nombre del Socio / Beneficiario',
                    'participacion_porcentaje': '% de Participación',
                    'porcentaje': '% de Participación',
                    'nacionalidad': 'Nacionalidad',
                    'domicilio': 'Dirección / Domicilio',
                    'tipo_entidad': 'Tipo de Entidad',
                    'nro_documento': 'Documento / RUC'
                }
                columnas_ordenadas_ideal = ['denominacion', 'nombres_apellidos', 'nro_documento', 'participacion_porcentaje', 'nacionalidad', 'domicilio', 'tipo_entidad']
                columnas_a_mostrar = [col for col in columnas_ordenadas_ideal if col in columnas_existentes]
                
                df_mostrar = resultados_beneficiarios[columnas_a_mostrar].rename(columns=renombrar_dict) if columnas_a_mostrar else resultados_beneficiarios
                st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
            else:
                st.info("No se encontraron registros de empresas o personas que coincidan con tu búsqueda.")

    #Caso 2: Cruce automático masivo a petición con barra de progreso
    else:
        # Validación de seguridad: Comprobamos si 'top_proveedores' existe y tiene datos
        if 'top_proveedores' in globals() and len(top_proveedores) > 0:
            st.warning(f"Se realizará un cruce masivo para los **{len(top_proveedores)}** proveedores del ranking de arriba.")
            
            #Botón 
            boton_ejecutar = st.button(" Iniciar Cruce Masivo Inteligente")
            
            if boton_ejecutar:
                # Contenedores visuales para la barra de espera
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                with st.spinner("Procesando bases de datos y emparejando socios..."):
                    # Pre-calculamos la normalización del dataframe de beneficiarios una sola vez para ganar velocidad
                    denominaciones_normalizadas = df_beneficiarios['denominacion'].apply(normalizar_texto)
                    
                    lista_resultados = []
                    total_empresas = len(top_proveedores)
                    
                #Iteramos sobre todos los proveedores del ranking
                    for i, (index, fila) in enumerate(top_proveedores.iterrows()):
                        nombre_prov = str(fila['nombre_proveedor'])
                        prov_normalizado = normalizar_texto(nombre_prov)
                        
                        # Actualizar barra de progreso y el texto descriptivo
                        progreso_actual = (i + 1) / total_empresas
                        progress_bar.progress(progreso_actual)
                        status_text.text(f"Analizando ({i+1}/{total_empresas}): {nombre_prov}")
                        
                        #Filtro inteligente
                        mascara = denominaciones_normalizadas.apply(
                            lambda x: prov_normalizado in x or x in prov_normalizado if x else False
                        )
                        coincidencias = df_beneficiarios[mascara].copy()
                        
                        # Si encontramos coincidencias, agregamos información del proveedor original
                        if not coincidencias.empty:
                            coincidencias['Proveedor Adjudicado'] = nombre_prov
                            # Si existe monto adjudicado, lo arrastramos para dar más valor al reporte
                            if 'monto_adjudicado' in top_proveedores.columns:
                                coincidencias['Monto Total Adjudicado'] = fila['monto_adjudicado']
                            lista_resultados.append(coincidencias)
                        
                        #Pequeño delay artificial para que la barra se aprecie visualmente si es muy rápido
                        time.sleep(0.05)
                    
                    # Limpiamos los indicadores de progreso al finalizar
                    progress_bar.empty()
                    status_text.empty()
                    
                # Consolidamos y desplegamos los resultados combinados de todos los proveedores
                if lista_resultados:
                    df_cruce_total = pd.concat(lista_resultados, ignore_index=True)
                    st.success(f"¡Cruce completado con éxito! Se hallaron socios para tus adjudicados.")
                    
                    columnas_existentes = df_cruce_total.columns.tolist()
                    renombrar_dict = {
                        'Proveedor Adjudicado': 'Proveedor (Tu Ranking)',
                        'Monto Total Adjudicado': 'Monto Adjudicado',
                        'denominacion': 'Empresa / Razón Social (Registro)',
                        'nombres_apellidos': 'Socio / Beneficiario Final',
                        'participacion_porcentaje': '% de Participación',
                        'porcentaje': '% de Participación',
                        'nacionalidad': 'Nacionalidad',
                        'domicilio': 'Domicilio',
                        'tipo_entidad': 'Tipo de Entidad',
                        'nro_documento': 'Cédula / RUC del Socio'
                    }
                    
                    columnas_ordenadas_ideal = [
                        'Proveedor Adjudicado', 'Monto Total Adjudicado', 'nombres_apellidos', 
                        'nro_documento', 'participacion_porcentaje', 'nacionalidad', 'tipo_entidad'
                    ]
                    columnas_a_mostrar = [col for col in columnas_ordenadas_ideal if col in columnas_existentes]
                    
                    df_mostrar = df_cruce_total[columnas_a_mostrar].rename(columns=renombrar_dict) if columnas_a_mostrar else df_cruce_total
                    
                    # Formateo del monto adjudicado en la tabla si existe
                    if 'Monto Adjudicado' in df_mostrar.columns:
                        df_mostrar['Monto Adjudicado'] = df_mostrar['Monto Adjudicado'].map(lambda x: f"${x:,.0f}" if pd.notnull(x) else "")
                    
                    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)
                else:
                    st.info(" No se encontraron beneficiarios registrados para ninguno de los proveedores de tu ranking actual.")
        else:
            st.warning(" No se ha detectado el ranking de proveedores. Genera o filtra la tabla de arriba antes de ejecutar el cruce automático.")

#Footer
html_footer = """
<style>
    footer {
        text-align: center;
        font-size: 0.9rem;
        font-weight: 500;
        color: #94a3b8;
        padding: 12px;
        background: rgba(0,0,0,0.5);
        border-radius: 0px;
        max-width: 650px;
        margin: 30px auto 10px auto;
        border: 1px solid rgba(255,255,255,0.1);
        font-family: 'Segoe UI', sans-serif;
    }
</style>
<footer>
    Este proyecto fue desarrollado por Paraguay Data dentro del programa Lede de Columbia University.
</footer>
"""
st.components.v1.html(html_footer, height=100)
