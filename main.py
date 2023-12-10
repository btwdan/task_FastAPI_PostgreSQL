from fastapi import FastAPI
from database import get_comic_id, get_count, get_sum, insert_values, isUser, update_values_rating, update_rating_comic, get_all_comics
from typing import Dict

app = FastAPI( 
    title="newmanga task"
    )

@app.get("/api/comics/{comic_id}/rating/")
async def avg_rating(comic_id: int) -> float:
    '''
    GET запрос для получения рейтинга комикса
    comic_id: int
    return float
    '''
    
    comics = await get_comic_id(comic_id)
    rating = float(comics['rating'])
    return rating

@app.post("/api/ratings/")
async def post_rating(comic_id: int, user_id: int, mark: int) -> Dict[str, str]:
    '''
    POST запрос для создания оценки комикса 
    comic_id: int
    user_id: int
    mark: int
    return Dict[str, str]
    '''

    #Подсчет количества id комиксов для дальнейшей валидации
    count_all_users_comic = await get_all_comics()

    #Валидация
    if mark < 1 or mark > 5 or comic_id < 1 or user_id < 1 or comic_id > count_all_users_comic:
        return {"status": "error", "Exeption": "Invalid data!"} 
    
    #Определение был ли ранее оставлен отзыв пользователем
    IsUser = await isUser(user_id, comic_id)
    if IsUser:
        #Пользователь ранее осталвлял отзыв соотвествено нужно обновить даные
        await update_values_rating(comic_id, user_id, mark)
    else:
        #Пользователь ранее не оставлял отзыв нужно создать запись в бд
        await insert_values(comic_id, user_id, mark)

    #Подсчет среднего арифметического и обновление рейтинга комикса в бд
    count = await get_count(comic_id)
    sum = await get_sum(comic_id)
    rating = round(sum/count, 2)
    await update_rating_comic(comic_id, rating)
    return {"status": "sucsess"} 