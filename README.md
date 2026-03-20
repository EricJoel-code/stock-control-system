# 🧦 Sistema de Control de Stock y Gestión de Pedidos – Daos Sport

## 🚀 Overview

Sistema web desarrollado para optimizar la **gestión de inventario**, **pedidos** y **operaciones internas** de la empresa textil *Daos Sport*. La solución permite centralizar la información del negocio, mejorar la trazabilidad y reducir errores operativos.

> 🔐 Aplicación privada orientada a uso interno.

---

## 🎯 Objetivos

* Optimizar el control de inventario en tiempo real
* Automatizar el flujo de pedidos
* Centralizar la información del negocio
* Reducir errores manuales
* Escalar operaciones de forma eficiente

---

## ⚙️ Funcionalidades

### 📦 Gestión de Productos

* CRUD completo de productos
* Control de stock disponible
* Organización por categorías

### 🧾 Gestión de Pedidos

* Registro de pedidos
* Estados del pedido (pendiente, procesado, entregado)
* Relación pedidos-clientes

### 📊 Inventario

* Actualización automática de stock
* Alertas por bajo inventario

### 👥 Usuarios y Roles

* Sistema de roles (administrador / cliente)
* Control de acceso por permisos

### 🔐 Seguridad

* Autenticación basada en sesiones
* Protección de rutas por roles
* Validación de datos de entrada
* Manejo seguro de credenciales (hashing por defecto de Django)

---

## 🧠 Arquitectura

* Arquitectura cliente-servidor
* Patrón MVT (Model - View - Template)
* Separación de responsabilidades

---

## 🛠️ Stack Tecnológico

### ⚙️ Backend

* Django (Python)

### 🗄️ Base de Datos

* PostgreSQL

### 🎨 Frontend

* HTML5 (Templates Django)
* CSS3
* JavaScript

### 🛠️ Herramientas

* Git
* GitHub

---

## 🔍 Enfoque Backend

Este proyecto fue diseñado aplicando principios clave de desarrollo backend:

* Implementación de lógica de negocio para control de inventario (evitando inconsistencias como stock negativo)
* Manejo de relaciones entre entidades (productos, pedidos, usuarios)
* Validación de datos tanto a nivel de formularios como de lógica del sistema
* Uso de Django Signals para automatización de procesos internos
* Control de integridad de datos y consistencia del sistema
* Manejo de estados en pedidos (flujo del sistema: pendiente, procesado, entregado)
* Organización modular del proyecto mediante apps independientes (usuarios, productos, pedidos)

---

## 🔐 Seguridad Aplicada

Se implementaron medidas básicas de seguridad orientadas a aplicaciones web:

* Autenticación de usuarios mediante sesiones
* Autorización basada en roles (control de acceso a funcionalidades)
* Validación y sanitización de entradas del usuario
* Uso de hashing seguro de contraseñas proporcionado por Django
* Protección de vistas y rutas sensibles

---

## 📸 Capturas

<img width="2728" height="1278" alt="login" src="https://github.com/user-attachments/assets/207cb582-a0c7-4da7-86bc-ebf6f38c25a8" />

<img width="1349" height="550" alt="catalog_admin" src="https://github.com/user-attachments/assets/cac1f2f3-fb40-4431-a246-18353bbd429e" />

---

## 📊 Estado del Proyecto

* ✅ Sistema funcional en uso interno
* 🔧 Mejoras futuras:

  * Dashboard analítico
  * Reportes avanzados
  * Integración con facturación

---

## 👨‍💻 Autor

**Eric Joel Cacuango de la Torre**
Backend Developer | Security Focused

---

## 📝 Nota

Proyecto desarrollado para una empresa real. Por motivos de confidencialidad, el acceso público y datos reales no están disponibles.
