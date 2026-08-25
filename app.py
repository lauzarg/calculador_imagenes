import streamlit as st
from streamlit_drawable_canvas import st_canvas
import fitz  # PyMuPDF
from PIL import Image
import io
import pandas as pd

st.set_page_config(page_title="Medidor de Elementos en Planos/Documentos", layout="wide")

st.title("📏 Medidor Relativo de Elementos")
st.markdown("Sube una imagen o PDF, define sus medidas reales y selecciona el área a medir.")

# ----------------- PANEL LATERAL: CONFIGURACIÓN -----------------
with st.sidebar:
    st.header("1. Cargar Archivo")
    uploaded_file = st.file_uploader("Sube un PDF o Imagen", type=["pdf", "png", "jpg", "jpeg"])
    
    st.header("2. Dimensiones Reales del Documento")
    unidad = st.selectbox("Unidad de medida", ["mm", "cm", "m", "pulgadas"])
    ancho_real = st.number_input(f"Ancho real ({unidad})", min_value=0.1, value=210.0, step=1.0)
    alto_real = st.number_input(f"Alto real ({unidad})", min_value=0.1, value=297.0, step=1.0)
    
    st.header("3. Opciones de Visualización")
    max_display_width = st.slider("Ancho de visualización en pantalla (px)", min_value=400, max_value=1200, value=750, step=50)

# ----------------- PROCESAMIENTO DE IMAGEN -----------------
@st.cache_data
def extraer_imagen(file_bytes, file_type):
    """Convierte el PDF o imagen a objeto PIL Image."""
    if file_type == "application/pdf":
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        page = doc.load_page(0)  # Carga primera página
        pix = page.get_pixmap(dpi=150)  # Renderiza a 150 DPI
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return img
    else:
        return Image.open(io.BytesIO(file_bytes)).convert("RGB")

if uploaded_file is not None:
    # Cargar y ajustar tamaño para visualización
    img_original = extraer_imagen(uploaded_file.getvalue(), uploaded_file.type)
    orig_w, orig_h = img_original.size
    
    # Calcular factor de escala de la visualización en Streamlit
    scale_display = max_display_width / orig_w
    display_w = int(orig_w * scale_display)
    display_h = int(orig_h * scale_display)
    
    img_resized = img_original.resize((display_w, display_h), Image.Resampling.LANCZOS)
    
    col_canvas, col_results = st.columns([3, 2])
    
    with col_canvas:
        st.subheader("Dibuja un rectángulo sobre el elemento")
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Naranja translúcido
            stroke_width=2,
            stroke_color="#FF4B4B",
            background_image=img_resized,
            update_streamlit=True,
            height=display_h,
            width=display_w,
            drawing_mode="rect",
            key="canvas",
        )

    with col_results:
        st.subheader("Resultados de Medición")
        
        if canvas_result.json_data is not None:
            objects = canvas_result.json_data["objects"]
            
            if len(objects) > 0:
                rect = objects[-1]
                
                # Coordenadas en la visualización
                w_rect_display = rect["width"] * rect.get("scaleX", 1)
                h_rect_display = rect["height"] * rect.get("scaleY", 1)
                
                # Coordenadas en la imagen original
                w_rect_orig_px = w_rect_display / scale_display
                h_rect_orig_px = h_rect_display / scale_display
                
                # Factores de escala
                escala_x = ancho_real / orig_w
                escala_y = alto_real / orig_h
                
                # Dimensiones reales calculadas
                elem_ancho_real = w_rect_orig_px * escala_x
                elem_alto_real = h_rect_orig_px * escala_y
                elem_area_real = elem_ancho_real * elem_alto_real
                doc_area_real = ancho_real * alto_real
                
                porcentaje_area = (elem_area_real / doc_area_real) * 100
                porcentaje_ancho = (elem_ancho_real / ancho_real) * 100
                porcentaje_alto = (elem_alto_real / alto_real) * 100
                
                st.metric(label="Área Relativa a la Página", value=f"{porcentaje_area:.2f} %")
                
                st.write("#### Medidas del Elemento:")
                df_medidas = pd.DataFrame({
                    "Propiedad": [
                        f"Ancho ({unidad})", 
                        f"Alto ({unidad})", 
                        f"Área ({unidad}²)",
                        "% del Ancho Total",
                        "% del Alto Total"
                    ],
                    "Valor": [
                        f"{elem_ancho_real:.2f}",
                        f"{elem_alto_real:.2f}",
                        f"{elem_area_real:.2f}",
                        f"{porcentaje_ancho:.2f} %",
                        f"{porcentaje_alto:.2f} %"
                    ]
                })
                st.table(df_medidas)
                st.caption(f"Resolución original: {orig_w} x {orig_h} px")
            else:
                st.info("Dibuja un rectángulo sobre el elemento para calcular las dimensiones.")
else:
    st.info("Por favor, sube un documento PDF o imagen desde la barra lateral izquierda.")