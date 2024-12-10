import db.connection
import db.models
import configuration


def get_all_roles():
    with db.connection.get_session() as session:
        return session.query(db.models.Role)


def create_role(name: str, created_by: str):
    with db.connection.get_session() as session:
        new_role = db.models.Role(name=name, created_by=created_by)
        session.add(new_role)
        session.commit()
        session.refresh(new_role)
        return new_role
