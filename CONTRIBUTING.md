<details><summary><h1>Настройка локального окружения</h1></summary>

Для внесения изменений в репозиторий необходимо настроить работу внутри devcontainer-а.

- Устновить [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Установить [Visual Studio Code](https://code.visualstudio.com/download)
- [Настроить Visual Studio Code и Docker для использования Devcontainers](https://code.visualstudio.com/docs/devcontainers/containers#_getting-started)
- [Настроить Git и SSH для работы в Devcontainer](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials)
- [Установить шрифт Meslo Nerd Font для CLI в терминале](https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#fonts)
- По необходимости установить и настроить kubectl, внутри контейнера будут использованы настройки с хоста
- Склонировать этот репозиторий на рабочую станцию
- Открыть директорию с репозиторием через Visual Studio Code
- Установить [рекомендуемые плагины](.vscode/extensions.json) Visual Studio Code
- Ввести `Ctrl+Shift+P` или `Cmd+Shift+P` и выбрать `Dev Containers: Rebuild and Reopen in Container`

</details>

<details><summary><h1>Инструкция по установке</h1></summary>

- Клонируйте репозиторий и перейдите в него.
```bash
git clone git@hub.mos.ru:shift-python/y2024/homeworks/vstakrotskij/api_gateway.git
```
- Создайте файл .env, в корневой папке проекта, с переменными окружения.
```
SECRET = (секрет для создания токена)
```
- Для установки виртуального окружения с помощью Poetry нужно установить его через pip:
```bash
pip install poetry
```
- Для установки зависимостей выполните команду:

```bash
poetry install
```
- Для запуска API выполните команду:
```bash
python src/app/main.py
```

</details>

<details><summary><h1>Инструкция по запуску линтера</h1></summary>

- Для установки виртуального окружения с помощью Poetry нужно установить его через pip:
```bash
pip install poetry
```
- Для установки зависимостей выполните команду:

```bash
poetry install
```
- Для запуска линтера выполните команду:

```bash
flake8 src/
```

</details>

<details><summary><h1>Инструкция по запуску интеграционных тестов</h1></summary>

- Для установки виртуального окружения с помощью Poetry нужно установить его через pip:
```bash
pip install poetry
```
- Для установки зависимостей выполните команду:

```bash
poetry install
```

- Для запуска сервисов выполните команду:

```bash
docker compose -f docker-compose-test.yaml up
```

- В файле src/config/config.yaml замените значения base_url для каждого сервиса на 127.0.0.1:(порт из docker-compose-test.yaml).

- Для запуска интеграционных тестов выполните команду:

```bash
pytest src/tests/integration
```

</details>

<details><summary><h1>Инструкция по применению манифестов</h1></summary>

- Для загрузки манифестов кубернетис для каждого файла в папке /kuber/ необходимо выполнить следующую команду:

```bash
kubectl apply -f ./kuber/<filename>.yaml
```
</details>

<details><summary><h1>Инструкция по запуску приложения в кубернетис с использованием Helm</h1></summary>

- Выполните следующую команду:

```bash
helm install <prefix> ./api-gateway-chart
```
</details>
