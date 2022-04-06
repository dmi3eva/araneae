INSTRUCTIONS = """
\U0001F600 Здравствуйте! 

Мы занимаемся расширением существующего датасета SQL-запросов искусственными методами. Будем очень благодарны, если вы поможете оценить корректность новых примеров.
<i>Сейчас вы можете пропустить инструкцию и вернуться к ней, когда у вас возникнут вопросы.</i>
Главное, помните, что, если вы сомневаетесь, то лучше линий раз сообщить об ошибке.

Оценка корректности каждого примера разбита на 4 последовательных шага. 

1️⃣ <b>ШАГ</b>: 
Звучит ли запрос к базе данных естественно и адекватно?

Примеры:
\U00002796 What ID has the most surnames? \U00002192 <i>Звучит неестественно. Да и каждому ID, скорее всего, соответствует одно имя. </i>
\U00002795 Which command has the most wins?

2️⃣ <b>ШАГ</b>: 
Похож ли вообще данный текст на запрос к БД?

Примеры:
\U00002796 Any country in the world have five singers. \U00002192 <i>Это просто повествовательное предложение, не запрос.</i>
\U00002795 List all countries in the world that have five singers.

\U00002796 Why can't you count the number of conductors? \U00002192 <i>Нет запроса на получение информации из БД.</i>
\U00002795 What the number of conductors?

\U00002796 Compare all companies. \U00002192 <i>Запрос не четкий. Нельзя однозначно перевести его на SQL.</i> 
\U00002795 Order companies names by their profit margins, please.

\U00002796 All the broadcasting TV Channels don't working today. List the number of different channels by their owners. \U00002192 <i>Многовато лишней информации :)</i>
\U00002795 List the number of different channels by their owners.

3️⃣ <b>ШАГ</b>: 
Значат ли одно и то же два данных вопроса?

Примеры:
\U00002796 
Give the language that is spoken in the most countries.
What is the most spoken language in the world?
\U00002795
What are the type codes and descriptions for all template types?	
What are types of templates? What are their descriptions?

4️⃣ <b>ШАГ</b>: 
Самое сложное: соответствует ли запрос данному SQL?

Примеры:
\U00002796 
Show descriptions of simple properties.
<code>SELECT description FROM Properties WHERE type='Simple'</code>
\U00002795 
Show descriptions of simple properties.
<code>SELECT T2.description FROM Properties AS T1 JOIN Attributes AS T2 ON T1.code  =  T2.code WHERE T1.type='Simple'</code>

Для проверки вы можете заглядывать в таблицы БД.
Справочник по SQL: https://schoolsw3.com/sql/index.php.
Если совсем сложно, просто пропускайте. 
При возникновении вопросов пишите @dmi3eva.

Спасибо за помощь!
"""

OK_TO_CORRECT = "Записали, что с этим запросом все хорошо! Спасибо!"
WHATS_WRONG = "Опишите, в чем проблема? Если есть возможность, укажите верный вариант."
OK_TO_INCORRECT = "Спасибо, учтем!"


ERROR = "Этот функционал пока не работает"

TABLE_TITLE = '''
Это список таблиц в базе данных <b>{db}</b>. Выберите одну из них, чтобы посмотреть содержимое.
'''

TOO_LONG = "<i>В таблице слишком много данных. Вот лишь <b>часть из них</b></i>: \n"


FLUENCY_SOURCE_DESCRIPTION = '''
1️⃣ Может ли этот текст быть запросом к базе данных?

<i> {nl} </i>

<b>Пояснение:</b>
\U000025CF Естественно ли это звучит?
\U000025CF Содержится ли в тексте заявка на получение информации?
'''


FLUENCY_SUBSTITUTION_DESCRIPTION = '''

2️⃣ А этот текст может быть запросом к базе данных?

<i> {nl} </i>
'''

EQV_DESCRIPTION = '''
3️⃣ Дан <b>исходный</b> вопрос к базе данных:

<i>{source}</i>

Значит ли наш запрос то же самое?

<i>{paraphrase}</i>
'''

SQL_DESCRIPTION = '''
4️⃣ Дан SQL:

<code>{sql}</code>

Соответствует ли ему этот запрос:

<i>{nl}</i>
'''

FLUENCY_SOURCE_CORRECTION = """
\U0001F527 Если возможно, переформулируйте запрос:

<i>{nl}</i>

Важно, чтобы он соответствовал SQL:

<code>{sql}</code>
"""

FLUENCY_SUBSTITUTION_CORRECTION = """
\U0001F529 Если возможно, переформулируйте запрос:

<i>{nl}</i>

Важно, чтобы он соответствовал SQL:

<code>{sql}</code>
"""

EQUIVALENT_CORRECTION = """
\U0001F529 Если возможно, переформулируйте запрос:

<i>{nl}</i>

Важно, чтобы он соответствовал SQL:

<code>{sql}</code>
"""


SQL_CORRECTION = """
\U0001F529 Если возможно, переформулируйте запрос:

<i>{nl}</i>

Важно, чтобы он соответствовал SQL:

<code>{sql}</code>
"""

OK_TO_FLUENCY_SOURCE = "Да, может"
OK_TO_FLUENCY_SUBSTITUTION = "Да, может"
OK_TO_EQV = "Да, это одно и то же"
OK_TO_SQL = "Да, соответствует"

WRONG_TO_FLUENCY_SOURCE = "Нет!"
WRONG_TO_FLUENCY_SUBSTITUTION = "Нет!"
WRONG_TO_EQV = "Нет, не значит"
WRONG_TO_SQL = "Нет, не соответствует"

DB = "Посмотреть БД"
SKIP = "Пропустить"
HELP = "Инструкции"

FLUENCY_CORRECTION = '''
Если возможно, поправьте вопрос. Важно, чтобы он звучал естественно и соответствовал данному SQL-запросу:

<code>{sql}</code>

Запишите свой вариант в сообщении.
'''

CORRECTION_DONE = "Сохранить"
CORRECTION_IMPOSSIBLE = "Не знаю, как поправить запрос"
ANSWER_TO_IMPOSSIBLE = "Спасибо, что нашли ошибку! Мы рассмотрим этот запрос внимательнее."

TABLE_VIEW = '''
Это содержимое таблицы <b>\"{table}\"</b>.

<code>{view}</code>
'''

CALL_OK = 'correct'
CALL_WRONG = 'incorrect'
CALL_SKIP = "skip"
CALL_DB = "db"
CALL_INFO = "info"

ESTIMATE = "estimate"
RETURN = "return"
RETURN_TO_TABLES = "return_to_tables"
TEXT_TYPED = "text_typed"
TABLE = "table"
COLUMN = "column"

# RAN_OUT = "Sorry, but we don't have any new samples for you! Thank you very much!"
RAN_OUT = "Вы отсмотрели все доступные запросы. Разметка на данный момент закончена. Большое спасибо вам за помощь!"
KEY_DOESNT_EXIST = "Пожалуйста, выберите один из предложенных вариантов и нажмите соответствующую кнопку. Если вам не было ничего предложено, то введите /start."