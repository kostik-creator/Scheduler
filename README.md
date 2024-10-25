# NudgeNinja

**NudgeNinja** — это ваш личный бот-напоминалка, созданный для того, чтобы помочь вам оставаться организованным и не пропустить ни одного важного события. 

Этот бот предоставляет удобный интерфейс для управления вашими напоминаниями.

С *NudgeNinja* вы всегда будете в курсе всех ваших дел и встреч, получая своевременные напоминания прямо в **Telegram**.

Приветственное сообщение и интуитивно понятное меню помогут вам быстро освоиться и начать использовать все возможности бота.

---

**NudgeNinja** — ваш надежный помощник в повседневной жизни!


## Функционал

- **Запуск бота**: Пользователи могут начать взаимодействие с ботом, отправив команду `/start`, после чего бот приветствует их и объясняет свои возможности.
  
- **Редактирование напоминаний**: Команда `/edit_reminder` позволяет пользователям изменять текст и дату существующих напоминаний. Пользователь должен указать номер напоминания, новый текст и дату в формате `YYYY-MM-DD HH:MM:SS`.

Пример редактирования напоминания:
- `/edit_reminder 1 Новый текст напоминания 2024-10-25 14:30:00` — изменяет текст и дату напоминания с номером 1.

- **Удаление напоминаний**: Команда `/delete_reminder` позволяет пользователям удалять напоминания по их ID. Пользователь должен указать номер напоминания, которое он хочет удалить.

Пример удаления напоминания:
- `/delete_reminder 2` — удаляет напоминание с номером 2.


- **Список напоминаний**: Пользователи могут запросить список всех своих напоминаний с помощью команды "Список моих напоминаний". Бот отправит список с описанием каждого напоминания.

- **Анализ и установка напоминаний**: Бот принимает текстовые команды для установки напоминаний. Пользователь может указать, что и когда ему нужно напомнить, и бот автоматически анализирует текст, определяя дату и время. Пользователь может использовать такие фразы, как "завтра", "через 10 минут", "послезавтра", "через час" и т.д.

Примеры установки напоминаний:
- "Напомни о встрече завтра в 15:00."
- "Напомни позвонить маме через 10 минут."
- "Напомни о дедлайне послезавтра в 18:00."
- "Отправить тестовое задание на почту через 15 мин"
  
Эти команды позволяют пользователю легко и быстро устанавливать напоминания, используя естественный язык.

- **Уведомления**: Бот отправляет уведомления пользователям, когда приходит время напоминания. Уведомления отправляются в Telegram, что позволяет пользователям получать уведомления в реальном времени.
## Запуск проекта

Для работы приложения выполните следующие шаги (также они есть в файлах main.py и env.example):

1. **Создайте виртуальное окружение**:
   
   Выполните команду в терминале:
   ```
   python -m venv venv
   ```
2. **Активируйте его**:

   Выполните команду в терминале (для **Windows**):
   ```
   venv\Scripts\activate
   ```
   Выполните команду в терминале (для **macOS и Linux**):
   ```
   source venv/bin/activate
   ```
3. **Установите все зависимости**:
   
   Выполните команду в терминале:
   ```
   pip install -r requirements.txt
   ```
4. **Создайте файл .env**:
   
   В корне вашего проекта создайте файл с именем .env и заполните его своими значениями(значения DATA_TTL и STATE_TTL оставьте без изменений):
   ```
    # Токен от Telegram Bot
    TOKEN_API=your_token_telegram_bot

    # Данные для подключения к Redis
    REDIS_HOST=your_redis_host 
    REDIS_PORT=your_redis_port
    REDIS_DB=your_redis_num_db
    REDIS_PASSWORD=your_redis_password 
    DATA_TTL=3600 
    STATE_TTL=600
    REDIS_USERNAME=your_redis_username

    # Данные для подключения к PostgreSQL
    host=your_postgres_host
    user=your_postgres_username
    password=your_postgres_password
    db_name=your_postgres_db_name
    port=your_postgres_port
5. **Запустите бота**

   Откройте терминал и перейдите в директорию с вашим проектом. Затем выполните:
   ```
   python main.py
   ```
   Откройте второй терминал и выполните:
   ```
   arq bot.other_func.arq_func.WorkerSettings
   ```
   ![image](https://github.com/user-attachments/assets/f9589df5-6efd-4864-857b-ddd7f16ceed0)
   
# Заключение

После выполнения этих шагов ваше приложение "NudgeNinja" должно быть успешно запущено и готово к использованию. Убедитесь, что все настройки в файле .env указаны корректно, а сервисы Redis и PostgreSQL доступны и работают должным образом.

Надеюсь, это руководство помогло вам успешно развернуть и запустить приложение "NudgeNinja".
