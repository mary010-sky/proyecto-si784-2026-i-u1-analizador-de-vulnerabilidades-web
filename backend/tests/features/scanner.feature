Feature: Deteccion de vulnerabilidades web
  Como analista de seguridad
  Quiero que el scanner detecte vulnerabilidades en sitios web
  Para generar reportes de riesgo y guias de remediacion

  Scenario: Detectar cabeceras de seguridad faltantes
    Given una pagina sin cabeceras de seguridad configuradas
    When analizo las cabeceras de la pagina
    Then debo encontrar al menos una vulnerabilidad de cabecera faltante

  Scenario: No reportar falsos positivos cuando las cabeceras estan presentes
    Given una pagina con todas las cabeceras de seguridad configuradas
    When analizo las cabeceras de la pagina
    Then no debo encontrar vulnerabilidades de cabecera faltante

  Scenario: Detectar formulario POST sin token CSRF
    Given una pagina con un formulario POST sin token CSRF
    When analizo el CSRF de la pagina
    Then debo encontrar una vulnerabilidad de tipo csrf

  Scenario: No reportar CSRF cuando el formulario tiene token
    Given una pagina con un formulario POST con token CSRF
    When analizo el CSRF de la pagina
    Then no debo encontrar vulnerabilidades de csrf

  Scenario: Detectar Local File Inclusion mediante path traversal
    Given un parametro vulnerable a path traversal
    When pruebo LFI sobre el parametro
    Then debo encontrar una vulnerabilidad de tipo lfi

  Scenario: Detectar archivo .env expuesto
    Given un sitio con el archivo .env accesible publicamente
    When busco archivos sensibles expuestos
    Then debo encontrar una vulnerabilidad de archivo .env expuesto

  Scenario: Construir un hallazgo con los campos correctos
    Given un hallazgo de tipo sqli con severidad high
    When verifico la estructura del hallazgo
    Then el modulo del hallazgo debe ser sqli
    And la severidad debe ser high

  Scenario: Reemplazar un parametro existente en la URL
    Given una URL con parametros de consulta
    When reemplazo el valor de un parametro
    Then el nuevo valor debe aparecer en la URL resultante
