# NOTAS SOBRE EL PROYECTO
+ Crear una carpeta para contener al proyecto y al entorno virtual. Por ejemplo: 
Mafalda
 -- mafaldavenv (entorno virtual)
 -- Mafalda (carpeta del proyecto)

+ Los empleados y las empresas(Mafalda) son creados desde el administrador `http://localhost:8000/admin/` por el developer del proyecto que se lo entrega al cliente. Primero crear el superusuario, luego, en el admin, la compañía y por último nuevos usuarios. En la pantalla de creación de usuarios especificar la compañía a la que pertenecen.

+ Crear un registro Parámetro en 0 desde el administrador para que el cliente modifique solo este registro.

+ Modelo Parameters: tiene un único campo: surcharge. Este campo indica el porcentaje de recargo(margen de ganancia) a aplicar por default a todos los productos.

+ Los usuarios solo pueden ver los productos y presupuestos de la empresa a la que pertenecen, auque haya varias empresas creadas.

+ Los presupuestos, productos y clientes poseen un borrado lógico; tienen un campo `active` que por default es `True` y que al borrarlos pasa a ser `False`. Al ejecutar un GET solo muestra los registros que están activos.

+ Para chequear que no haya errores, antes de levantar el servidor de desarrollo ejecutar en la consola `python manage.py check`. Devuelve 'System check identified no issues (0 silenced).' si no hay errores.

+ Los comandos `python manage.py check`, `python manage.py createsuperuser`, `python manage.py runserver` deben correrse en la carpeta donde se bajó el proyecto, la que contiene el archivo manage.py.

+ El proyecto posee un endpoint para hacer búsquedas de productos.

+ No crear productos ni presupuestos desde el admin ya que no hace los cálculos automáticamente de precios. Además pueden mezclarse las compañías, productos, presupuestos, etc entre si (la libreria 1 puede tener en un presupuesto con productos de la libreria 2) La lógica está implementada en las vistas.


---
# CÓMO CORRER EL PROYECTO LOCALMENTE:
 Setear una nueva variable de entorno `MAFALDA_ENV` con el valor `development`
1. Activar el entorno virtual (ver punto siguiente 'creando un entorno virtual')
2. Instalar los requirimientos del proyecto (siempre con el entorno virtual activado)
   * `pip install -r requirements.txt`
3. En la consola ejecutar:
   * `python manage.py migrate`
   * `python manage.py collectstatic`
4. Generar el super usuario para tener acceso al admin. En la consola ejecutar:
   * `python manage.py createsuperuser` ingresar nombre de usuario, contraseña y mail.
5. La primera vez Correr `run.ps1` para levantar el servidor de desarrollo y setear la clave del proyecto
6. Las veces siguientes correr `python manage.py runserver` para levantar el servidor de desarrollo.

--- 

# CREANDO UN ENTORNO VIRTUAL
1. Instalar python 3.7.3
2. Crear una carpeta para contener el entorno virtual y **el proyecto**. (por ej 'mafalda')
3. En la consola, detro de esta carpeta ('mafalda') ejecutar `virtualenv mafaldavenv` siendo 'mafaldavenv' el nombre del entorno virtual.
4. Cuando termine de crearse el entorno virtual, activarlo con el siguiente comando
   * mafalda>> `mafaldavenv/Scripts/activate.bat`

---

# MODELOS DE DATOS

## **Modelo Company** (librería, se crea desde el admin)

    name = CharField(max_length=255, no puede estar en blanco)

    razon_social = CharField(max_length=255)

    commercial_address = CharField(max_length=255)

    iibb = CharField(max_length=11)

    iva_condition =  CharField(max_length=3, Opciones: CONTADO('contado') = 'CTD' ó RESP_INSCR('Responsable Inscripto') = 'RIN', default=CONTADO)

    cuit = CharField(max_length=11, hace una validación sobre este campo: chequea que sea válido el cuit)

    activity_start_date = DateField()


## **Modelo Employee** (usuarios de la aplicación, se crean desde al admin)

    user = OneToOneField(User, Primero se crea el usuario, luego se lo vincula como empleado)
    company = ForeignKey('Company', librería a la que pertenece este usuario)


## **Modelo Parameters** 

    surcharge = DecimalField(max_digits=10, decimal_places=2, default=0)


## **Modelo Client**

    name_bussinessname = CharField(max_length=255, no puede estar en blanco)

    commercial_address = CharField(max_length=255)

    cuit = CharField(max_length=11, hace una validación sobre este campo: chequea que sea válido el cuit)

    iva_condition = CharField(max_length=3, Opciones: INSCR('Inscripto')= 'INS', EXC('Exento')= 'EXC', CF, ('Consumidor Final')='CFI' ,default=CF)

    sale_condition = CharField(max_length=3, Opciones: CONTADO, ('Contado')= 'CTD', CTA_CTE, ('Cuenta Corriente')= 'CCT' , default=CONTADO)

    company = ForeignKey(Empresa que carga el producto)

    active = BooleanField(default=True)

    owner = ForeignKey(instancia de User, se asigna por default al usuario autenticado al momento de creación)


