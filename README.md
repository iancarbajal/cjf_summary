# Resumidor de PDFs

## Descripción

Este proyecto es un resumidor de documentos PDF que utiliza GPT-3.5 para generar resúmenes. El modelo de GPT-3.5 se emplea para extraer la información más relevante de los documentos y generar un resumen conciso.

## Requisitos

- Conda (para gestionar el entorno)
- Python 3.x
- Una clave de API de OpenAI (para acceder a GPT-3.5)

## Instrucciones de configuración

### 1. Crear un entorno de Conda

Primero, crea un nuevo entorno de Conda. Ejecuta el siguiente comando:

```bash
conda create --name nombre_del_entorno python=3.x
```

Reemplaza `nombre_del_entorno` con el nombre que desees para tu entorno (por ejemplo, `pdf_resumidor`). Si prefieres una versión específica de Python, reemplaza `3.x` con el número de la versión deseada.

### 2. Activar el entorno

Activa el entorno recién creado ejecutando:

```bash
conda activate nombre_del_entorno
```

### 3. Instalar Tesseract

Instala Tesseract usando Conda desde el canal `conda-forge` ejecutando el siguiente comando:

```bash
conda install -c conda-forge tesseract
```

### 4. Instalar dependencias de Python

Finalmente, instala todas las dependencias de Python ejecutando:

```bash
pip install -r requirements.txt
```

Esto instalará todos los paquetes listados en el archivo `requirements.txt`.

### 5. Clave de API de OpenAI

Para utilizar GPT-3.5, necesitarás una clave de API de OpenAI. Coloca tu clave en un archivo llamado `OPENAI_KEY.txt` en la raíz del proyecto. El archivo debe contener únicamente la clave de API en texto plano.
}
## Uso

Una vez que el entorno esté configurado, puedes usar el proyecto para resumir archivos PDF. El script principal procesará los archivos PDF y generará resúmenes utilizando GPT-3.5. Asegúrate de que el archivo `OPENAI_KEY.txt` esté presente y contenga la clave de API correcta.
