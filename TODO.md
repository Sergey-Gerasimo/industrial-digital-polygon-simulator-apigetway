# ТЗ на API-GetWay для индустриального симулятора

## Требования
API должно только имплементировать ручки (список ниже) и возвращать тестовые данные. Образ контейнера дожен быть скопилирован и выложен github тобы можно было его склонировать прямо в docker-compose (надо настроить ci/ci/cd процесс!). 

ВСЕ ПЕРЕМЕННЫЕ ДОЛЖНЫ БРАТЬСЯ И ПЕРЕМЕННЫХ ОКРУЖЕНИЯ!!!!

Код дожен быть написан а асинхронном фрейморке(желательно на python3 и fastapi). 

Пакет должен содержать README.md и pyproject.toml (я делаю с poetry)

Пример репозитория: https://github.com/Sergey-Gerasimo/gRPC-JWT-AuthService

## Ручки api
### Ручки аутинтификации
- POST `auth/registrate` - регистрация пользователя
    Принимате структуру `AuthResquest` и возрващает `TokenResponse` 

- POST `auth/login` - вход в систему. 
    Принимает `AuthRequets` и возрващает  `TokenResponse`

- POST `auth/refresh` - перевыпуск токена
    Принимает  `RefreshTokenRequest` и возвращает `TokenResponse`

- POST `auth/logout` - выход из системы
    Принимате Ничего (только токен в head запроса) и возвращает  `SuccessResponse`

- GET `auth/me` - получение текущего пользователя
    Принимает ничего (только токен в head запроса) и возвращает `User`

- POST `auth/verify-token` - проверяет токен на валидность
    Принимает ничего(только токен в head запроса) и возвращает `SuccsessResponse`

- POST `auth/change-password` - изменяет пароль у пользователя
    Принимает `ChangePasswordRequest` (и токен в head запроса) и возвращает `SuccsessResonse`

### Ручки управления пользователями
- GET `users/me` - получение текущего пользователя
    Принимает `ничего` (только токена в head запроса) и возвращает `User`

- PUT `users/me` - изменяет текущего пользователя
    Принимает `ChangeUserRequest` (и токен в head запроса) и возвращает `User`

- POST `users` - создает пользователя (может использовать пользователь с правами администратора)
    Принимает `UserCreateRequest` (с токеном в head запроса) и возвращает `User`

- GET `users` - отдает список полльзователей (может использовать пользователь с правами администратора)
    Принимает `GetAllUsersRequest`(c токеном в head запроса) и возвращает `GetAllUsersResponse` 

- GET  `users/{user_id}` - отдает пользователя по id (может использовать пользователь с правами администратора)
     Принимает только  `user_id` в запроса (и токен в head запроса) и возвращает `User`

- DELETE `users/{user_id}` - удаляет пользователя по id (может использовать пользователь с правами администратора)
    Принимает только `user_id` в запросе (и токен в head запроса) и возвращает `SuccsessRepsonse`

- PUT `users/{user_id}` - изменяет пользователя по id (может использовать пользователь с правами администратора)
    Принимает только `ChangeUserRequest` и `user_id` в запросе (и токен в head запроса) и возвращает `User`

- POST `users/{user_id}/deactivate` - изменяет флаг is_active в false у пользователя с id=user_id. (может использовать пользователь с правами администратора)
    Принимает только `user_id` в запросе (и токен в head запроса) и возвращает `User`

- POST `users/{user_id}/activate` - изменяет флаг is_active в true у пользователя с id=user_id. (может использовать пользователь с правами администратора)
    Принимает только `user_id` в запросе (и токен в head запроса) и возвращает `User`

### Ручки игровых комнат

- GET `rooms` - отдает список всех комнат (может использовать пользователь с правами администратора)
    Принимает `GetAllRoomsRequest` (токен в head запроса) и возвращает `GetAllRoomsResponse`

- GET `rooms\my` - отдает список всех комнат текущего пользователя
    Принимает `GetAllRoomsRequest` (токен в head запроса) и возвращает `GetAllRoomsResponse`

- POST `rooms` - создает комнату 
    Принимает  `CreateRoomRequest` (и токен в head запроса) и возвращает `Room` 

- POST `rooms/my` - получить комнаты пользователя
    Принимает `ничего` (токен в head запроса) и возвращает `GetMyRoomsResponse`

