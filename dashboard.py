from langchain_google_genai import ChatGoogleGenerativeAI
import sqlite3
import re
import json

api_key = "AIzaSyBtvoNHT1NoIGI1kp2nN_HGMIRu9LBKFVo"
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)

def create_quiz(task_type):
    with open("prompt.txt") as f:
        prompt = f.read().replace("{{task_type}}", task_type)
        content = llm.invoke(prompt).content
        try:
            quiz_json = json.loads(content)
        except json.JSONDecodeError:
            import re
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                quiz_json = json.loads(match.group(0))
            else:
                raise ValueError("Output model tidak berformat JSON.")

        return quiz_json

def get_user_rank_info(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT id, username, score FROM users ORDER BY score DESC")
    all_users = c.fetchall()

    index = next((i for i, u in enumerate(all_users) if u[1] == username), None)
    rank = index + 1

    user_above = all_users[index - 1] if index is not None and index > 0 else None
    user_below = all_users[index + 1] if index is not None and index < len(all_users)-1 else None

    return all_users[index], user_above, user_below, rank

def update_score(username, is_correct):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT score FROM users WHERE username = ?", (username,))
    result = c.fetchone()

    if not result:
        conn.close()
        return "User tidak ditemukan"

    current_score = result[0]
    if is_correct:
        new_score = current_score + 10
    else:
        new_score = current_score - 10
    if new_score < 0:
        new_score = 0
    c.execute("UPDATE users SET score = ? WHERE username = ?", (new_score, username))
    conn.commit()
    conn.close()

    return new_score


