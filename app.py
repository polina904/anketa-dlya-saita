from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import io
import os
import openpyxl
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['EXCEL_FILE'] = "survey_results.xlsx"

# Вопросы и варианты ответов для анкетирования
questions = [
    "1. Как часто вы обновляете антивирусное программное обеспечение на своих устройствах ?",
    "2. Как часто вы используете общедоступные Wi-Fi-сети для работы с конфиденциальной информацией в Академии управления МВД России ?",
    "3. Получали ли вы когда-либо подозрительные электронные письма ?",
    "4. Знаете ли вы, как распознать фишинг ?",
    "5. Как вы оцениваете уровень защиты от кибератак в Академии управления МВД России ?",
    "6. Как часто вы проводите сканирование на наличие вирусов на своих устройствах в Академии управления МВД России ?",
    "7. Используете ли вы VPN для защиты ваших данных в Академии управления МВД России ?",
    "8. Как часто вы получаете предупреждения о возможных кибератаках ?",
    "9. Знаете ли вы, как реагировать на кибератаку ?",
    "10. Как часто вы меняете пароли на своих учетных записях в Академии управления МВД России ?",
    "11. Используете ли вы одноразовые пароли для входа в системы Академии управления МВД России ?",
    "12. Как вы оцениваете уровень подготовки вашего персонала в Академии к противодействию кибератакам ?",
    "13. Получали ли вы когда-либо обучение в Академии по вопросам кибербезопасности ?",
    "14. Как часто вы слышите о кибератаках на образовательные учреждения ?",
    "15. Оцените уровень своей осведомленности о современных угрозах кибербезопасности.",
    "16. Как вы оцениваете уровень технической поддержки в Академии управления МВД России ?",
    "17. Как часто вы сообщаете о подозрительной активности в системах в Академии ?",
    "18. Знаете ли вы, какие данные необходимо защищать в первую очередь в Академии управления МВД России ?",
    "19. Как часто вы проверяете обновления системного программного обеспечения в Академии управления МВД России ?",
    "20. Как вы оцениваете уровень угрозы кибератак в Академии ?",
    "21. Как часто вы проверяете наличие обновлений для своего антивируса на рабочем месте ?",
    "22. Как часто вы используете общедоступные Wi-Fi-сети для работы с конфиденциальной информацией ?",
    "23. Получали ли вы когда-нибудь электронные письма, в которых от вас требовали личную информацию или просили перейти по незнакомой ссылке ?",
    "24. Знаете ли вы, какие характеристики указывают на фишинговые попытки ?",
    "25. Как вы оцениваете уровень защиты от кибератак в вашей организации ?",
    "26. Какова ваша периодичность проведения антивирусных сканирований на рабочем месте в Академии ?",
    "27. Активируете ли вы VPN для обеспечения конфиденциальности ваших данных ?",
    "28. Как часто ваша система безопасности выдает предупреждения о кибератаках ?",
    "29. Знаете ли вы, как реагировать на кибератаку ?",
    "30. Как часто вы меняете пароли на своих учетных записях ?",
    "31. Используете ли вы одноразовые пароли для входа в системы ?",
    "32. Как вы оцениваете уровень подготовки вашего персонала к противодействию кибератакам ?",
    "33. Получали ли вы когда-либо обучение по вопросам кибербезопасности ?",
    "34.  Как часто вы слышите о кибератаках на образовательные учреждения ?",
    "35. Оцените уровень своей осведомленности о современных угрозах кибербезопасности.",
    "36. Как оценивается уровень технической поддержки в вашей организации ?",
    "37. Как часто вы сообщаете о подозрительной активности в системах ?",
    "38. Знаете ли вы, какие данные необходимо защищать в первую очередь ?",
    "39. Как часто вы проверяете обновления системного программного обеспечения ?",
    "40. Как вы оцениваете уровень угрозы кибератак для вашей организации ?",
    "41. Как часто вы получаете обучение по работе с информационными системами в Академии ?",
    "42.  Как вы оцениваете уровень удобства используемых вами информационных систем в Академии ?",
    "43. Как часто вы сталкиваетесь с техническими проблемами в информационных системах в Академии ?",
    "44. Как вы оцениваете уровень поддержки пользователей в вашей организации ?",
    "45. Получали ли вы когда-либо обучение по использованию конкретной информационной системы в Академии ?",
    "46. Как часто вы используете документацию для работы с системами в Академии ?",
    "47. Как вы оцениваете уровень автоматизации процессов в ваших информационных системах в Академии ?",
    "48. Как часто вы сталкиваетесь с ошибками при работе с системами в Академии ?",
    "49. Знаете ли вы, как правильно сохранять и архивировать данные ?",
    "50. Как вы оцениваете уровень безопасности используемых вами систем в Академии управления МВД России ?",
    "51. Как часто вы получаете обновления о новых функциях в системах ?",
    "52. Как вы оцениваете свою способность решать проблемы, возникающие в системах в Академии ?",
    "53. Как часто вы используете резервное копирование данных в Академии управления МВД России ?",
    "54. Как вы оцениваете уровень интеграции различных систем в Академии управления МВД России ?",
    "55. Как часто вы обсуждаете проблемы использования информационных систем с коллегами в Академии ?",
    "56. Как вы оцениваете уровень доступа к необходимым системам для выполнения своей работы в Академии ?",
    "57. Знаете ли вы о существующих процедурах по обработке данных в Академии управления МВД России ?",
    "58. Как часто вы сталкиваетесь с конфликтами данных в системах в Академии ?",
    "59. Как вы оцениваете уровень взаимодействия между различными информационными системами в Академии?",
    "60. Как часто вы используете отчеты для анализа данных в системах в Академии управления МВД России ?",
    "61. Как часто вы сталкиваетесь с ошибками в работе сотрудников в Академии ?",
    "62. Получаете ли вы обучение по предотвращению ошибок в работе ?",
    "63. Как вы оцениваете уровень своей внимательности при выполнении задач ?",
    "64. Как часто вы проверяете свою работу перед отправкой ?",
    "65. Как часто ваши коллеги делают ошибки в работе ?",
    "66. Оцените уровень стресса на рабочем месте.",
    "67. Как часто вы получаете обратную связь о своей работе в Академии управления МВД России ?",
    "68. Как вы оцениваете уровень командной работы в вашем коллективе в Академии ?",
    "69. Как часто вы сталкиваетесь с недопониманием задач среди коллег в Академии ?",
    "70. Как вы оцениваете уровень коммуникации в вашей команде в Академии ?",
    "71. Как часто вы получаете обучение по работе в команде в Академии?",
    "72. Как вы оцениваете уровень удовлетворенности вашей работы в Академии управления МВД России ?",
    "73. Как часто вы обсуждаете ошибки на рабочем месте в Академии ?",
    "74. Как вы оцениваете влияние ошибок на работу вашей команды в Академии ?",
    "75. Как часто вы получаете поддержку от коллег в трудных ситуациях в Академии ?",
    "76. Как вы оцениваете уровень ответственности ваших коллег в Академии ?",
    "77. Как часто вы сталкиваетесь с конфликтами в своем коллективе в Академии ?",
    "78. Как часто вы получаете помощь при выполнении сложных задач ?"
    "79. Как вы оцениваете уровень доверия между сотрудниками ?",
    "80. Как часто вы обсуждаете способы улучшения работы в коллективе Академии ?",
    "81. Как часто вы обсуждаете личные данные студентов вне рабочего места в Академии ?",
    "82. Как вы оцениваете уровень конфиденциальности данных в Академии управления МВД России ?",
    "83. Получаете ли вы обучение по вопросам конфиденциальности данных в Академии управления МВД России ?",
    "84. Как часто вы проверяете, кто имеет доступ к вашим личным данным ?"
    "85. Как вы оцениваете уровень защиты персональных данных в Академии управления МВД России ?",
    "86. Как часто вы обсуждаете политику конфиденциальности с коллегами в Академии ?",
    "87. Как вы оцениваете уровень доступа к личным данным сотрудников в Академии ?",
    "88. Как часто вы получаете уведомления о нарушениях конфиденциальности ?",
    "89. Знаете ли вы о процедурах, связанных с нарушением конфиденциальности данных ?",
    "90. Как вы оцениваете уровень осведомленности сотрудников в Академии о конфиденциальности данных ?"
    "91. Как часто вы используете защищенные каналы для обмена конфиденциальной информацией ?",
    "92. Как вы оцениваете уровень защиты данных в электронных системах Академии управления МВД России ?",
    "93. Как часто вы проверяете настройки конфиденциальности в своих учетных записях ?",
    "94. Как вы оцениваете уровень доверия к системе защиты данных в Академии управления МВД России ?",
    "95. Как часто вы пересматриваете политику конфиденциальности в Академии управления МВД России ?"
    "96. Как вы оцениваете уровень защиты данных на мобильных устройствах ?",
    "97. Как часто вы сообщаете о случаях нарушения конфиденциальности в Академии ?",
    "98. Как вы оцениваете уровень защиты данных в облачных сервисах Академии управления МВД России ?",
    "99. Как часто вы получаете обучение по вопросам защиты конфиденциальной информации ?",
    "100. Как вы оцениваете уровень безопасности хранения личных данных в Академии управления МВД России ?"
]

