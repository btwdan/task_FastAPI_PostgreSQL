from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#Тестирование бд на коректность вывода
def test_get_avg_rating():
    for i in range(1, 6):
        response = client.get(f"/api/comics/{i}/rating/")
        #Определение записей которые были уже оценены
        if i == 1 or i == 3:
            assert response.status_code == 200
            assert response.json() == 5.0  
        #Определение записей которые не были уже оценены
        else:
            assert response.status_code == 200
            assert response.json() == 0.0

#Тестирование POST запроса на некорретные данные
async def test_post_rating_invalid_data():
    client = TestClient(app)
    data = {
        "comic_id": 1000,  # Указываем некорректный ID комикса
        "user_id": 0,      # Указываем некорректный ID пользователя
        "mark": 6          # Указываем некорректную оценку
    }
    
    response = await client.post("/api/ratings/", json=data)
    assert response.status_code == 200
    assert response.json() == {"status": "error", "Exeption": "Invalid data!"}

#Тестирование POST запроса на корретные данные
async def test_post_rating_correct_data():
    client = TestClient(app)
    data = {
        "comic_id": 1,      # Указываем корректный ID комикса
        "user_id": 1,       # Указываем короректный ID пользователя
        "mark": 4           # Указываем корректную оценку
    }
    
    response = await client.post("/api/ratings/", json=data)
    assert response.status_code == 200
    assert response.json() == {"status": "sucsess"} 