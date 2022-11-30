# Примеры использования TrueConf Server API

Данный пример кода демонстрирует решение с помощью TrueConf Server API задач, которые были детально рассмотрены в статьях нашей базы знаний:

1. [Как добавить учётные записи пользователей из файла](https://trueconf.ru/blog/baza-znaniy/kak-dobavit-uchyotnye-zapisi-polzovatelej-iz-fajla.html)

1. [Как автоматически очищать завершившиеся конференции](https://trueconf.ru/blog/baza-znaniy/kak-avtomaticheski-ochishhat-zavershivshiesya-konferenczii.html)

*Читать описание на других языках: [English](README.md)*

:warning: ***Внимание!***
> **Не рекомендуется запускать файл скрипта на ОС с установленным TrueConf Server, лучше всего используйте для этого другой компьютер в локальной сети, которому виден ВКС-сервер по IP или доменному именю (FQDN).**

Код написан на Python, поэтому для его работы необходимо:

1. Установить **Python 3.7+**, скачав его с официального сайта: https://www.python.org/downloads 

1. Обновить установщик пакетов **pip**: https://pip.pypa.io/en/stable/installing/#upgrading-pip 

1. Установить дополнительные пакеты для работы с Excel-файлами:

```bash
pip install requests pyexcel pyexcel-odf pyexcel-xls pyexcel-xlsx
```

## Подготовка сервера

[Настройте HTTPS](https://trueconf.ru/blog/baza-znaniy/kak-nastroit-webrtc-konferentsii-v-chrome.html#_HTTPS) в панели управления TrueConf Server.

Далее перейдите в [раздел API → OAuth2](https://docs.trueconf.com/server/admin/web-config#oauth2). Создайте новое OAuth 2.0 приложение, отметив флажками необходимые для решения рассмотренных выше задач права:

- conferences
- groups
- groups.users
- users
- users.avatar:read
- users.avatar:write

:point_right: ***Подсказка***
> **Детально о том, что такое протокол OAuth и как с ним работать, рассказано [в документации к серверу](https://docs.trueconf.com/server/admin/web-config#oauth2).**

## Использование параметров

Вы можете указать параметры, необходимые для работы скрипта, в файле настроек **data.json** (рекомендуемый метод) или же ввести вручную после его запуска. Список необходимых параметров:

- **`"server"`** – IP-адрес или URL TrueConf Server, например, **video.company.name** или **10.120.1.10**;
- **`"new_users_file"`** – к файлу, где хранятся данные для импорта учётных записей на сервер или их удаления (поддерживаются форматы **.csv**, **.ods**, **.xls** и **.xslx**, детальное описание его формата смотрите в статье о добавлении пользователей из файла);
- **`"client_id"`** – идентификатор OAuth-приложения;
- **`"client_secret"`** – секретный ключ OAuth-приложения;
- **`"delimiter"`** – разделитель значений в строках при использовании **.csv**, требуется указать тот что используется в вашем файле;
- **`"verify"`** – настройка проверки SSL-сертификата, подробнее: https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification. В случае использования на сервере самоподписанного SSL-сертификата требуется скачать .crt-файл сертификата на ПК с данным скриптом, и в параметре `"verify"` указать полный путь к этому файлу. Если же используется коммерческий сертификат, то указать значение **true** без кавычек: **`"verify":true`**.

Путь к файлу сертификата:
- TrueConf Server для Linux: `/opt/trueconf/server/etc/webmanager/ssl/ca.crt`
- TrueConf Server для Windows: `C:\Program Files\TrueConf Server\httpconf\ssl\ca.crt`

## Работа со скриптом

**Запуск скрипта на Windows**

Перейдите в каталог со скриптом и запустите его двойным кликом мыши. Альтернативный способ: открыть терминал и выполнить в нём команду `/path/api-examples.py` где `path` – полный путь к скрипту.

**Запуск скрипта на Linux**

Выполните в терминале команду:

```bash
sudo python3 /path/api-examples.py
```

где `path` – полный путь к скрипту.

После запуска файла скрипта **api-examples.py** вы увидите меню в окне терминала, где вам будет предложено выбрать требуемую задачу. Для этого введите одну из таких команд:

- **S** – чтение параметров для подключения к серверу (из файла **json.data** или их ввод вручную);

- **E** – [удаление завершившихся конференций](https://trueconf.ru/blog/baza-znaniy/kak-avtomaticheski-ochishhat-zavershivshiesya-konferenczii.html):
  - введение количества суток, старше которых надо удалить мероприятия (можно дробное, например 1.5 для удаления конференций, завершившихся за 36 часов до текущего момента времени);
  - получение списка всех остановленных конференций;
  - поиск среди них запланированных мероприятий со сроком окончания старше указанного;
  - удаление конференций.

- **N** – [импорт пользователей и групп из файла](https://trueconf.ru/blog/baza-znaniy/kak-dobavit-uchyotnye-zapisi-polzovatelej-iz-fajla.html):
  - чтение данных из файла;
  - добавление групп пользователей на сервер;
  - добавление учётных записей;
  - загрузка аватарок для пользователей (если указаны);
  - добавление пользователей в группы.

- **D** – [удаление пользователей и групп, перечисленных в файле](https://trueconf.ru/blog/baza-znaniy/kak-dobavit-uchyotnye-zapisi-polzovatelej-iz-fajla.html#i-2);

- **Q** – завершение работы скрипта.
