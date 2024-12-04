from flask import Flask, render_template, request
from flask import redirect, url_for, session, flash, jsonify
from models import db, setup_db, Task
from datetime import datetime
#Importamos las librerias que vamos a utilizar 


#Creamos nuestra app donde inicializamos Flask y configuramos nuestra llave 
def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='tsp2024'
    #Realizamos la conexion con nuestra db y SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///app.db'
    setup_db(app)#Inicializamos nuestra db con setup

    #Creamos el primer endpoint 
    @app.route('/')
    #Definimos nuestra función INDEX
    def index():
        pending_tasks = Task.query.filter_by(completed=False).all() #Llamamos a nuestras tareas pendientes mediante una consulta filtrada 
        return render_template('index.html',tasks = pending_tasks)#Regresamos las tareas pendientes en el formato especificado

    #Nuevo endpoint  para nuestras tareas  
    @app.route('/task',methods=['POST'])#Llamada al metodo POST
    #Definimos nuestra función crear Tarea
    def create_task():
        title = request.form.get('title')#Solicitamos el titulo para neustra tarea
        description = request.form.get('description','')#Solicitamos la descripciónn de nuiestra tarea
        #Si nos han proporcionado un titulo entonces podemos proceguir
        if title:
            new_task = Task(title = title, description = description) #De models llamamos a TASK para que cree nuestra tarea en la base de datos
            db.session.add(new_task)#Agregamos una nueva tarea a la lista
            db.session.commit()#Mandamos la tarea despues de agregarla 
            flash('Tarea creada con éxito','success')#Mensaje de respuesta
            return redirect(url_for('index'))
        #Si no nos han proporcionado un titulo mandamos un error y redireccionamos a index
        else:
            flash('Agrega un titulo a la Tarea','error')
            return redirect(url_for('index'))
        
    #Creamos un nuevo endpoint para las tareas pendientes 
    @app.route('/tasks/pending',methods=['GET']) #Llamamos al metodo GET
    #Definimos nuestra funcion de tareas pendientes
    def get_pending_tasks():
        pending_tasks = Task.query.filter_by(completed = False).all()#Realizamos una consulta de las tareas pendientes
        return jsonify([{'id': task.id,'title': task.title,'description': task.description}for task in pending_tasks])#Mandamos la tarea en formato JSON
    
    #Nuevo Endpoint para las tareas completadas
    @app.route('/tasks/complete/<int:id>', methods = ['PUT','POST'])#Llamamos el metodo PUT
    
    #Definimos nuestra funcion PARA TAREAS COMPLETADAS
    def complete_task(id):
        task = Task.query.get(id)#Obtenemos de la tabla el ID
        #Si la tarea a sido completada entonces podemos seguir
        if task:
            task.completed = True
            task.completion_date = datetime.utcnow()
            db.session.commit()
            flash('Tarea completada con exito', 'success')
            return redirect(url_for('index'))
        #Si no existe tareas completadas entonces mandamos un error
        else: 
            flash('Tarea no encontrada','error')
            return redirect(url_for('index'))
        
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug = True)