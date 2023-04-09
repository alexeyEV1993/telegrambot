from io import BytesIO

import telebot
from PIL import Image, ImageDraw
from imageai.Detection import ObjectDetection

# инициализация бота с помощью API-ключа
bot = telebot.TeleBot('api')

# загрузка предобученной модели для детекции объектов
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath('yolov3.pt')
detector.loadModel()
# приветствие
@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, f'Привет,{message.from_user.first_name}! Это бот для определения объектов на \
    картинке, загрузите в чат  фотографию на которой  вы хотите определить объект')


# обработка входящих изображений
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # загрузка изображения из сообщения
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Сохранение файл на диск
    file_name = 'image.jpg'
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    # детекция объектов на изображении
    detections = detector.detectObjectsFromImage(input_image='image.jpg')
    image = Image.open(BytesIO(downloaded_file))
    draw = ImageDraw.Draw(image)

    if detections:
        response_text = 'Найдено объектов: {}\n'.format(len(detections))
        for detection in detections:
            name = detection["name"]
            percentage_probability = detection["percentage_probability"]
            box_points = detection["box_points"]
            draw.rectangle(box_points, outline="red")
            draw.text((box_points[0], box_points[1] - 15), f"{name} ({percentage_probability:.2f}%)", fill="red")
            response_text += '{}: {}\n'.format(detection['name'], detection['percentage_probability'])
            bot.send_message(message.chat.id, response_text)
    # сохранение изображения в байтовом формате
    output = BytesIO()
    image.save(output, format='JPEG')
    output.seek(0)

    # отправляем изображение с обведенными объектами обратно в чат
    bot.send_photo(message.chat.id, photo=output)
    new_file.close()
# запуск бота
bot.polling(none_stop=True)