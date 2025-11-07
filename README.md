#Levantar el servidor
python manage.py runserver

#Crear un usuario global del sistema
python manage.py createsuperuser

#Luego de crear un tenant registrar el usuario global en el tenant
INSERT INTO nombreTenant.users_tenantuserprofile (user_id, tenant_id, date_joined, is_active)
VALUES (1, 1, NOW(), true);

#Aplicar migraciones globales
python manage.py migrate_schemas --shared

#Aplicar migraciones para empresa
python manage.py migrate_schemas --tenant