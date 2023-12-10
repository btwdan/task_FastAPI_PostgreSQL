import asyncpg

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

#Подключение к бд
async def connect_to_db():
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

async def  get_all_comics() -> int:
    '''
    Получение количества комиксов
    return int
    '''

    conn = await connect_to_db()
    query = "SELECT COUNT(id) FROM comic"
    count = await conn.fetchval(query)
    await conn.close()
    return count

async def get_comic_id(comic_id: int) -> float:
    '''
    Получение комикса по id
    return float
    '''

    conn = await connect_to_db()
    query = "SELECT * FROM comic WHERE id = $1"
    comic = await conn.fetchrow(query, comic_id)
    await conn.close()
    return comic

#Получение общего количества оценок комикса(для подсчета ср. ариф.)
async def get_count(comic_id: int) -> int:
    '''
    Получение общего количества оценок комикса(для подсчета ср. ариф.)
    comic_id: int
    return int
    '''

    conn = await connect_to_db()
    query = "SELECT COUNT(comic_id) FROM rating WHERE id = $1"
    count = await conn.fetchval(query, comic_id)
    await conn.close()
    return count

async def get_sum(comic_id: int) -> int:
    '''
    Получение суммы всех оценок комикса(для подсчета ср. ариф.)
    comic_id: int
    return int
    '''

    conn = await connect_to_db()
    query = "SELECT SUM(mark) FROM rating WHERE id = $1"
    sum = await conn.fetchval(query, comic_id)
    await conn.close()
    return sum

#Занесение в rating 
async def insert_values(comic_id: int, user_id: int, mark: int) -> None:
    '''
    Занесение в rating
    comic_id: int
    user_id: int
    mark: int
    return None
    '''

    conn = await connect_to_db()
    query = "INSERT INTO rating (comic_id, user_id, mark) VALUES ($1, $2, $3)"
    await conn.execute(query, comic_id, user_id, mark)
    await conn.close()

#Определение оставлял ли пользователь ранее отзыв на комикс
async def isUser(user_id: int, comic_id: int) -> bool:
    '''
    Получение комикса по id
    user_id: int
    comic_id: int
    return bool
    '''

    conn = await connect_to_db()
    query = "SELECT COUNT(user_id) FROM rating WHERE user_id = $1 AND comic_id = $2"
    count = conn.fetchval(query, user_id, comic_id)
    await conn.close()
    if count == 1:
        return True
    else:
        return False
    
#Обновление оценки комикса если ранее был отзыв
async def update_values_rating(comic_id: int, user_id: int, mark: int) -> None:
    '''
    Получение комикса по id
    comic_id: int
    user_id: int
    mark: int
    return None
    '''

    conn = await connect_to_db()
    query = "UPDATE rating SET mark = $1 WHERE comic_id = $2 AND user_id = $3"
    await conn.execute(query, mark, comic_id, user_id)
    await conn.close()

#Обновление рейтинга комикса
async def update_rating_comic(comic_id: int, new_rating: float) -> None:
    '''
    Получение комикса по id
    comic_id: int
    new_rating: float
    return None
    '''
    
    conn = await connect_to_db()
    query = "UPDATE comic SET rating = $1 WHERE id = $2"
    await conn.execute(query, new_rating, comic_id)
    await conn.close()