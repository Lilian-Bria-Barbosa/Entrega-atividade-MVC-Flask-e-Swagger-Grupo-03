import os
from flask import Flask
from config import Config # importa as 
from controllers.user_controller import UserController
from controllers.task_controller import TaskController
from models import db

app = Flask(__name__, template_folder=os.path.join('view', 'templates'))
app.config.from_object(Config)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# inicializa o banco de dados
db.init_app(app)

# cria tabelas

with app.app_context():
    db.create_all()

# forma alternativa de criar rotas, parâmetros: rota em si, endpoint interno do flask e função a ser executada quando a URL for acessada
app.add_url_rule("/users", view_func=UserController.list_user, endpoint="list_user")
app.add_url_rule("/users/new", view_func=UserController.create_user, methods=["GET", "POST"])


# Rotas Tarefas
app.add_url_rule("/tasks", view_func=TaskController.list_tasks, endpoint="list_tasks")
app.add_url_rule("/tasks/new", view_func=TaskController.create_task, methods=["GET", "POST"], endpoint="create_task")
app.add_url_rule("/tasks/update/<int:task_id>", view_func=TaskController.update_task_status, methods=["POST"], endpoint="update_task_status")
app.add_url_rule("/tasks/delete/<int:task_id>", view_func=TaskController.delete_task, methods=["POST"], endpoint="delete_task")


if __name__ == '__main__':
    app.run(debug=True, port=5002)