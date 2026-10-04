import pandas as pd
import streamlit as st
import io

def limpiar_leads(archivo):
    if archivo.name.endswith('.csv'):
        df = pd.read_csv(archivo)
    else:
        df = pd.read_excel(archivo)
    
    # 1. Eliminar espacios en blanco
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    # 2. Normalizar Emails
    for col in df.columns:
        if 'email' in col.lower() or 'correo' in col.lower():
            df[col] = df[col].astype(str).str.lower()
            
    # 3. Capitalizar Nombres
    for col in df.columns:
        if 'nombre' in col.lower():
            df[col] = df[col].astype(str).str.title()

    # 4. Eliminar duplicados
    email_cols = [c for c in df.columns if 'email' in c.lower() or 'correo' in c.lower()]
    if email_cols:
        df = df.drop_duplicates(subset=[email_cols[0]], keep='first')
    else:
        df = df.drop_duplicates()
        
    output = io.BytesIO()
    if archivo.name.endswith('.csv'):
        df.to_csv(output, index=False)
        mime = 'text/csv'
        nuevo_nombre = 'leads_limpios.csv'
    else:
        df.to_excel(output, index=False, engine='openpyxl')
        mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        nuevo_nombre = 'leads_limpios.xlsx'
        
    output.seek(0)
    return output, nuevo_nombre, mime

st.title("🧹 Limpiador de Leads para Vendedores")
st.write("Sube tu archivo desordenado y descárgalo limpio en segundos.")

archivo_subido = st.file_uploader("Sube tu Excel o CSV", type=["csv", "xlsx"])

if archivo_subido is not None:
    if st.button("¡Limpiar Leads Ahora!"):
        with st.spinner("Procesando datos..."):
            output, nombre_archivo, mime_type = limpiar_leads(archivo_subido)
            
        st.success("¡Listo! Tu archivo está optimizado.")
        st.download_button(
            label="📥 Descargar Archivo Limpio",
            data=output,
            file_name=nombre_archivo,
            mime=mime_type
)

      
