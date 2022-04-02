# Урок 5
# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
# и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)

from mail_ru_parser import MailRuParser

if __name__ == '__main__':
    parser = MailRuParser()
    parser.parse()

    parser.write_result_to_db()
    parser.write_result_to_json('letters.json', ensure_ascii=False)
