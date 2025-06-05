# Дизайн CRM для компьютерного клуба

## Структура базы данных (PostgreSQL/SQLite)

### roles
- `id` — PK
- `name` — название роли (`admin`, `operator`, `read-only`)

### users
- `id` — PK
- `username` — логин
- `password_hash` — пароль
- `full_name` — имя оператора
- `phone`
- `role_id` — FK -> roles.id
- `created_at`

### clients
- `id` — PK
- `full_name`
- `phone`
- `balance` — текущее состояние счёта
- `debt` — сумма долгов
- `notes`
- `created_at`

### zones
- `id` — PK
- `name` — Standart, PRO, VIP, PS5 и т.д.

### computers
- `id` — PK
- `zone_id` — FK -> zones.id
- `name` — идентификатор ПК
- `status` — свободен/занят/забронирован/не работает

### tariffs
- `id` — PK
- `name`
- `price_per_hour`
- `description`

### promotions
- `id` — PK
- `name`
- `pattern` — описание акции (например "2+1")
- `schedule` — JSON с днями проведения

### bookings
- `id` — PK
- `client_id` — FK -> clients.id
- `zone_id` — FK -> zones.id
- `num_pcs` — количество ПК
- `start_time`
- `duration`
- `status` — активна/отменена/использована

### sessions
- `id` — PK
- `computer_id` — FK -> computers.id
- `client_id` — FK -> clients.id
- `tariff_id` — FK -> tariffs.id
- `start_time`
- `end_time`
- `cost`

### payments
- `id` — PK
- `client_id` — FK -> clients.id
- `amount`
- `method` — kaspi/nal/debt
- `created_at`
- `shift_id` — FK -> shifts.id

### shifts
- `id` — PK
- `operator_id` — FK -> users.id
- `start_time`
- `end_time`
- `kaspi_amount`
- `cash_amount`
- `coins_amount`
- `debt_amount`

### actions
- `id` — PK
- `user_id` — FK -> users.id
- `action_type`
- `details`
- `created_at`

## Основные маршруты API (Flask)

- `POST /api/auth/login` — логин и получение JWT
- `POST /api/auth/register` — создание пользователя
- `POST /api/auth/logout` — отзыв токена
- `GET /api/users` — список пользователей (admin)
- `POST /api/users` — создание пользователя
- `GET /api/clients` — список клиентов
- `POST /api/clients` — создание клиента
- `GET /api/zones` — список зон
- `POST /api/zones`
- `GET /api/computers` — список ПК
- `POST /api/computers`
- `GET /api/bookings` — бронирования
- `POST /api/bookings`
- `POST /api/bookings/<id>/cancel` — отменить бронь
- `GET /api/sessions` — активные/завершённые сессии
- `POST /api/sessions/start` — запуск сессии
- `POST /api/sessions/stop` — завершение
- `GET /api/tariffs`
- `POST /api/tariffs`
- `GET /api/promotions`
- `POST /api/promotions`
- `GET /api/shifts` — история смен
- `POST /api/shifts/close` — закрытие смены (kaspi, нал, мелочь, долги, комментарий)

Все запросы, кроме логина, требуют заголовок `Authorization: Bearer <jwt>`.

## Структура каталогов проекта

```
newcrm/
├── backend/
│   ├── app.py              # точка входа Flask
│   ├── requirements.txt    # зависимости бэкенда
│   ├── models/             # SQLAlchemy модели
│   ├── routes/             # Blueprints/маршруты API
│   └── ...
├── frontend/
│   ├── README.md           # Next.js фронтенд
│   └── ...                 # pages, components, etc.
├── docs/
│   └── design.md           # этот файл
└── README.md               # общая информация
```

## Зависимости

### Backend
- `Flask`
- `Flask-JWT-Extended` — JWT авторизация
- `Flask-SQLAlchemy` + `Flask-Migrate`
- `psycopg2` или `sqlite3`
- `requests` (для интеграции с внешними сервисами)
- `python-telegram-bot` (Telegram-уведомления)

### Frontend
- `React`, `Next.js`
- `Tailwind CSS`
- `axios` для запросов к API
- `jwt-decode` для работы с токенами

Эта структура задаёт основу для полноценной CRM-системы компьютерного клуба с ролями `admin`, `operator` и `read-only`, REST API, Telegram-уведомлениями и возможностью подключения внешних приложений.
