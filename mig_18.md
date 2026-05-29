# Checklist técnica de migración Odoo 17 → 18

Este documento reúne una checklist técnica de migración de código desde Odoo 17 hacia Odoo 18, priorizando cambios que afectan módulos personalizados, vistas, seguridad, frontend y validación post-migración. La base principal son fuentes oficiales de Odoo y la wiki de migración de OCA; al final se añade un artículo técnico útil como apoyo para ampliar el listado.[cite:17][cite:23][cite:38][cite:43]

## Fuentes base

- Release Notes oficiales de Odoo 18: <https://www.odoo.com/es/odoo-18-release-notes> [cite:1]
- Guía oficial de upgrade: <https://www.odoo.com/documentation/18.0/administration/upgrade.html> [cite:23]
- Changelog oficial del ORM en Odoo 18: <https://www.odoo.com/documentation/18.0/es_419/developer/reference/backend/orm/changelog.html> [cite:17]
- Referencia oficial del ORM: <https://www.odoo.com/documentation/18.0/es_419/developer/reference/backend/orm.html> [cite:17]
- Referencia oficial de Owl/components: <https://www.odoo.com/documentation/18.0/es_419/developer/reference/frontend/owl_components.html> [cite:39]
- Wiki OCA “Migration to version 18.0”: <https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-18.0> [cite:38]
- Artículo técnico de apoyo: <https://ecosire.com/tr/blog/odoo-migration-v17-to-v18-guide> [cite:43]

## 1. Preparación

- [ ] Generar backup completo de base de datos, filestore y repositorio antes de cualquier prueba de upgrade.[cite:23][cite:43]
- [ ] Levantar un inventario de módulos estándar, OCA, terceros y personalizados instalados en la base actual.[cite:23][cite:43]
- [ ] Identificar integraciones externas, jobs, cron, webhooks, pasarelas de pago y procesos batch que dependan de modelos o endpoints custom.[cite:23][cite:43]
- [ ] Preparar un entorno de ensayo separado para ejecutar la migración y validar sin tocar producción.[cite:23]
- [ ] Revisar si los módulos de comunidad usados ya tienen rama o guía de migración a 18.0 en OCA.[cite:38]

## 2. Python y ORM

### Métodos de búsqueda

- [ ] Revisar overrides de `_name_search`; en Odoo 18 la búsqueda por nombre se implementa mediante `_search_display_name`.[cite:17][cite:38]
- [ ] Revisar cualquier lógica que dependa de `display_name`, `name_search()` o búsquedas por nombre implícitas.[cite:17]

### Accesos y reglas

- [ ] Sustituir llamadas separadas a `check_access_rights()` y `check_access_rule()` por `check_access()` donde corresponda.[cite:17][cite:38]
- [ ] Sustituir `_filter_access_rule()` y `_filter_access_rule_python()` por `_filter_access()`.[cite:17][cite:38]
- [ ] Reemplazar `self.user_has_groups(...)` por `self.env.user.has_group(...)` en código custom.[cite:38]

### Dominios, SQL y utilidades ORM

- [ ] Buscar cualquier uso de `inselect`; Odoo 18 lo elimina y debe reemplazarse por `in` con `Query` u objetos SQL.[cite:17]
- [ ] Auditar SQL directo, helpers low-level y cualquier personalización que dependa del comportamiento interno del ORM.[cite:17]
- [ ] Revisar importaciones antiguas de `registry`; OCA recomienda usar `Registry` desde `odoo.modules.registry`.[cite:38]

### Copias, recursión y campos

- [ ] Reemplazar `_check_recursion()` por `_has_cycle()`.[cite:38]
- [ ] Revisar overrides de `copy()` y `copy_data()`; en 18 `copy_data` devuelve una lista y ambos métodos soportan multi-recordsets.[cite:38]
- [ ] Reemplazar el atributo de campo `group_operator` por `aggregator`.[cite:38]
- [ ] Validar dominios y búsquedas sobre campos related no almacenados; en 18 pueden lanzar excepción en lugar de advertencia.[cite:38]
- [ ] Evaluar migrar traducciones de `_(...)` a `self.env._(...)` donde OCA lo recomienda por consistencia y rendimiento.[cite:38]

## 3. XML y vistas

### Tipos de vista

- [ ] Reemplazar etiquetas `<tree>` por `<list>` en las vistas XML.[cite:38][cite:43]
- [ ] Mantener los XML IDs existentes aunque contengan la palabra `tree`, para evitar romper dependencias externas.[cite:38]
- [ ] Revisar acciones, contexto y código custom que haga referencia textual al tipo de vista `tree`.[cite:38][cite:43]
- [ ] Evaluar ejecutar `odoo-bin upgrade_code` sobre addons propios para detectar reemplazos mecánicos soportados por Odoo.[cite:38]

### Formularios y chatter

- [ ] Revisar que las vistas `form` conserven una estructura compatible y, cuando aplique, incluyan `sheet` correctamente.[cite:43]
- [ ] Reemplazar bloques clásicos de chatter con `<div class="oe_chatter">` por `<chatter/>` donde corresponda.[cite:38]
- [ ] Limpiar campos puestos solo como invisibles para expresiones auxiliares si Odoo 18 ya los inyecta automáticamente.[cite:38]

### Acciones y navegación

