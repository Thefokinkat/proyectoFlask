from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#Importamos las librertias que vamos a Utilizar

#Importamos la clase SQLAlchemy para nuestra base de datos
db = SQLAlchemy()

#Inicializamos nuestra db 
def setup_db(app):
    db.init_app(app)
    
#Creamos la clase Task para crear una tabla nueva 
class Task(db.Model):
    #Dentro ponemos las clases que vamos a utilizar
    #id 
    id = db.Column(db.Integer,primary_key=True)
    #title 
    title = db.Column(db.String(100),nullable = False)
    #description 
    description = db.Column(db.String(100), nullable = True)
    #completed 
    completed = db.Column(db.Boolean,default = False)
    #creation_date 
    creation_date = db.Column(db.DateTime, default = datetime.utcnow)
    #completion_date 
    completion_date = db.Column(db.DateTime, nullable = True)
    
    