options = [
["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Не знаю", "Плохо знаю", "Знаю, но неуверенно", "Знаю хорошо", "Знаю отлично"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Не знаю", "Плохо знаю", "Знаю, но неуверенно", "Знаю хорошо", "Знаю отлично"],
    ["Никогда", "Раз в год", "Раз в полгода", "Раз в квартал", "Каждый месяц"],
    ["Никогда", "Раз в год", "Раз в полгода", "Раз в квартал", "Каждый месяц"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Низкий", "Ниже среднего", "Средний", "Выше среднего", "Высокий"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Не знаю", "Плохо знаю", "Знаю, но неуверенно", "Знаю хорошо", "Знаю отлично"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Не знаю", "Плохо знаю", "Знаю, но неуверенно", "Знаю хорошо", "Знаю отлично"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Не знаю", "Плохо знаю", "Знаю, но неуверенно", "Знаю хорошо", "Знаю отлично"],
    ["Никогда", "Раз в год", "Раз в полгода", "Раз в квартал", "Каждый месяц"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Низкий", "Ниже среднего", "Средний", "Выше среднего", "Высокий"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Не знаю", "Плохо знаю", "Знаю, но неуверенно", "Знаю хорошо", "Знаю отлично"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень не удобные", "Неудобные", "Средние", "Удобные", "Очень удобные"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Не знаю", "Плохо знаю", "Знаю, но неуверенно", "Знаю хорошо", "Знаю отлично"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкая", "Низкая", "Средняя", "Высокая", "Очень высокая"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Не знаю", "Плохо знаю", "Знаю, но неуверенно", "Знаю хорошо", "Знаю отлично"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкое", "Низкое", "Среднее", "Высокое", "Очень высокое"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Не знаю", "Плохо знаю", "Знаю, но неуверенно", "Знаю хорошо", "Знаю отлично"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Совсем не доверяю", "Немного доверяю", "Средний уровень доверия", "Довольно доверяю", "Полностью доверяю"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"],
    ["Никогда", "Редко", "Иногда", "Часто", "Всегда"],
    ["Очень низкий", "Низкий", "Средний", "Высокий", "Очень высокий"]
]

def write_excel(data):
    filename = app.config["EXCEL_FILE"]
    
    if not os.path.exists(filename):
        # Create a new Excel file if it doesn't exist
        df = pd.DataFrame(columns=['Респондент'] + [f'Вопрос {i+1}' for i in range(len(questions))])
        df.to_excel(filename, index=False)

    try:
        # Load the existing Excel file
        book = openpyxl.load_workbook(filename)
        sheet = book.active
        
        # Get the last respondent number
        last_respondent = 0
        for cell in sheet['A']:
            if cell.value is not None and isinstance(cell.value, int):
                last_respondent = max(last_respondent, cell.value)
        
        # Prepare the new data to be appended
        respondent_num = last_respondent + 1
        row_data = [respondent_num]
        for i in range(len(questions)):
            question_key = f'question{i+1}'
            answer = data.get(question_key, '')
            row_data.append(answer)
        
        # Append the new data to the sheet
        sheet.append(row_data)
        
        # Save the changes
        book.save(filename)

    except Exception as e:
        print(f"Error writing to Excel file: {e}")

@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        form_answers = {}
        for i in range(1, len(questions) + 1):
            question_key = f'question{i}'
            form_answers[question_key] = request.form.get(question_key, '')

        write_excel(form_answers)
        return redirect(url_for('success'))

    return render_template('survey.html', questions=questions, options=options)

@app.route('/success')
def success():
    return "Спасибо за участие! Ваши ответы сохранены."

@app.route('/risks')
def risks():
    # Проверяем, существует ли файл с результатами
    if os.path.exists(app.config['EXCEL_FILE']):
        df = pd.read_excel(app.config['EXCEL_FILE'])
        
        # Подсчет ответов по каждому вопросу
        results = {}
        for i in range(1, len(questions) + 1):
            question_col = f'Вопрос {i}'
            results[question_col] = df[question_col].value_counts()


if __name__ == '__main__':
    app.run(debug=True)
