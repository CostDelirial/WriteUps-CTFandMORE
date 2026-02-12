OWASP API TOP 10 — API1: Broken Object Level Authorization (BOLA)
Introducción

Hola, soy CostDelirial.
En este write-up se documenta la explotación de la vulnerabilidad API1: Broken Object Level Authorization (BOLA) utilizando la aplicación vulnerable crAPI.

El objetivo de esta prueba es demostrar cómo una API expone información sensible y permite el acceso a recursos de otros usuarios mediante la manipulación directa de identificadores en los endpoints.

**Descripción de la vulnerabilidad**

Broken Object Level Authorization (BOLA) ocurre cuando una API no valida correctamente si el usuario autenticado tiene permisos para acceder a un objeto específico.

Esto permite que un atacante modifique identificadores como:

    id = VIN vheiculo

y acceda a información de otros usuarios.

Esta vulnerabilidad está clasificada como:
OWASP API1:2023 – Broken Object Level Authorization y es considerada crítica debido a que puede derivar en exposición masiva de información o toma de cuentas.

**Herramientas utilizadas****

    Burp Suite
    Caido
    Firefox + FoxyProxy
    Postman

Estas herramientas permitieron interceptar, analizar y modificar las peticiones HTTP enviadas a la API de crAPI.

**Enumeración de endpoints****

Para iniciar la explotación fue necesario:

Registrar un usuario en la plataforma.
Interceptar todas las peticiones generadas por la aplicación.
Identificar endpoints relevantes que interactúan con la API.
Durante el análisis se identificaron los siguientes endpoints:

    /identity/api/v2/user/dashboard
    /identity/api/v2/vehicle/vehicles
    /workshop/api/shop/products?limit=30&offset=0
    /community/api/v2/community/posts/recent?limit=30&offset=0
    /community/api/v2/community/posts/DvpHFhEfaiMbtwC2xepPnj
    /identity/api/v2/user/dashboard
    /identity/api/v2/vehicle/vehicles
    /identity/api/v2/user/videos/0
    /workshop/api/merchant/contact_mechanic
    /identity/api/auth/login
    /identity/api/auth/verify

![1770785335991](images/BOLA/1770785335991.png)

**Exposición de información sensible**

Durante la revisión de respuestas del servidor se observó que la API expone:

    Correos electrónicos de usuarios
    Identificadores UUID
    VIN de vehículos
    IDs internos

Esta información puede ser utilizada para realizar pruebas de enumeración y acceso no autorizado.
Prueba de Concepto (PoC)

Se identificaron endpoints que reciben como parámetro directo en la URL el identificador del vehículo o del usuario.

IMAGEN POC

En condiciones normales, un usuario solo debería poder visualizar su propio vehículo.

Sin embargo, al modificar manualmente el identificador:

Se interceptó la petición con Burp Suite.

Se reemplazó el vehicle_id por otro obtenido previamente.

El servidor respondió con información del vehículo perteneciente a otro usuario.

Esto demuestra que la API no valida correctamente la autorización a nivel de objeto.

Impacto

    La explotación de esta vulnerabilidad permite:
    Acceso a datos de otros usuarios
    Exposición de información sensible
    Enumeración de recursos internos
    Posible escalación a toma de cuentas
    Violación de privacidad

El impacto se considera crítico debido a la posibilidad de acceder a información de múltiples usuarios autenticados.

Clasificación OWASP

La vulnerabilidad corresponde a:

OWASP API1:2023 – Broken Object Level Authorization

Debido a que la API no valida si el usuario autenticado tiene permisos para acceder al objeto solicitado.

**Recomendaciones**

    Implementar validación de autorización en cada endpoint.
    Verificar que el objeto solicitado pertenezca al usuario autenticado.
    Evitar exponer identificadores sensibles en respuestas.
    Implementar controles de acceso a nivel de backend.
    Registrar y monitorear accesos anómalos.

Conclusión

La aplicación crAPI presenta una vulnerabilidad crítica de tipo BOLA que permite acceder a información de otros usuarios mediante la manipulación de identificadores en los endpoints.

Esto demuestra la importancia de implementar controles de autorización robustos en APIs modernas.
