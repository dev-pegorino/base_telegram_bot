commands = [
    ["start", "Restarting the bot",]
]

settings = {
    "about": "About",
    "description": "Description",
    "version": "1.0.0",
    "author": "Mingaleev Ilnaz",
}


def get_text(key: str, lang: str="en") -> str:
    translations = {
        "en": {
            "start": "Welcome!",
            "dont_understand": "Dont understand you",
            "captcha": "Please solve the example for confirmation:\n\n{problem} = ?",
            "captcha_correct": "✅ Correct! You passed the check.\n\nChoose the bot language:",
            "captcha_incorrect": "❌ Incorrect! Try again:\n\n{problem} = ?",
            "captcha_blocked": "You are blocked for {minutes} minutes due to wrong attempts",
            "captcha_wrong": "Wrong answer. Attempts left: {attempts_left}",
            "captcha_blocked_all": "You have exhausted all attempts. Blocked for 10 minutes",
            "language_selected": "Language selected: {lang}",
            "no_sub_channels": "Привет!\n\nПожалуйста, подпишитесь на каналы, чтобы использовать бота.",
            "no_sub_channels_dialog": "Пожалуйста, подпишитесь на каналы, чтобы использовать бота.",
        },
        "ru": {
            "start": "Добро пожаловать!",
            "dont_understand": "Не понимаю вас",
            "captcha": "Пожалуйста, решите пример для подтверждения:\n\n{problem} = ?",
            "captcha_correct": "✅ Правильно! Вы прошли проверку.\n\nВыберите язык бота:",
            "captcha_incorrect": "❌ Неправильно! Попробуйте еще раз:\n\n{problem} = ?",
            "captcha_blocked": "Вы заблокированы на {minutes} минут из-за неверных попыток",
            "captcha_wrong": "Неверный ответ. Осталось попыток: {attempts_left}",
            "captcha_blocked_all": "Вы исчерпали все попытки. Заблокировано на 10 минут",
            "language_selected": "Язык выбран: {lang}",
            "no_sub_channels": "Привет!\n\nПожалуйста, подпишитесь на каналы, чтобы использовать бота.",
            "no_sub_channels_dialog": "Пожалуйста, подпишитесь на каналы, чтобы использовать бота.",
        },
    }
    return translations[lang][key]


def get_text_button(key: str, lang: str="en") -> str:
    translations = {
        "en": {
            "language_en": "🇺🇸 English",
            "language_ru": "🇷🇺 Русский",
            "check_sub_channels": "I subscribed to the channels",
        },
        "ru": {
            "language_en": "🇺🇸 Английский",
            "language_ru": "🇷🇺 Русский",
            "check_sub_channels": "Я подписался на каналы",
        },
    }
    return translations[lang][key]