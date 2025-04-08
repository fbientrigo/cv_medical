# ISP Killer

.___  ___________________   ____  __.___.____    .____     _____________________ 
|   |/   _____/\______   \ |    |/ _|   |    |   |    |    \_   _____/\______   \
|   |\_____  \  |     ___/ |      < |   |    |   |    |     |    __)_  |       _/
|   |/        \ |    |     |    |  \|   |    |___|    |___  |        \ |    |   \
|___/_______  / |____|     |____|__ \___|_______ \_______ \/_______  / |____|_  /
            \/                     \/           \/       \/        \/         \/ 


Es un programa que se encarga de solcitar información de medicamentos al ISP, si somos capaces de acceder a su base de datos esto no sería necesario, sin embargo es dificil contactarlos, por tanto a bomb4rd34r con pedidos.

## Instalación
Es recomendado tener un entorno de Python limpio, por ello utilizo entornos virtuales, crea el entorno virtual y activalo
```
python -m venv env
cd env/Scripts
activate
```
Luego procederemos a instalar los requirements, esto puede demorar un poco
```
python -m pip install -r requirements.txt
```
Entonces estas listo para utilizar el script
```
python isp_killer.py
```
reconoce automaticamente si tienes el archivo "Listado_de_registros.xlsx" a su lado, si no, puedes especificarlo:
```
python isp_killer.py --x path_del_listado.xlsx
```


### Funcionalidades Actuales
- Interacción con la pagina
- Tiempos de espera aleatorios simulando humanos
- Capacidad de guardar registros: Vigentes, No Vigentes, Suspendidos

### Futuras Funcionalidades
- Sistema de json para guardar checkpoints
    - comprobación de 2 pasos para ver que un registro efectivamente se almacena correctamente