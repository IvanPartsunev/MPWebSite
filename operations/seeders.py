"""Seeders operations"""
import operations.users
import operations.roles
import configuration


def seed_default_user():
    if len(operations.users.get_users()) == 0:
        default_user = configuration.DefaultUser()
        new_user = operations.users.create_user(
            first_name=default_user.first_name,
            last_name=default_user.last_name,
            email=default_user.email,
            phone_number=default_user.phone_number,
            password=default_user.password)
        admin_role = operations.roles.create_role("ADMIN", new_user.id)
        operations.users.add_user_to_role(user_id=new_user.id, role_id=admin_role.id, added_by=new_user.id)