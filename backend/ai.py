from sentence_transformers import SentenceTransformer, util

def recommend_tasks(tasks, mode="default"):
    text_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    difficulty_model = SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")
    impact_model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")
    
    priority_references = {
        "urgent": "Tugas dengan deadline mendesak",
        "daily": "Tugas harian",
        "progress": "Tugas yang hampir selesai dan perlu diselesaikan",
        "impact": "Tugas dengan dampak besar"
    }
    priority_reference = priority_references.get(mode, "Tugas dengan deadline mendesak")
    
    important_keywords = ["bug", "error", "urgent", "segera", "deadline", "hari ini", "besok"]
    
    status_weights = {"Pending": 1.0, "In Progress": 0.7, "Completed": 0.3}
    
    mode_weights = {
        "urgent": {"text": 0.4, "priority": 0.3, "keyword": 0.3, "status": 0.2, "progress": 0.2},
        "impact": {"text": 0.3, "impact": 0.4, "priority": 0.2, "status": 0.2, "progress": 0.1},
        "progress": {"text": 0.2, "priority": 0.2, "status": 0.3, "progress": 0.5},
        "daily": {"text": 0.3, "difficulty": 0.3, "priority": 0.2, "status": 0.2, "progress": 0.1},
    }
    
    weights = mode_weights.get(mode, mode_weights["urgent"])
    
    task_scores = []
    
    for task in tasks:
        text_score = util.pytorch_cos_sim(text_model.encode(task.title), text_model.encode(priority_reference)).item()
        difficulty_score = util.pytorch_cos_sim(difficulty_model.encode(task.description), difficulty_model.encode("Tugas sulit")).item()
        impact_score = util.pytorch_cos_sim(impact_model.encode(task.title), impact_model.encode("Dampak besar" if mode == "impact" else "Dampak kecil")).item()
        priority_weight = 1 / (task.priority + 0.1)
        keyword_bonus = sum(1.0 for word in important_keywords if word in task.title.lower() or word in task.description.lower())
        status_score = status_weights.get(task.status, 0.5)
        progress_score = (100 - task.progress) / 100
        
        final_score = (
            text_score * weights.get("text", 0) +
            difficulty_score * weights.get("difficulty", 0) +
            impact_score * weights.get("impact", 0) +
            priority_weight * weights.get("priority", 0) +
            keyword_bonus * weights.get("keyword", 0) +
            status_score * weights.get("status", 0) +
            progress_score * weights.get("progress", 0)
        )
        
        task_scores.append((task, final_score))
    
    task_scores.sort(key=lambda x: x[1], reverse=True)
    
    return [task for task, _ in task_scores]
