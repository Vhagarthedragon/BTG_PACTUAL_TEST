# Proyecto de API con FastAPI

Este proyecto es una API desarrollada con FastAPI que utiliza Pydantic para la validación de datos, Boto3 para la interacción con AWS, y Docker para la contenedorización. También incluye un archivo YAML de CloudFormation para facilitar el despliegue en AWS.

## Características

- **Framework**: FastAPI
- **Validación de datos**: Pydantic
- **Interacción con AWS**: Boto3
- **Contenedorización**: Docker
- **Despliegue en AWS**: CloudFormation

## Requisitos

- Python 3.7 o superior
- Docker
- AWS CLI configurado

## Estructura del Proyecto

```
/mi_proyecto
│
├── app/
│   ├── main.py            # Punto de entrada de la aplicación
│   ├── routers/           # Rutas de la API
│   ├── models/            # Modelos de Pydantic
│   └── services/          # Servicios de Boto3
│
├── Dockerfile              # Archivo de configuración de Docker
├── requirements.txt        # Dependencias del proyecto
├── cloudformation.yml      # Plantilla de CloudFormation
├── .env                    # Variables de entorno (no subir a repositorio)
└── README.md               # Documentación del proyecto
```

## Instalación

1. **Clona el repositorio**:

   ```bash
   git clone https://github.com/Vhagarthedragon/BTG_PACTUAL_TEST.git
   cd BTG_PACTUAL_TEST
   ```

2. **Instala las dependencias**:

   Crea un entorno virtual y activa el entorno:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate     # En Windows
   ```

   Luego instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configura las credenciales de AWS**:

   Crea un archivo `.env` en la raíz del proyecto y agrega tus credenciales de AWS:

   ```
   AWS_ACCESS_KEY_ID=tu_access_key_id
   AWS_SECRET_ACCESS_KEY=tu_secret_access_key
   ```

4. **Ejecuta la aplicación**:

   Puedes ejecutar la aplicación localmente con:

   ```bash
   uvicorn app.main:app --reload
   ```

## Uso de Docker

Para crear y ejecutar la aplicación dentro de un contenedor Docker, utiliza los siguientes comandos:

1. **Construir la imagen Docker**:

   ```bash
   docker build -t mi_api .
   ```

2. **Ejecutar el contenedor**:

   ```bash
   docker run -d -p 8000:8000 mi_api
   ```

   La API estará disponible en `http://localhost:8000`.

## Despliegue en AWS

Este proyecto incluye un archivo `lambda-backend.yml` que puedes utilizar para desplegar la infraestructura en AWS.

Para desplegar, utiliza el siguiente comando de AWS CLI:

```bash
aws cloudformation create-stack --stack-name mi-stack --template-body file://lambda-backend.yml --parameters ParameterKey=YourParameter,ParameterValue=YourValue
```


