from flask import Flask, request, jsonify
from transformers import pipeline
from shared.utils.task_manager import TaskManager

app = Flask(__name__)
task_manager = TaskManager(redis_host="redis", redis_port=6379)
translation_pipeline = pipeline("translation_ar_to_en")

@app.route('/translate/ar2en', methods=['POST'])
def translate_ar2en():
    task_id = task_manager.create_task()
    text = request.json.get("text", "")
    try:
        translated_text = translation_pipeline(text)[0]["translation_text"]
        task_manager.update_task(task_id, result=translated_text)
    except Exception as e:
        task_manager.update_task(task_id, error=str(e))
    return jsonify({"task_id": task_id})

@app.route('/translate/ar2en/status/<task_id>', methods=['GET'])
def check_status(task_id):
    return jsonify(task_manager.get_status(task_id))
