from email.mime import text
import smtplib
import sys
from pathlib import Path
from os.path import isfile, join, splitext
from os import listdir
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML

TXT_EXTENSION = '.txt'  # расширение искомых файлов

# ==== Доп. задание ====
# В качестве дополнительного параметра задается ключевое слово. 
# По данному ключевому слову выполняется поиск в текстовых файлах в папке клиента, 
# При обнаружении слова файл прикрепляется к письму.

# Поиск файла, в котором содержится подходящее ключевое слово
def find_files(msg, keyword):
    if keyword == '':
        return msg

    # Все файлы в директории
    all_files = []

    for f in listdir("."):
        if isfile(join(".", f)):
            all_files.append(f)

    # Список файлов искомого расширения
    res_files = []

    for file in all_files:
        # Функция splitext() модуля os.path делит путь path на двойной кортеж (root, ext), 
        # так что root + ext == path.
        filename = splitext(file)
        if filename[1] == TXT_EXTENSION:
            with open(file) as f:
                # Текст, считанный из файла
                text = f.read()
                # Если в тексте есть ключевое слово - сохраняем файл
                if keyword in text:
                    res_files.append(file)

    for f in res_files:
        part = MIMEApplication(open(f, 'rb').read())
        # attachments - вложения
        part.add_header(f'Content-Disposition', f'attachment; filename={(Path(f).name)}')
        msg.attach(part)

    return msg

# формирование и отправка сообщения
def send_mail(msg, msg_to_sent, smtphost, from_mail, password, to_mail, keyword):
    msg['From'] = from_mail # Адресат
    msg['To'] = to_mail # Получатель
    msg['Subject'] = "Test message" # Тема сообщения
    msg.attach(MIMEText(msg_to_sent, 'plain')) # Добавляем в сообщение текст

    msg = find_files(msg, keyword)

    server = smtplib.SMTP(smtphost[0], smtphost[1]) # Создаем объект SMTP
    server.starttls() # Начинаем шифрованный обмен по TLS
    server.login(from_mail, password) # Получаем доступ
    res = server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit() #закрываем подключение

def main():
    msg = MIMEMultipart() #создаем объект класса MIME
    msg_to_sent = "Hello! This is me)" # Текст сообщения
    smtphost = ["smtp.mail.ru", 587] #587 - незащищенный порт

    # получение аргументов из командной строки
    to_mail = sys.argv[1]
    from_mail = sys.argv[2]
    password = sys.argv[3]
    keyword = sys.argv[4]

    send_mail(msg, msg_to_sent, smtphost, from_mail, password, to_mail, keyword)

if __name__ == '__main__':
    main()