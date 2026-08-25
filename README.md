# Calculador de Elementos en Planos/Documentos

Aplicación Streamlit para medir elementos en imágenes o PDFs. Sube un documento, define las dimensiones reales del papel y dibuja un rectángulo sobre el elemento para obtener sus dimensiones reales y porcentuales.

## Contenido del repositorio

- `app.py` — aplicación principal en Streamlit.
- `requirements.txt` — dependencias usadas por el proyecto.

## Requisitos

- Windows, macOS o Linux
- Python 3.11 (se recomienda)
- `git` (para subir al repositorio)

## Instalación (Windows - PowerShell)

1. Clona el repositorio:

```powershell
git clone https://github.com/lauzarg/calculador_imagenes.git
cd calculador_imagenes
```

2. Crea y activa un entorno virtual con Python 3.11:

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
```

Si tu sistema no tiene `py -3.11`, descarga e instala Python 3.11 desde https://www.python.org/

3. Actualiza `pip` e instala dependencias:

```powershell
python -m pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

4. Ejecuta la app:

```powershell
streamlit run app.py
```

Abre la URL que Streamlit muestra (normalmente `http://localhost:8501`).

## Instalación con Conda

Si prefieres `conda`:

```bash
conda create -n calcimg python=3.11 -y
conda activate calcimg
pip install -r requirements.txt
python -m streamlit run app.py
```

## Recomendaciones si falla la instalación

- Si `numpy` intenta compilar (error de Meson/compilador), instala una versión binaria compatible:

```powershell
pip install numpy==1.25.2
pip install -r requirements.txt
```

- Si `pip` no existe en el intérprete, asegúrate de activar correctamente el `venv` o usa el ejecutable directo:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Uso

1. Sube un PDF o imagen en la barra lateral.
2. Define `Unidad`, `Ancho real` y `Alto real` (p.ej. 210 x 297 mm para A4).
3. Ajusta el ancho de visualización si lo deseas.
4. Dibuja un rectángulo sobre el elemento en la imagen.
5. Consulta las medidas reales y porcentajes en el panel derecho.

## Archivos importantes

- `app.py` — lógica principal y UI.
- `requirements.txt` — versiones recomendadas de dependencias.

## Licencia

Este proyecto se publica bajo la **Licencia MIT** con los titulares de copyright:

- `lauzarg`
- `GitHub Copilot`

Resumen de la licencia MIT:

- Tipo: licencia permisiva y de código abierto.
- Permisos: permite usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y vender el software.
- Requisito principal: conservar el aviso de copyright y el texto de la licencia en todas las copias o partes sustanciales.
- Limitación de responsabilidad: el software se entrega “tal cual”, sin garantías; los autores no son responsables por daños.
- Compatibilidad: puede incorporarse en proyectos propietarios (no obliga a abrir el código derivado).

