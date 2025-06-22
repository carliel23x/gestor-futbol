# Gestor de Equipo de Fútbol

## Descripción

Este proyecto es una aplicación de escritorio desarrollada en Python con `tkinter` que permite gestionar un equipo de fútbol. Está diseñada para ser sencilla, visual e interactiva, permitiendo registrar jugadores, crear partidos, generar alineaciones válidas y visualizar estadísticas de rendimiento como goles, asistencias y un ranking de jugadores.

El sistema organiza sus funcionalidades en diferentes pestañas, permitiendo una navegación clara y ordenada.

## Funcionalidades

- **Gestión de jugadores**  
  Agrega, edita y lista jugadores con nombre, número, posición, goles y asistencias.

- **Rating de jugadores**  
  Ordena automáticamente los jugadores por desempeño (goles y asistencias) en una tabla comparativa.

- **Organización de partidos**  
  Crea partidos con equipos, fecha y hora. Calcula y muestra el tiempo restante para cada uno por separado.

- **Alineaciones**  
  Permite seleccionar jugadores para una alineación válida (1 portero obligatorio y máximo 11 en total). Guarda y muestra todas las alineaciones.

- **Configuración**  
  Permite borrar jugadores, partidos, alineaciones individualmente o eliminar todo con un solo botón.

## Paradigmas de Programación Utilizados

- **Imperativo**:  
  Se emplean estructuras clásicas como bucles, condicionales y manejo de eventos en `tkinter`.

- **Funcional**:  
  Se usan funciones puras para filtrado, ordenamiento de listas, y cálculo de rankings o tiempos restantes.

- **Asincrónico / Reactivo**:  
  Se actualiza en tiempo real el tiempo restante para cada partido usando `after()` de `tkinter` para simular comportamiento asincrónico.

## Tecnologías

- Python 3.10+
- `tkinter` (interfaz gráfica)
- `tkcalendar` (selección de fechas)
- Archivos `.csv` como base de datos local (persistencia ligera)

## Requisitos

- Python instalado
- Instalar `tkcalendar` si no lo tienes:

```bash
pip install tkcalendar
