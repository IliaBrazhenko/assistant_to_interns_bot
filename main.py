from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# Константы состояний для ConversationHandler
MAIN_MENU, SUBMENU, TASK_SELECTION, FEEDBACK_INPUT = range(4)

# Токен от BotFather
TOKEN = "7530843123:AAEkVvS2N51zVl_6EJa5ypQNxfA-kR-bidI"

# Список часто задаваемых вопросов и ответов
FAQS = {
    "Что такое стажировка?": "Стажировка — это практическое обучение, которое даёт студентам и молодым специалистам опыт работы.",
    "Какие требования к стажёрам?": "Обычно стажёры должны иметь базовые знания в своей специальности и готовность учиться.",
    "Где проходят стажировки?": "Стажировки проходят в наших дарсторах (складах), частично дистанционно, в зависимости от вакансии.",
    "Какой график работы у стажёров?": "График стажера оыбчно соответсвует графику наставника, согласовывается индивидуально с куратором.",
}

# Материалы для изучения
STUDY_MATERIALS = [
    "Тренировки в приложении УзнайПро: https://samokat.uznaipro.ru/4/dashboard",
    "Видеоуроки: https://samokat.uznaipro.ru/4/video",
]

# Контактные данные кураторов
CURATORS_INFO = """
Илья Браженко (t.me/@iledbrz): отвечает за стажировку товароведов/директоров.
Илья Браженко (t.me/@iledbrz): занимается обучением товароведов/директоров.
"""

# Функция-обработчик для команды "/start"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Часто задаваемые вопросы", callback_data='faq')],
        [InlineKeyboardButton("Получить задание", callback_data='task')],
        [InlineKeyboardButton("Обратная связь", callback_data='feedback')],
        [InlineKeyboardButton("Информация о компании", callback_data='company_info')],
        [InlineKeyboardButton("Материалы для изучения", callback_data='study_materials')],
        [InlineKeyboardButton("Контакты кураторов", callback_data='curators_info')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать! Выберите нужное действие:", reply_markup=reply_markup)
    return MAIN_MENU

# Обработчик нажатий на кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'faq':
        await show_faqs(query)
    elif query.data == 'task':
        await assign_task(query)
    elif query.data == 'feedback':
        await ask_for_feedback(query)
    elif query.data == 'company_info':
        await company_info(query)
    elif query.data == 'study_materials':
        await study_materials(query)
    elif query.data == 'curators_info':
        await curators_info(query)
    elif query.data == 'back_to_main_menu':
        await start(query, context)

# Показываем список часто задаваемых вопросов
async def show_faqs(query):
    text = "\n\n".join([f"{q}:\n{a}" for q, a in FAQS.items()])  # Добавляем дополнительное пространство между парами
    keyboard = [[InlineKeyboardButton("Вернуться в главное меню", callback_data='back_to_main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"Часто задаваемые вопросы:\n\n{text}", reply_markup=reply_markup)

# Присваиваем задание
async def assign_task(query):
    current_tasks = ['Закончить отчет по проекту.', 'Изучить документацию по Sharepoint.', 'Создать отчёт о проделанной работе.']
    task = current_tasks.pop()  # Берём первое задание из списка
    message = f"Твое текущее задание по ссылке: https://mubint.sharepoint.com/sites/stazhirovka2025/Lists/List/AllItems.aspx"  # добавляем ссылку на задание
    keyboard = [[InlineKeyboardButton("Вернуться в главное меню", callback_data='back_to_main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=message, reply_markup=reply_markup)

# Спрашиваем обратную связь
async def ask_for_feedback(query):
    message = "Пожалуйста, оставьте обратную связь, заполнив анкету по ссылке: https://forms.office.com/Pages/ResponsePage.aspx?id=MHQdU9OAJ0WNwAEUONkf4EpPSz3j3vZAnrkPyGmRql5UNTBQUkFMTTlYNVczSkQ0MjJXMVZSWVc5Ry4u"  # добавляем ссылку на форму обратной связи
    keyboard = [[InlineKeyboardButton("Вернуться в главное меню", callback_data='back_to_main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=message, reply_markup=reply_markup)
    return FEEDBACK_INPUT

# Обрабатываем оставленную обратную связь
async def process_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    feedback = update.message.text
    await update.message.reply_text(f"Спасибо за вашу обратную связь: '{feedback}'")
    return ConversationHandler.END

# Информация о компании
async def company_info(query):
    info = "Наша компания занимается экономией времени наших пользователей. Мы ценим креативность и стремление к развитию!"
    keyboard = [[InlineKeyboardButton("Вернуться в главное меню", callback_data='back_to_main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=info, reply_markup=reply_markup)

# Материалы для изучения
async def study_materials(query):
    materials = "\n".join(STUDY_MATERIALS)
    keyboard = [[InlineKeyboardButton("Вернуться в главное меню", callback_data='back_to_main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=materials, reply_markup=reply_markup)

# Контакты кураторов
async def curators_info(query):
    keyboard = [[InlineKeyboardButton("Вернуться в главное меню", callback_data='back_to_main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=CURATORS_INFO, reply_markup=reply_markup)

# Завершаем беседу
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Действие отменено.")
    return ConversationHandler.END

# Основной запуск бота
if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            MAIN_MENU: [CallbackQueryHandler(button)],
            TASK_SELECTION: [],
            FEEDBACK_INPUT: [MessageHandler(filters.TEXT & (~filters.COMMAND), process_feedback)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    print("Запускаю бота...")
    application.run_polling()