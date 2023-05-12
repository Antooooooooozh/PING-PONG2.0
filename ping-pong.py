from pygame import *

#фоновая музыка

# нам нужны такие картинки:

# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

# Создаем окошко
win_width = 600
win_height = 500
display.set_caption("Ping Pong")
window = display.set_mode((win_width, win_height))
# background = transform.scale(image.load(img_back), (win_width, win_height))

# создаем спрайты
racket1 = Player('raketka.png', 30, 200, 50, 150, 4) 
racket2 = Player('raketka.png', 520, 200, 50, 150, 4)
ball = GameSprite('ball.png', 200, 200, 50, 50, 4)

score = 0

font.init()
font = font.Font(None, 35)
lose1 = font.render('Игрок 1 проиграл!', True, (180, 0, 0))
lose2 = font.render('Игрок 2 проиграл!', True, (180, 0, 0))

speed_x = 3
speed_y = 3

#флаги, отвечающие за состояние игры
run = True
finish = False
clock = time.Clock()
FPS = 120

while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        # обновляем фон
        window.fill((32, 178, 170))
        # производим движения спрайтов
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

    if not finish:
        # обновляем фон
        window.blit(window,(0,0))
        # пишем текст на экране
        text = font.render("Счет  0 : " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        # обновляем их в новом местоположении при каждой итерации цикла
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            speed_y *= 1
        
        #если мяч достигает границ экрана, меняем направление его движения
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1

        #если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))
            finish = True

        #если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x > win_width:
            finish = True
            window.blit(lose2, (200, 200))
            finish = True

        racket1.reset()
        racket2.reset()
        ball.reset()

        display.update()
    # цикл срабатывает каждую 0.05 секунд
    time.delay(40)