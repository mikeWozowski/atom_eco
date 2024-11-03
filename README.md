# Atom Eco Waste Management API

Этот проект представляет собой API для системы учета отходов Atom Eco, с 
возможностями учета отходов, генерируемых организациями, и управления их 
хранением в специально оборудованных хранилищах.

Технологии:
```
- FastAPI — для разработки API.
- PostgreSQL — в качестве базы данных для хранения данных организаций, хранилищ и отходов.
- Alembic — для управления миграциями базы данных.
- Docker и docker-compose — для контейнеризации и облегчения развертывания приложения.
- Pydantic — для управления данными и валидации.
- SQLAlchemy — для работы с базой данных.
- PyTest — для написания unit-тестов основных методов API.
```

## Установка и запуск

Сколинруйте репозиторий

```bash
git clone https://github.com/mikeWozowski/atom_eco.git
cd atom_eco
```

Переименуйте файл .env.example в .env и настройте переменные окружения.

Обновите sqlalchemy.url в alembic.ini

Примените миграции базы данных с помощью Alembic:

```bash
alembic upgrade head
```

### Вариант 1: Локальная установка с использованием виртуального окружения

Убедитесь, что у вас установлен Pipenv.

Создайте виртуальное окружение и установите зависимости:

```bash
pipenv install
```

Активируйте виртуальное окружение:

```bash
pipenv shell
```

Перейдите в директорию src и запустите приложение:
```bash
cd src
fastapi dev main.py
```

### Вариант 2: Запуск с использованием Docker и Docker Compose

Убедитесь, что у вас установлены Docker и Docker Compose.

Постройте и запустите контейнеры с помощью Docker Compose:

```bash
docker-compose up --build
```

Приложение и документация будут доступны по адресу http://127.0.0.1:8000.

### API

В базе данных автоматически созданы типы отходов:

	•	Стекло (id: 1)
	•	Пластик (id: 2)
	•	Биоотходы (id: 3)

При использовании методов API обязательно указывайте соответствующие ID типов мусора.

Для расчета расстояния между объектами (между организациями и хранилищами) выбран подход, при котором каждой сущности задаются координаты её местоположения. Расстояние в метрах затем вычисляется с использованием этих координат по соответствующей формуле.


