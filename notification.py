import notify2

#def notify():

#ICON_PATH= "полный путь до иконки"

# Получаем текущий курс
#bitcoin = rates.fetch_bitcoin()

# Инициализируем d-bus соединение
notify2.init("Cryptocurrency rates notifier")

# Создаем Notification-объект
n = notify2.Notification("Crypto Notifier")

# Устанавливаем уровень срочности
n.set_urgency(notify2.URGENCY_NORMAL)

# Устанавливаем задержку
n.set_timeout(10000)

#result = '{0} — {1}'.format(*bitcoin) 

# Обновляем содержимое 
n.update("Текущий курс") 

# Показываем уведомление
n.show()
