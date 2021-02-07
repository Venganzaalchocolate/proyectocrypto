# Instalación Python
        # Intalación Python:
                En Linux(ubuntu):
                        # Actualizar lista de repositorios
                                sudo apt-get update

                        # Instalar Python
                                sudo apt-get install python<version>
                En Windows:
                        # Desde la tienda de Microsoft
                        # En este enlace: https://www.python.org/downloads/
        
        #(Opcional) – Instalar Ambiente Virtual Python:
                En Linux(ubuntu):
                        # Primero debemos instalar un paquete adicional:
                                sudo apt-get install -y python3-venv
                        # Crearemos el ambiente virtual
                                python3 -m venv virtual_env
                                «virtual_env» es el nombre de la carpeta donde se encuentra este ambiente virtual.
                        # Activamos el ambiente virtual
                                source virtual_env_/bin/activate

                En Windows:
                        # Descargaremos Python
                        # Desde el cmd de windows crearemos el ambiente virtual
                                python3 -m venv virtual_env
                        # Activamos el ambiente virtual
                                virtual_env\Scripts\activate

# (opcional )Instalar Gestor Paquetes de Python PIP en Ubuntu Linux
        En Linux(ubuntu):
                python3 get-pip.py
        En Windows:
                python3 get-pip.py

# Obtención de Api
        Debes obtener una clave api en https://pro.coinmarketcap.com/
# Instalación de dependencias
        pip install -r requirements.txt
        python iniciando.py

# Ejecuta programa