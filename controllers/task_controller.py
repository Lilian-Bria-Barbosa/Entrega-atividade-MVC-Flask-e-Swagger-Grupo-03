# controllers/task_controller.py
from flask import request, jsonify
from models import db
from models.task import Task
from models.user import User

class TaskController:
    @staticmethod
    def list_tasks():
        """
        Listar tarefas
        ---
        tags:
          - Tasks
        responses:
          200:
            description: Lista de tarefas
            schema:
              type: array
              items:
                $ref: '#/definitions/Task'
        """
        tasks = Task.query.order_by(Task.id.desc()).all()
        payload = [t.to_dict(include_user=True) for t in tasks]
        return jsonify(payload), 200

    @staticmethod
    def create_task():
        """
        Criar tarefa
        ---
        tags:
          - Tasks
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/definitions/TaskInput'
        responses:
          201:
            description: Tarefa criada com sucesso
            schema:
              $ref: '#/definitions/Task'
          400:
            description: Erro de validação
        """
        if not request.is_json:
            return jsonify({"message": "Content-Type deve ser application/json"}), 400
        data = request.get_json()

        title = data.get("title")
        user_id = data.get("user_id")
        description = data.get("description")
        status = data.get("status", "Pendente")

        if not title or not user_id:
            return jsonify({"message": "Campos obrigatórios: title, user_id"}), 400

        # valida se o usuário existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuário não encontrado"}), 404

        task = Task(title=title, description=description, status=status, user_id=user_id)
        db.session.add(task)
        db.session.commit()

        return jsonify(task.to_dict(include_user=True)), 201

    @staticmethod
    def update_task(task_id):
        """
        Atualizar tarefa
        ---
        tags:
          - Tasks
        parameters:
          - in: path
            name: task_id
            type: integer
            required: true
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/definitions/TaskInput'
        responses:
          200:
            description: Tarefa atualizada
            schema:
              $ref: '#/definitions/Task'
          404:
            description: Tarefa não encontrada
        """
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"message": "Tarefa não encontrada"}), 404

        if not request.is_json:
            return jsonify({"message": "Content-Type deve ser application/json"}), 400
        data = request.get_json()

        # atualiza somente se vier no payload
        for field in ("title", "description", "status", "user_id"):
            if field in data and data[field] is not None:
                if field == "user_id":
                    # garante que o novo usuário exista
                    new_user = User.query.get(data[field])
                    if not new_user:
                        return jsonify({"message": "Usuário não encontrado"}), 404
                setattr(task, field, data[field])

        db.session.commit()
        return jsonify(task.to_dict(include_user=True)), 200

    @staticmethod
    def delete_task(task_id):
        """
        Excluir tarefa
        ---
        tags:
          - Tasks
        parameters:
          - in: path
            name: task_id
            type: integer
            required: true
        responses:
          200:
            description: Tarefa excluída
            schema:
              type: object
              properties:
                message:
                  type: string
          404:
            description: Tarefa não encontrada
        """
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"message": "Tarefa não encontrada"}), 404

        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Tarefa excluída com sucesso"}), 200
