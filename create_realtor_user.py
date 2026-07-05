"""
Crea (o actualiza) un usuario del PORTAL REALTOR en MongoDB.

El login del realtor (streamlit_authenticator) exige un documento en la
coleccion 'users' de la base 'smartbids' con:
  - email     (str)
  - name      (str)
  - password  (hash bcrypt, str)
  - verified  (True)

Uso (desde la carpeta realtor-main/realtor-main, con su venv):
  .\.venv\Scripts\python.exe create_realtor_user.py <email> "<Nombre>" <password>

Lee MONGO_AUTH del archivo .env de esta misma carpeta.
"""
import os
import sys
import bcrypt
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))


def main():
    if len(sys.argv) != 4:
        print('Uso: python create_realtor_user.py <email> "<Nombre>" <password>')
        sys.exit(1)

    email, name, password = sys.argv[1], sys.argv[2], sys.argv[3]

    mongo_auth = os.environ.get("MONGO_AUTH")
    if not mongo_auth or "REEMPLAZAME" in mongo_auth:
        print("ERROR: MONGO_AUTH no esta configurado en .env (todavia dice REEMPLAZAME).")
        sys.exit(1)

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    client = MongoClient(mongo_auth)
    users = client["smartbids"]["users"]
    users.update_one(
        {"email": email},
        {"$set": {"email": email, "name": name, "password": hashed, "verified": True}},
        upsert=True,
    )
    client.close()
    print(f"OK: usuario '{email}' creado/actualizado y marcado como verified=True.")
    print("Ya puedes iniciar sesion en el portal realtor con ese email y contraseña.")


if __name__ == "__main__":
    main()
