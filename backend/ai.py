from sentence_transformers import SentenceTransformer, util

def recommend_tasks(tasks):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    priority_reference = "Tugas dengan deadline mendesak"

    important_keywords = ["bug", "error", "urgent", "segera", "deadline", "hari ini", "besok"]
    
    task_scores = []

    for task in tasks:
        # Skor kemiripan teks
        text_score = util.pytorch_cos_sim(
            model.encode(task.title), model.encode(priority_reference)
        ).item()

        # Bobot prioritas (Semakin kecil angka priority, semakin tinggi bobotnya)
        priority_weight = 1 / task.priority  

        # Tambahkan bobot tambahan jika ada kata kunci penting
        keyword_bonus = sum(1.0 for word in important_keywords if word in task.title.lower() or word in task.description.lower())

        # Skor akhir = kombinasi teks + prioritas + bonus kata kunci
        final_score = text_score * 0.5 + priority_weight * 0.3 + keyword_bonus * 0.2

        task_scores.append((task, final_score))

    # Urutkan berdasarkan skor akhir (descending)
    task_scores.sort(key=lambda x: x[1], reverse=True)

    return [task[0] for task in task_scores]
