# Procesador de Archivos DICOM - Taller Evaluativo Informática 2: Unidad 3

**Integrantes del equipo:**  
Juan Diego Quintero.

## Descripción del Proyecto
Este proyecto desarrolla una aplicación en Python para automatizar la lectura, extracción y almacenamiento de metadatos de archivos DICOM. Utilizando la librería 'pydicom'

## Contenido del repositorio 
- **script.py**: Código principal que implementa la funcionalidad de procesamiento DICOM.
- **README.md**: Documentación del proyecto.
- **venv**: Carpeta del entorno virtual con las dependencias necesarias.
- **Anonymized_20251120**: Carpeta de ejemplo con archivos DICOM para pruebas.

## Funcionamiento del código
- El código carga archivos DICOM de un directorio especificado por el usuario. Para la realización del código se usó una carpeta extraida de una librería pública: https://www.dicomlibrary.com/meddream/?study=1.2.826.0.1.3680043.8.1055.1.20111103111148288.98361414.79379639 
- Extrae metadatos clave (como ID del paciente, fecha del estudio y dimensiones de la imagen). 
- Estructura en un DataFrame de Pandas y calcula la intensidad promedio de píxeles con NumPy. 
- Se simula un flujo de un sistema PACS, encapsulando la lógica en la clase 'ProcesadorDICOM' con Programación Orientada a Objetos (POO). 
- El resultado es un DataFrame consultable.

## Dificultades Encontradas 
- Anonimización de datos (tags ausentes → valores 'None' en DataFrame)
- Manejo de errores en carga (archivos no DICOM válidos)
- Descompresión de píxeles comprimidos (JPEG Lossless requirió instalaciones extras como 'pylibjpeg' para evitar fallos en 'pixel_array').

## Soluciones Implementadas
- Validación de archivos DICOM antes de procesamiento.
- Manejo de excepciones para errores de lectura.
- Instalación de librerías adicionales para soporte de descompresión.

## Instalación y Uso
1. **Preparación del entorno:**  
    *Se realiza la activación del entorno virtual:*  
        - source venv/bin/activate  (Linux/Mac)
        - venv\Scripts\activate  (Windows)
        
    *Dado el caso salte un error de seguridad, usar el siguiente comando:*  
        - Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

2. **Instalación de dependencias:**  
    
    - pip install pydicom pandas numpy
    
    *Para descompresión de imágenes (e.g., JPEG Lossless en MR):*  
        - pip install pylibjpeg pylibjpeg-libjpeg 
        - pip install python-gdcm
        - pip install Pillow
    

3. **Ejecución:**  
    - Coloca archivos DICOM en un directorio.  
    - Ejecuta el archivo.  
    - Ingresa la ruta al directorio.  
    - Visualiza el DataFrame en consola y/o guárdalo como CSV.

