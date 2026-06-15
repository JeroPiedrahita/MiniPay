from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#1. Definimos la URL de conexion de la base de datos
# Le dice a SQLalchemy que cree un archivo local en la raiz llamado minipay.db
SQLALCHEMY_DATABASE_URL = "sqlite:///./minipay.db"

# 2. Creamos el Motor (Engine)
# El parametro connect_args es exclusivo y obligatorio para SQLite por manejo de hilos en FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Creamos la fabrica de Sesiones (SessionLocal)
#Cada peticion que llegue a la API abrira una sesion corta para transaccionar
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Creamos la Clase Base de mapeo
# Todos los modelos de tablas que hagamos en el futuro heredaran de esta clase
Base = declarative_base()

#5. Dependencia para inyectar la Base de Datos en los Endpoints
def get_db():
    """
    Abre una conexion con la base de datos por cada peticion HTTP
    y se asegura de cerrarla automaticamente al terminar, evitando fugas de memoria.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()