## **Modelo Product** 

    name = CharField(max_length=255, no puede estar en blanco)

    title = CharField(max_length=255, breve descripcion del producto)

    brand = CharField(max_length=255, marca del producto. No puede estar en blanco)

    product_code = CharField(max_length=13)

    wholesaler_code = CharField(max_length=13, código del proveedor)

    iibb = CharField(max_length=25, IIBB del proveedor)

    list_price= DecimalField(max_digits=10, decimal_places=2)

    surcharge = DecimalField(max_digits=10, decimal_places=2, blank=True)

    iva_percentage = DecimalField(max_digits=10, decimal_places=2, default=0)

    company = ForeignKey(Empresa que carga el producto)

    **picture = ImageField(upload_to=None, blank=True, null=True) A desarrollarse en una segunda versión del proyecto.**

    final_price = DecimalField(max_digits=10, decimal_places=2, default=0. Calculado automáticamente)

    active = BooleanField(default=True)

    owner = ForeignKey(instancia de User, se asigna por default al usuario autenticado al momento de creación)


## **Modelo Presupuesto**

    date = DateField() A ingresar por el usuario

    client = ForeignKey(Client, no puede estar en blanco) A ingresar por el usuario

    items = ManyToManyField(Product, A través de la tabla intermedia 'Item') A ingresar por el usuario. Debe vincularse con la vista de búsqueda /search.
    **Este campo debe renderizarse tantas veces como el usuario necesite. Al lado debe haber un campo para ingresar la cantidad. Esta se graba en la tabla intermedia ITEMS.**

    discount = DecimalField(max_digits=10, decimal_places=2, default=0, % del total.)  A ingresar por el usuario

    total_before_discounts = DecimalField(max_digits=10, decimal_places=2, default=0, calculado automáticamente)

    total_after_discounts = DecimalField(max_digits=10, decimal_places=2, default=0, calculado automáticamente. Este es el precio final a pagar por el cliente. Es el total antes de descuentos menos el descuento.)

    total_iva = DecimalField(max_digits=10, decimal_places=2, default=0, calculado automáticamente)

    company = ForeignKey(Empresa que carga el producto)

    active = BooleanField(default=True)

    owner = ForeignKey(instancia de User, se asigna por default al usuario autenticado al momento de creación)


## **Modelo Item**

    presupuesto = ForeignKey(Presupuesto al que pertenece este item)
    product = ForeignKey(Product que se está agregando al presupuesto)
    quantity = IntegerField(CAntidad de este item que se quiere agregar al presupuesto)
    price = DecimalField(max_digits=10, decimal_places=2, default=0. Precio de lista multiplicado por la cantidad)
    iva = DecimalField(max_digits=10, decimal_places=2, default=0. Iva del producto multiplicado por la cantidad)
    final_price = DecimalField(max_digits=10, decimal_places=2, default=0. Precio + iva)

---

# ENDPOINTS
## /admin/
    http://localhost:8000/admin/
Este endpoint se usa para crear librerias(company) y empleados de esas librerias(employee).

## /docs/

    http://localhost:8000/docs/
Este endpoint lista todos los endpoints disponibles y permite ejecutarlos, pasando parámetros si es necesario.

## /get-token/

    http://localhost:8000/get-token/
POST: **devuelve un token necesario para hacer las consultas a los endpoints listados a continuación.**

## /client/

'Headers' requerido: 'Authorization': 'Token 'token-obtenido''


    http://localhost:8000/client/
GET : lista todos los clientes de la librería (a quien se les hace los presupuestos) que hay en la base de datos.
Muestra aquellos que tienen True en el campo 'active'

POST: crea un nuevo cliente en la base de datos

DATOS DE EJEMLPLO: 

name_bussinessname: Pepe S.A.

commercial_address: av siempreviva 123

cuit: 27327667525 (algún cuit válido, chequea que lo sea)

iva_condition: INS

sale_condition: CCT

    http://localhost:8000/client/{id}/
GET: Devuelve el cliente que corresponde al id pasado.

PUT: Modifica el cliente que corresponde al id.

PATCH: Modifica el cliente que corresponde al id.

DELETE: elimina lógicamente el cliente que corresponde al id: cambia 'active' a False.


## /parameters/
'Headers' requerido: 'Authorization': 'Token 'token-obtenido''

Endpoints a usar: 

    http://localhost:8000/parameter/
GET: lista el parámetro

    http://localhost:8000/parameter/{id}/
PUT o PATCH: modificar el parámetro. Debe existir solo un registro. IMPORTANTE! el cliente debería poder modificar solo un registro, no crear nuevos. Al entregar el proyecto, crear un registro con valor 0 para que sea este el que se modifique.


## /presupuesto/
'Headers' requerido: 'Authorization': 'Token 'token-obtenido''

    http://localhost:8000/presupuesto/
GET : lista todos los presupuestos de la librería que hay en la base de datos.
Muestra aquellos que tienen True en el campo 'active'

POST: crea un nuevo presupuesto en la base de datos

DATOS DE EJEMLPLO: 

date: 2019-10-18

discount: 10

items: [{"id":"1","quantity":"2"},{"id":"2","quantity":"1"}]

Al ser items un campo many to many, la relación se da a través de la tabla intermedia `items`.
A este campo se le pasa una lista conteniendo el `id` del producto a agregar y la cantidad de dicho producto(`quantity`).

    http://localhost:8000/presupuesto/{id}/
GET: Devuelve el presupuesto que corresponde al id pasado.

PUT: Modifica el presupuesto que corresponde al id.

PATCH: Modifica el presupuesto que corresponde al id.

DELETE: elimina lógicamente el presupuesto que corresponde al id: cambia 'active' a False.


## /search/

    http://localhost:8000/search/
POST: String. La vista busca en la base de datos de **productos** coincidencias en los campos nombre, titulo y marca. Devuelve una lista de productos

---
# VERSIONES
Python: 3.7.3

Django: 2.2.4

Django rest framework: 3.11.0