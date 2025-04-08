import pandas as pd
import os

def merge_excel_files(folder_path, output_file):
    merged_data = pd.DataFrame()
    
    # Recorrer todos los archivos en el folder
    for file in os.listdir(folder_path):
        if file.endswith('.xlsx') or file.endswith('.xls'):  # Solo archivos de Excel
            file_path = os.path.join(folder_path, file)
            df = pd.read_excel(file_path)

            # Llenar los registros vacíos si el 'Nombre' falta usando el mismo 'Registro'
            df['Nombre'] = df['Nombre'].fillna(method='ffill')

            merged_data = pd.concat([merged_data, df], ignore_index=True)

    # Eliminar duplicados basándonos en el 'Registro'
    # Eliminar duplicados dando prioridad a las filas con menos NaNs
    merged_data = merged_data.sort_values(by='Nombre', na_position='last') \
                            .drop_duplicates(subset='Registro', keep='first')

    # Guardar el archivo resultante
    merged_data.to_excel(output_file, index=False)
    print(f"Archivo combinado guardado en: {output_file}")


# Ruta del folder con los archivos Excel y nombre del archivo de salida
folder_path = '.'
output_file = 'resultado_combinado.xlsx'
merge_excel_files(folder_path, output_file)
