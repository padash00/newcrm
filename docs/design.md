# Дизайн CRM для компьютерного клуба

## Структура базы данных (PostgreSQL/SQLite)

### roles
- `id` — PK
codex/разработка-crm-системы-для-компьютерного-клуба
- `name` — название роли (`admin`, `operator`, `tech`, `read-only`)

- `name` — название роли (`admin`, `operator`, `read-only`)
main

### users
- `id` — PK
- `username` — логин
- `password_hash` — пароль
- `full_name` — имя оператора
- `phone`
- `role_id` — FK -> roles.id
codex/разработка-crm-системы-для-компьютерного-клуба
- `role` — строка роли (admin/operator/tech)
=======
main
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
codex/разработка-crm-системы-для-компьютерного-клуба
- `POST /api/auth/register` — создание пользователя

 codex-ui-clean
- `POST /api/auth/register` — создание пользователя

 main
main
- `POST /api/auth/logout` — отзыв токена
- `GET /api/users` — список пользователей (admin)
- `POST /api/users` — создание пользователя
- `GET /api/clients` — список клиентов
- `POST /api/clients` — создание клиента
codex/разработка-crm-системы-для-компьютерного-клуба
- `POST /api/clients/import_excel` — загрузка списка клиентов из Excel
main
- `GET /api/zones` — список зон
- `POST /api/zones`
- `GET /api/computers` — список ПК
- `POST /api/computers`
- `GET /api/bookings` — бронирования
- `POST /api/bookings`
codex/разработка-crm-системы-для-компьютерного-клуба
- `POST /api/bookings/<id>/cancel` — отменить бронь

 codex-ui-clean
- `POST /api/bookings/<id>/cancel` — отменить бронь
 main
main
- `GET /api/sessions` — активные/завершённые сессии
- `POST /api/sessions/start` — запуск сессии
- `POST /api/sessions/stop` — завершение
- `GET /api/tariffs`
- `POST /api/tariffs`
- `GET /api/promotions`
- `POST /api/promotions`
## Переменные окружения

- `JWT_SECRET_KEY` — секрет для подписи JWT
- `SQLALCHEMY_DATABASE_URI` — строка подключения к SQLite или PostgreSQL
- `CORS_ORIGINS` — список доменов фронтенда

- `GET /api/shifts` — история смен
codex/разработка-crm-системы-для-компьютерного-клуба
- `POST /api/shifts/close` — закрытие смены (kaspi, нал, мелочь, долги, комментарий)
- `GET /api/shifts/export_excel` — выгрузить отчёт по сменам в Excel
- `GET /api/reports/daily` — отчёт за день
- `GET /api/reports/weekly` — отчёт за неделю
- `GET /api/reports/custom` — отчёт за период
- `GET /api/reports/income-by-day` — доход по дням
- `GET /api/reports/clients-active` — активные клиенты по дням
- `GET /api/reports/shift-performance` — производительность смен

 codex-ui-clean
- `POST /api/shifts/close` — закрытие смены (kaspi, нал, мелочь, долги, комментарий)

- `POST /api/shifts/close` — закрытие смены
 main
main

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
codex/разработка-crm-системы-для-компьютерного-клуба
- `openpyxl` (импорт/экспорт Excel)
 main

### Frontend
- `React`, `Next.js`
- `Tailwind CSS`
- `axios` для запросов к API
- `jwt-decode` для работы с токенами

Эта структура задаёт основу для полноценной CRM-системы компьютерного клуба с ролями `admin`, `operator` и `read-only`, REST API, Telegram-уведомлениями и возможностью подключения внешних приложений.
