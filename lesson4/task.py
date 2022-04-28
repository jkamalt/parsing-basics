# Урок 4
# 1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
#   - название источника;
#   - наименование новости;
#   - ссылку на новость;
#   - дата публикации.
# 2. Сложить собранные новости в БД

from news_mail_parser import NewsMailParser

if __name__ == '__main__':
    parser = NewsMailParser()
    parser.parse()

    parser.write_result_to_db()
    parser.write_result_to_json('result.json', ensure_ascii=False)