- [ ] Revisar `ir.actions.act_window` y usar `path` cuando aplique para rutas más limpias y consistentes.[cite:38]

## 4. JavaScript, assets y Owl

- [ ] Revisar componentes frontend basados en Owl según la documentación oficial de Odoo 18.[cite:39]
- [ ] Eliminar `/** @odoo-module **/` donde ya no sea necesario según la guía de migración de OCA.[cite:38]
- [ ] Adaptar componentes que usen ciclos de vida antiguos, moviendo lógica a `setup()` y hooks como `onWillStart` cuando corresponda.[cite:39][cite:43]
- [ ] Revisar acceso a servicios y RPC en componentes custom, priorizando el patrón basado en `env.services` descrito por Owl/Odoo.[cite:39][cite:43]
- [ ] Auditar `web.assets_backend`, `web.assets_frontend` y otros bundles definidos en `__manifest__.py`.[cite:39][cite:43]
- [ ] Revisar tours y tests JS; OCA indica cambios en el uso de `extra_trigger`.[cite:38]

## 5. Seguridad

- [ ] Revisar `ir.model.access.csv`, record rules y grupos para asegurar que la semántica de acceso sigue siendo correcta en 18.[cite:17][cite:38]
- [ ] Validar manualmente flujos donde el código custom aplicaba permisos de forma explícita antes de leer, escribir, crear o borrar.[cite:17][cite:38]
- [ ] Comprobar accesos en portales, website y controladores si hay endpoints custom que consulten modelos protegidos.[cite:23][cite:43]

## 6. Datos y modelos

- [ ] Revisar si módulos o modelos usados fueron fusionados, renombrados o retirados en la nueva versión.[cite:1][cite:38][cite:43]
- [ ] Inspeccionar cambios de campos, constraints y tablas en módulos críticos del proyecto antes de migrar scripts propios.[cite:38][cite:43]
- [ ] Si existe acceso directo a `ir.property`, revisar el cambio de almacenamiento indicado por guías técnicas de migración.[cite:43]
- [ ] Para proyectos con mucha personalización, revisar análisis por módulo en OpenUpgrade/OCA cuando exista soporte para 18.0.[cite:38]

## 7. Módulos personalizados

- [ ] Actualizar `__manifest__.py` a versión 18.0.x.x.x y revisar dependencias de cada addon.[cite:38]
- [ ] Eliminar restos de migraciones viejas y scripts ya no aplicables en carpetas `migrations/` si la estrategia adoptada lo requiere.[cite:38]
- [ ] Revisar reportes QWeb, server actions, datos XML y seguridad en cada módulo custom.[cite:23][cite:43]
- [ ] Probar instalación limpia del módulo en Odoo 18 y luego actualización sobre una base migrada.[cite:23][cite:43]

## 8. Validación funcional y técnica

- [ ] Ejecutar suite de tests existente y corregir regresiones antes de validar usuarios clave.[cite:38][cite:43]
- [ ] Añadir tests en módulos con lógica sensible si la cobertura actual es baja.[cite:38]
- [ ] Validar contabilidad, ventas, compras, inventario, fabricación, portal y reportes según los módulos realmente usados por la empresa.[cite:23][cite:43]
- [ ] Confirmar que cron jobs, colas, integraciones y automatizaciones siguen funcionando tras la migración.[cite:23][cite:43]
- [ ] Revisar logs del servidor y warnings del ORM para detectar incompatibilidades silenciosas.[cite:17][cite:23]

## 9. Priorización sugerida

| Prioridad | Qué revisar primero | Motivo |
|---|---|---|
| Alta | Overrides de ORM, seguridad, dominios, SQL directo | Son los cambios con más riesgo de romper lógica de negocio.[cite:17][cite:38] |
| Alta | Vistas XML `tree` a `list`, chatter y formularios | Son cambios frecuentes y visibles al instalar o actualizar módulos.[cite:38][cite:43] |
| Media | JavaScript/Owl y assets | Afectan backend web, widgets, clientes personalizados y tours.[cite:39][cite:43] |
| Media | Cambios de modelos y módulos fusionados/eliminados | Pueden romper dependencias o scripts de datos.[cite:1][cite:38][cite:43] |
| Baja | Limpieza de traducciones y refactors opcionales | Mejoran calidad, pero no siempre bloquean la migración.[cite:38] |

## 10. Enlaces oficiales a consultar durante la migración

- Release Notes: <https://www.odoo.com/es/odoo-18-release-notes> [cite:1]
- Upgrade oficial: <https://www.odoo.com/documentation/18.0/administration/upgrade.html> [cite:23]
- Changelog ORM: <https://www.odoo.com/documentation/18.0/es_419/developer/reference/backend/orm/changelog.html> [cite:17]
- ORM API: <https://www.odoo.com/documentation/18.0/es_419/developer/reference/backend/orm.html> [cite:17]
- Owl components: <https://www.odoo.com/documentation/18.0/es_419/developer/reference/frontend/owl_components.html> [cite:39]
- OCA migration 18.0: <https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-18.0> [cite:38]

## Nota sobre el artículo de apoyo

Como complemento no oficial, el artículo de ecosire resume cambios que suelen aparecer en proyectos reales de migración 17 → 18 y puede servir para contrastar la checklist técnica con casos prácticos.[cite:43]
