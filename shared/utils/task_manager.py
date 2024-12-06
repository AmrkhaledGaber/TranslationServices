import uuid
import redis
import json

class TaskManager:
    def __init__(self, redis_host="localhost", redis_port=6379):
        self.client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

    def create_task(self):
        task_id = str(uuid.uuid4())
        self.client.set(task_id, json.dumps({"status": "Processing", "result": None}))
        return task_id

    def update_task(self, task_id, result=None, error=None):
        task = self.client.get(task_id)
        if not task:
            return False
        task_data = json.loads(task)
        if error:
            task_data.update({"status": "Error", "result": str(error)})
        else:
            task_data.update({"status": "Completed", "result": result})
        self.client.set(task_id, json.dumps(task_data))
        return True

    def get_status(self, task_id):
        task = self.client.get(task_id)
        if not task:
            return {"status": "Invalid Task ID", "result": None}
        return json.loads(task)
