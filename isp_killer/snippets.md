```python
extracted_data = {
    "Nombre": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblNombre"),
    "Referencia_de_tramite": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblRefTramite"),
    "Equivalencia_Terapeutica_o_Biosimilar": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblEquivalencia"),
    "Titular": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblEmpresa"),
    "Estado_del_Registro": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblEstado"),
    "Resolucion_Inscribase": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblResInscribase"),
    "Fecha_Inscribase": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblFchInscribase"),
    "Ultima_Renovacion": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblUltimaRenovacion"),
    "Fecha_Proxima_Renovacion": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblProxRenovacion"),
    "Regimen": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblRegimen"),
    "Via_Administracion": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblViaAdministracion"),
    "Condicion_de_Venta": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblCondicionVenta"),
    "Expende_tipo_establecimiento": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblExTipoEstablecimiento"),
    "Indicacion": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_lblIndicacion"),
    "Nombre_PA": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_gvFormulas_ctl02_lblNombreElemento"),
    "Concentracion": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_gvFormulas_ctl02_lblConcentracion"),
    "Unidad_medida": safe_extract(By.ID, "ctl00_ContentPlaceHolder1_gvFormulas_ctl02_lblUnidadMedida")
}
```