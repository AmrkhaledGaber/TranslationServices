from fastapi import FastAPI, BackgroundTasks
from transformers import pipeline
from shared.utils.task_manager import TaskManager

app = FastAPI()
task_manager = TaskManager(redis_host="redis", redis_port=6379)
translation_pipeline = pipeline("translation_en_to_ar")

@app.post("/translate/en2ar")
async def translate_en2ar(text: str, background_tasks: BackgroundTasks):
    task_id = task_manager.create_task()
    background_tasks.add_task(perform_translation, task_id, text)
    return {"task_id": task_id}

@app.get("/translate/en2ar/status/{task_id}")
async def check_status(task_id: str):
    return task_manager.get_status(task_id)

def perform_translation(task_id, text):
    try:
        translated_text = translation_pipeline(text)[0]["translation_text"]
        task_manager.update_task(task_id, result=translated_text)
    except Exception as e:
        task_manager.update_task(task_id, error=str(e))
