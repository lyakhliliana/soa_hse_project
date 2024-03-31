import uuid

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from social_network_api.src.models.dao import UserDao, SessionDao
from social_network_api.src.models.dto import RegisterData, SessionKey, UserUpdate
from social_network_api.src.utils.session_maker import get_session
from social_network_api.src.routers.post import post_app

app = FastAPI(title='Social Network API')
app.include_router(post_app)


@app.post('/user', summary='Создать нового пользователя')
async def create_user(
        user_to_post: RegisterData,
        session: AsyncSession = Depends(get_session)
) -> Response:
    user: UserDao = (await session.execute(
        select(UserDao).where(UserDao.login == user_to_post.login))).unique().scalars().one_or_none()
    if user:
        raise HTTPException(status_code=409, detail=f'{user_to_post.login} уже существует.')

    new_user: UserDao = UserDao(login=user_to_post.login, password=user_to_post.password)
    session.add(new_user)
    await session.commit()
    return Response(status_code=201, media_type='text/plain', content='Регистрация успешна!')


@app.put('/user', summary='Обновление информации о пользователе')
async def update_info(
        user_data: UserUpdate,
        session_key: SessionKey,
        session: AsyncSession = Depends(get_session)
):
    # проверка существования пользователя
    user: UserDao = (
        await session.execute(select(UserDao).where(UserDao.login == user_data.login))).unique().scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail=f'{user_data.login} не найден.')

    # проверка доступа
    cur_session: SessionDao = (await session.execute(
        select(SessionDao).where(SessionDao.login == user_data.login))).unique().scalars().one_or_none()
    if not cur_session:
        raise HTTPException(status_code=401, detail=f'Действие недоступно.')
    if str(cur_session.key) != str(session_key.key):
        raise HTTPException(status_code=401, detail=f'Действие недоступно. {cur_session.key}, {session_key.key}')

    # обновление данных
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    await session.commit()
    return Response(status_code=200, media_type='text/plain', content='Данные обновлены.')


@app.post('/user_authentication', response_model=SessionKey, summary='Аутентификация в системе по логину и паролю')
async def authenticate_user(
        user_data: RegisterData,
        session: AsyncSession = Depends(get_session)
) -> SessionKey:
    # проверка логина и пароля на соответствие
    user: UserDao = (
        await session.execute(select(UserDao).where(UserDao.login == user_data.login))).unique().scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail=f'{user_data.login} не найден.')
    if user.password != user_data.password:
        raise HTTPException(status_code=403, detail='Введен неверный пароль.')

    # создание сессионного ключа
    cur_session: SessionDao = (await session.execute(
        select(SessionDao).where(SessionDao.login == user_data.login))).unique().scalars().one_or_none()
    key: uuid.UUID = uuid.uuid4()
    if not cur_session:
        new_session: SessionDao = SessionDao(login=user_data.login, key=key)
        session.add(new_session)
        await session.commit()
    if cur_session:
        await session.execute(update(SessionDao).where(SessionDao.login == user_data.login).values(key=key))
        await session.commit()

    return SessionKey(key=key)
