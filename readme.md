# Pylint os.environ Checker

Плагин для Pylint, который запрещает использование os.environ в проекте.

## Зачем?

Когда ссылки на переменные окружения разбросаны по большой кодовой базе 
в разных местах, становится сложно предсказывать поведение приложения. 

Особенно это мешает, если в проекте реализован паттерн настроек a la Django 
с несколькими файлами `base.py`, `prod.py`, `dev.py` и т.д.,
каждый из которых тоже опирается на переменные окружения.

Плагин os_environ_checker позволяет запретить использование os.environ во всех файлах, кроме избранных.

## Установка и настройка

```
pip install pylint_os_environ_checker
```

Добавить плагин в `.pylintrc`, в секцию `MASTER`:

```
[MASTER]
load-plugins = os_environ_checker
```

Добавить секцию OS_ENVIRON_CHECKER, в которой указать путь, в котором таки можно обращаться к `os.environ`. 
Это может быть регулярное выражение:

```
[OS_ENVIRON_CHECKER]
allow_in_modules = _devtools.*restore

```


Ошибка, которую выдает чеке, - `R9000`:

```
...
getmybot/settings/my.py:97: [R9000(os-environ-prohibited), ] Usage of os.environ is prohibited. Import from django settings instead.
...
```


Как запустить pylint на все файлы и папки текущей директории:

```
find . -name "*.py" | xargs pylint
```

Как сделать игнор папки для всего pylint (не только для этого чекера):

```
find . -name "*.py" | grep -v "node_modules" | xargs pylint
```