- POST `rooms/{room_id}/invite` - пригласить пользователя
    Принимает `room_id` и  `InviteToRoomRequest` (токен в head заопроса) и возвращает `Invation`

- POST `rooms/{room_id}/join` - вступить в комнату
    Принимает `room_id` и  `JoinToRoomRequest` (токен в head заопроса) и возвращает `Room`

- DELETE `rooms/{room_id}/members/{user_id}` - исключить игрока (может только создатель комнаты)
    Принимает `room_id` и `user_id` (токен в head заопроса) и возвращает `SuccsessResponse`

- DELETE `rooms/{room_id}/members/me` - покинуть комнату
    Принимает `room_id` (токен в head заопроса) и возвращает `SuccsessResponse`

- POST `rooms/{room_id}` - покинуть информацию о комнате
    Принимает `room_id` (токен в head заопроса) и возвращает `Room`

### Ручки приглашений
- GET `invites/my` - возвращает приглашения пользователя
    Принимает `GetMyInvitesRequest` (токен в head запроса) и возвращает `GetMyInvitesResponse`

### Ручки моинторинга (эти ручки формируются автоматически при добавлении мониторинга. пока не реализовывать)
- GET `metrics` - отдает собираемые метрики работы приложения 
    Получает `ничего` и возвращает json-строке, сгенерированною автоматически


## Типы данных

- `AuthResquest`
    ```json 

    {
        username: string
        password: string
    }

    ```

-  `TokenResponse`
```json 
{
    success: bool 
    message: string
    timestamp: string(iso format)
    access_token: Token
    refresh_token: Token
    user: User
}
```

- `Token`
``` json
{
    token: string
    token_type: string
    expires_in: int
}
```
- `User`
```json 
{
    username: string 
    user_role: string
    user_id: string
    is_active: bool
    created_at: string
    updated_at: string
}

```

- `SuccessResponse`
```json 
{
    success: bool 
    message: string 
    timestmap: string
}
```

- `RefreshTokenRequest`
```json 
{
    refresh_token: Token
}
```

- `ChangePasswordRequest`
```json 
{
    current_password: string
    new_password: string
}

```

- `ChangeUserRequest`
```json 
{
    user_id: string
    user_role: string // optional
    username: string // optional 
    is_active: bool // optional 
}
```

- `UserCreateRequest`
```json 
{
    user_role: string
    username: string
    username: string
    is_active: bool
}

```

- `GetAllUsersRequest`
```json 
{
    is_active: bool // optional
    role: string // optional 
    limit: int // 50 by default
    offset: int // 0 by default
}
```

- `GetAllUsersResponse`
```json 
{
    success: bool 
    timestamp: string(iso-format)
    users: [User, ...]
    total_count: int
}
```

- `Room`
```json 
    room_name: string
    room_id: string 
    created_at: string(iso-format)
    is_closed: bool
    is_ready: true
    players: [
        {
            user_id: string
            geme_role: string
    
        }
    ]

```
- `GetAllRoomsRequest`
```json 
{
    is_closed: bool // optional
    is_ready: bool // optional 
    limit: int // 50 by default
    offset: int // 0 by default
}

```

- `GetAllRoomsResponse`
```json 
{
    success: bool 
    timestamp: string(iso-format)
    rooms: [Room, ...]
    total_count: int
}

```

- `CreateRoomRequest`
```json 
{
    room_name: string
}

```

- `GetMyRoomsResponse`
```json 
{
    success: bool 
    timestamp: string(iso-format)
    rooms: [Room, ...]
    total_count: int
}
```
- `InviteToRoomRequest`

```json 
{
    user_name: string
    player_role: string

}
```

- `JoinToRoomRequest`

```json 
{
    ct: string (invation token)
}
```

- `Invation`
```json 
{
    invite_id: string 
    inviter_id: string
    room_id: string
    receiver_id: string
    player_role: string
    is_accepted: bool 
    created_at: string (iso-format)
    updated_at: string (iso-format)
    ct: string (invation token)
}
```

-  `GetMyInvitesRequest`

```json
{
    inviter_id: string //optional
    player_role: string //optinal
    is_accepted: bool //optional
}
```


-  `GetMyInvitesResponse`

```json
{
    success: bool 
    timestamp: string(iso-format)
    invations: [Invation, ...]
    total_count: int
}

```