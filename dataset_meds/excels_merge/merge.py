import pandas as pd
import os
import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_excel(file_path):
    """Carga un archivo Excel en un DataFrame."""
    return pd.read_excel(file_path)

def fill_missing_values(base_df, additional_dfs):
    """Rellena los valores faltantes en base_df usando los otros DataFrames."""
    for df in additional_dfs:
        for index, row in base_df.iterrows():
            if pd.isna(row['Nombre']):
                matching_row = df[df['Registro'] == row['Registro']]
                if not matching_row.empty:
                    base_df.at[index, 'Nombre'] = matching_row['Nombre'].values[0]
                    base_df.at[index, 'Procesado'] = False
    return base_df

def merge_excel_files(folder_path, output_file):
    setup_logging()
    logging.info("Cargando archivos de Excel...")
    
    files = {
        "ALE": "isp_parte_ALE.xlsx",
        "FABI": "isp_parte_FABI.xlsx",
        "DANI": "isp_parte_DANI.xlsx"
    }
    
    base_df = load_excel(os.path.join(folder_path, files["FABI"]))
    additional_dfs = [load_excel(os.path.join(folder_path, files["ALE"])),
                       load_excel(os.path.join(folder_path, files["DANI"]))]
    
    logging.info("Rellenando valores faltantes...")
    base_df = fill_missing_values(base_df, additional_dfs)
    
    logging.info("Guardando archivo CSV resultante...")
    output_csv = output_file.replace(".xlsx", ".csv")
    base_df.to_csv(output_csv, index=False)
    logging.info(f"Archivo combinado guardado en: {output_csv}")

def main():
    folder_path = '.'  # Ajusta esta ruta si es necesario
    output_file = 'resultado_combinado.xlsx'
    merge_excel_files(folder_path, output_file)

if __name__ == "__main__":
    main()
