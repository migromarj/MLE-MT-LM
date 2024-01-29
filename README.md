# MLE G9: Confiabilidad de Modelos de Lenguaje

> [!IMPORTANT]  
> Es importante que si desea llevar a cabo la ejecución del proyecto tenga instalada la versión 3.9.X de Python. Nosotros, por ejemplo, hemos hecho uso de la versión [3.9.13](https://www.python.org/downloads/release/python-3913/).

## Instalación de dependencias

Puede instalar todas las dependencias necesarias para la ejecución del proyecto con el comando: `pip install -r requirements.txt`

## Inicialización del archivo .env

Debe crear un archivo `.env`donde almacenar las variables de entorno necesarias, para ello puede copiar el contenido de la plantilla que se proporciona, con el nombre `.env.template`, y completarla con sus datos:

- `HUGGING_FACE_API_KEY` hace referencia a la API Key de la plataforma Hugging Face, necesaria para realizar peticiones sobre los distintos modelos de lenguaje bajo prueba. Si tiene problemas para obtenerla puede seguir el _quicktour_ que se accesible a través de su [página web](https://huggingface.co/docs/api-inference/quicktour).

- `BING_U_COOKIE` hace referencia a la cookie que tiene como nombre "U\_", en la página de Bing Chat. Si tiene problemas para obtenerla puede acceder al tutorial que se proporciona en el siguiente [enlace](https://www.youtube.com/watch?v=u0BzcbP1AVw&ab_channel=snuowCh).

- `SECURE_1PSID`, `SECURE_1PSIDTS` y `SECURE_1PSIDCC` hacen referencia a las cookies necesarias para el uso de Google Bard. Si tiene problemas para obtenerla puede acceder al repositorio del paquete en el siguiente [enlace](https://github.com/dsdanielpark/Bard-API). En el, aparte del tutorial principal descrito en el readme, si se tiene aún problemas puede acceder al apartado issues.
