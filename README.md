# ThinkLink: Take home project task.

## Initialization

Update params in `.env` file.

### `.env` param details

`min` = Max value of BitCoin to watch

`max` = Min value of BitCoin to watch

`email` = Email id to receive email on `min` and `max` value cross.

`smtp_host` = SMTP Host

`smtp_port` = SMTP Port

`smtp_username` = SMTP Username

`smtp_password` = SMTP Password

## To Start/Run project.

You need to execute docker compose command to start the project.
First of all, you need to build docker container.

`docker-compose up --build`

Furthermore, you can only use `docker-compose up` after building container.

## API

You can get data on `http://127.0.0.1:5000/api/prices/btc` 
You can also add query params in API endpoint.
such as `http://127.0.0.1:5000/api/prices/btc?date=18-04-2022&limit=2&offset=2`

## To stop project.
Enter `Ctrl + C` in console to stop project.

After stopping, you need to remove cotainer usage from system.
to do this, `docker-compose down`.