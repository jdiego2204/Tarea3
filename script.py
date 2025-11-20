import os
import glob
import pydicom
import pandas as pd
import numpy as np
from typing import List, Tuple, Optional

class ProcesadorDICOM:
    """
    Clase para procesar archivos DICOM
    """
    
    def __init__(self, directorio_path: str):
        """
        Inicializa el procesador con la ruta del directorio que contiene archivos DICOM.
        
        :parametro directorio_path: Ruta al directorio con archivos .dcm
        """
        self.directorio_path = directorio_path
        self.loaded_files: List[Tuple[str, pydicom.Dataset]] = []  # (path, ds)
        self.df: Optional[pd.DataFrame] = None
    
    def _obtener_archivos_dicom(self) -> List[str]:
        """
        Escanea el directorio y retorna lista de rutas a archivos .dcm.
        
        :return: Lista de paths a archivos DICOM
        """
        if not os.path.exists(self.directorio_path):
            raise ValueError(f"Directorio no válido: {self.directorio_path}")
        patron = os.path.join(self.directorio_path, "*.dcm")
        archivos = glob.glob(patron)
        if not archivos:
            raise ValueError(f"No se encontraron archivos .dcm en {self.directorio_path}")
        print(f"Encontrados {len(archivos)} archivos .dcm en el directorio.")
        return archivos
    
    def _cargar_dataset(self, archivo_path: str) -> Optional[pydicom.Dataset]:
        """
        Carga un archivo DICOM individual manejando errores.
        
        :parametro archivo_path: Ruta al archivo .dcm
        :return: Dataset si es válido, None en caso contrario
        """
        try:
            ds = pydicom.dcmread(archivo_path)
            return ds
        except pydicom.errors.InvalidDicomError:
            print(f"Advertencia: {archivo_path} no es un archivo DICOM válido. Omitiendo.")
            return None
        except Exception as e:
            print(f"Error al cargar {archivo_path}: {e}")
            return None
    
    def cargar_archivos(self) -> int:
        """
        Carga todos los archivos DICOM válidos del directorio.
        
        :return: Número de archivos cargados exitosamente
        """
        archivos = self._obtener_archivos_dicom()
        self.loaded_files = []
        num_cargados = 0
        for archivo in archivos:
            ds = self._cargar_dataset(archivo)
            if ds:
                self.loaded_files.append((archivo, ds))
                num_cargados += 1
        print(f"Cargados {num_cargados} archivos DICOM válidos de {len(archivos)} encontrados.")
        return num_cargados
    
    def _extraer_metadato(self, ds: pydicom.Dataset, tag: str) -> Optional[str]:
        """
        Extrae un metadato de forma segura, retornando None si no existe.
        
        :parametro ds: Dataset DICOM
        :parametro tag: Nombre del tag (e.g., 'PatientID')
        :return: Valor del tag o None
        """
        try:
            valor = getattr(ds, tag)
            return str(valor) if valor is not None else None
        except AttributeError:
            return None
    
    def extraer_metadatos(self) -> pd.DataFrame:
        """
        Extrae metadatos de todos los datasets y crea un DataFrame.
        Incluye el nombre del archivo como columna para identificar filas.
        
        :return: DataFrame con metadatos
        """
        if not self.loaded_files:
            raise ValueError("No hay archivos cargados. Ejecute cargar_archivos() primero.")
        
        datos = []
        for path, ds in self.loaded_files:
            nombre_archivo = os.path.basename(path)
            
            metadatos = {
                'Nombre_Archivo': nombre_archivo,
                'PatientID': self._extraer_metadato(ds, 'PatientID'),
                'PatientName': self._extraer_metadato(ds, 'PatientName'),
                'StudyInstanceUID': self._extraer_metadato(ds, 'StudyInstanceUID'),
                'StudyDescription': self._extraer_metadato(ds, 'StudyDescription'),
                'StudyDate': self._extraer_metadato(ds, 'StudyDate'),
                'Modality': self._extraer_metadato(ds, 'Modality'),
                'Rows': self._extraer_metadato(ds, 'Rows'),
                'Columns': self._extraer_metadato(ds, 'Columns')
            }
            datos.append(metadatos)
        
        self.df = pd.DataFrame(datos)
        print("Metadatos extraídos y estructurados en DataFrame.")
        return self.df
    
    def analizar_intensidades(self) -> pd.DataFrame:
        """
        Calcula la intensidad promedio de píxeles para cada imagen y la agrega al DataFrame.
        
        :return: DataFrame actualizado con columna 'IntensidadPromedio'
        """
        if self.df is None:
            raise ValueError("No hay DataFrame. Ejecute extraer_metadatos() primero.")
        
        intensidades = []
        for _, ds in self.loaded_files:
            try:
                pixel_array = ds.pixel_array
                intensidad_promedio = np.mean(pixel_array)
                intensidades.append(intensidad_promedio)
            except AttributeError:
                # Si no hay pixel_array (e.g., no es imagen)
                intensidades.append(None)
            except Exception as e:
                print(f"Error al analizar imagen en {ds.filename if hasattr(ds, 'filename') else 'archivo'}: {e}")
                intensidades.append(None)
        
        self.df['IntensidadPromedio'] = intensidades
        print("Análisis de intensidades completado.")
        return self.df
    
    def procesar_todo(self) -> pd.DataFrame:
        """
        Método conveniente que ejecuta todos los pasos: carga, extracción y análisis.
        
        :return: DataFrame final
        """
        self.cargar_archivos()
        self.extraer_metadatos()
        self.analizar_intensidades()
        return self.df

# Ejemplo de uso
if __name__ == "__main__":
    print("=== Procesador de Archivos DICOM ===")
    directorio = input("Ingrese la ruta completa al directorio con archivos DICOM: ").strip()
    
    if not os.path.exists(directorio):
        print(f"Error: El directorio '{directorio}' no existe. Verifique la ruta.")
        exit(1)
    
    try:
        procesador = ProcesadorDICOM(directorio)
        df_final = procesador.procesar_todo()
        print("\n=== Resultados ===")
        print(df_final)
        
        print("\nNota: Muchos campos pueden estar en 'None' porque los archivos están anonimizados o no contienen todos los metadatos.")
        
        # Opcional: guardar a CSV
        salida = input("\n¿Desea guardar el DataFrame como CSV? (s/n): ").strip().lower()
        if salida == 's':
            nombre_archivo = 'metadatos_dicom.csv'
            df_final.to_csv(nombre_archivo, index=False)
            print(f"DataFrame guardado como '{nombre_archivo}'")
    except Exception as e:
        print(f"Error durante el procesamiento: {e}")