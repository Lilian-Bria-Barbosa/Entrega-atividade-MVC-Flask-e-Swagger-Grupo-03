# app.py
from flask import Flask
from models import db
from controllers.task_controller import TaskController
from controllers.user_controller import UserController  # se você ainda usa para CRUD de usuários
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Swagger (template + config)
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Gerenciador de Tarefas API",
            "description": "API REST para gerenciar tarefas (exercício IMPACTA).",
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": ["http"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "definitions": {
            "Task": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "title": {"type": "string", "example": "Pagar contas"},
                    "description": {"type": "string", "example": "Pagar luz e água"},
                    "status": {"type": "string", "example": "Pendente"},
                    "user_id": {"type": "integer", "example": 1},
                    "user_name": {"type": "string", "example": "Alice"}
                }
            },
            "TaskInput": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "example": "Nova tarefa"},
                    "description": {"type": "string", "example": "Detalhes da tarefa"},
                    "status": {"type": "string", "example": "Pendente"},
                    "user_id": {"type": "integer", "example": 1}
                },
                "required": ["title", "user_id"]
            }
        }
    }
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    Swagger(app, template=swagger_template, config=swagger_config)

    # Inicializa DB
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Rotas REST de tarefas
    app.add_url_rule("/tasks", view_func=TaskController.list_tasks, methods=["GET"], endpoint="list_tasks")
    app.add_url_rule("/tasks", view_func=TaskController.create_task, methods=["POST"], endpoint="create_task")
    app.add_url_rule("/tasks/<int:task_id>", view_func=TaskController.update_task, methods=["PUT"], endpoint="update_task")
    app.add_url_rule("/tasks/<int:task_id>", view_func=TaskController.delete_task, methods=["DELETE"], endpoint="delete_task")

    # (Opcional) Rotas de usuários se quiser manter algo exposto como API
    # app.add_url_rule("/users", view_func=UserController.list_users, methods=["GET"], endpoint="list_users")
    # app.add_url_rule("/users", view_func=UserController.create_user, methods=["POST"], endpoint="create_user")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
