import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random
class StupidBirdGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Flying Bird")

        # Создаем холст для отображения игры
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        # Загружаем начальное и финальное изображения
        self.start_image = Image.open("start.png")
        self.start_image = self.start_image.resize((800, 400))
        self.start_photo = ImageTk.PhotoImage(self.start_image)

        self.end_image = Image.open("end.png")
        self.end_image = self.end_image.resize((800, 400))
        self.end_photo = ImageTk.PhotoImage(self.end_image)

        # Загружаем и обрабатываем GIF-анимацию птички
        self.bird_imgs = self.load_resized_gif("bird.gif", (95, 75))
        self.bird_index = 0
        self.bird_photo = self.bird_imgs[self.bird_index]

        # Загружаем и изменяем размер фона
        self.bg_image = Image.open("fon.jpg")
        self.bg_image = self.bg_image.resize((self.bg_image.width // 2, 600))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Загружаем изображение нижнего столба
        wall_image = Image.open("wall.png")
        wall_image = wall_image.resize((70, 300))
        self.wall_photo = ImageTk.PhotoImage(wall_image)

        # Загружаем изображение верхнего столба
        wall_top_image = Image.open("wall up.png")
        wall_top_image = wall_top_image.resize((70, 350))
        self.wall_top_photo = ImageTk.PhotoImage(wall_top_image)

        # Загружаем изображение земли
        ground_image = Image.open("ground.png")
        ground_image = ground_image.resize((900, 100))
        self.ground_photo = ImageTk.PhotoImage(ground_image)

        # Инициализируем игровые объекты как None
        self.bird = None
        self.wall = None
        self.wall_top = None
        self.ground = None
        self.bg1 = None  # Первый фон
        self.bg2 = None  # Второй фон

        # Устанавливаем начальные значения
        self.score = 0
        self.gravity = 10
        self.initial_speed = 20  # Начальная скорость
        self.speed = self.initial_speed
        self.score_threshold = 10
        self.pipe_gap = 275

        # Создаем метку для отображения счета
        self.score_label = tk.Label(root, text="Счет: 0", font=("Arial", 24))
        self.score_label.pack()

        # Привязываем обработчики событий для нажатия клавиш
        self.root.bind("<KeyPress>", self.on_key_down)
        self.root.bind("<KeyRelease>", self.on_key_up)

        # Устанавливаем флаг для проверки состояния игры
        self.game_running = False
        self.resetting = False  # Флаг для проверки перезапуска игры
        self.after_id = None  # ID вызова after

        # Показываем начальный экран
        self.show_start_screen()

    def load_resized_gif(self, filepath, size):
        """Загружает GIF и изменяет размер всех кадров"""
        img = Image.open(filepath)
        frames = []
        for frame in ImageSequence.Iterator(img):
            frame = frame.resize(size)
            frames.append(ImageTk.PhotoImage(frame))
        return frames

    def show_start_screen(self):
        """Отображаем начальный экран с инструкцией"""
        self.canvas.delete("all")
        self.start_label = tk.Label(self.root,
                                    text="Нажмите Enter для начала игры\nИспользуйте пробел для управления птичкой",
                                    font=("Arial", 24))
        self.start_label.pack()
        self.canvas.create_image(400, 300, anchor=tk.CENTER, image=self.start_photo)

    def show_end_screen(self):
        """Отображаем финальный экран с результатом"""
        self.canvas.delete("all")
        self.end_label = tk.Label(self.root, text=f"Счет: {self.score}\nНажмите Enter для новой игры",
                                  font=("Arial", 24))
        self.end_label.pack()
        self.canvas.create_image(400, 300, anchor=tk.CENTER, image=self.end_photo)

    def on_key_down(self, event):
        """Обработчик нажатия клавиш"""
        if event.keysym == "space":
            self.gravity = -13
        elif event.keysym == "Return":
            if not self.game_running and not self.resetting:
                self.start_game()

    def on_key_up(self, event):
        """Обработчик отпускания клавиш"""
        if event.keysym == "space":
            self.gravity = 13

    def start_game(self):
        """Запуск игры"""
        self.resetting = True  # Устанавливаем флаг перезапуска игры
        if hasattr(self, 'start_label') and self.start_label:
            self.start_label.destroy()
        if hasattr(self, 'end_label') and self.end_label:
            self.end_label.destroy()
        self.score = 0
        self.speed = self.initial_speed  # Сбрасываем скорость до начальной
        self.score_threshold = 10
        self.canvas.delete("all")

        # Создаем фон сначала
        self.bg1 = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)
        self.bg2 = self.canvas.create_image(self.bg_image.width, 0, anchor=tk.NW, image=self.bg_photo)

        # Затем создаем остальные игровые объекты
        wall_height = random.randint(200, 400)
        self.wall = self.canvas.create_image(600, wall_height + self.pipe_gap, anchor=tk.CENTER, image=self.wall_photo)
        self.wall_top = self.canvas.create_image(600, wall_height - self.pipe_gap, anchor=tk.CENTER,
                                                 image=self.wall_top_photo)
        self.ground = self.canvas.create_image(400, 620, anchor=tk.S, image=self.ground_photo)

        self.bird_index = 0
        self.bird_photo = self.bird_imgs[self.bird_index]
        self.bird = self.canvas.create_image(75, 275, anchor=tk.CENTER, image=self.bird_photo)

        self.score_label.config(text="Счет: 0")
        self.game_running = True
        self.resetting = False  # Сбрасываем флаг перезапуска игры
        self.stop_update_game()  # Останавливаем предыдущие вызовы
        self.update_game()
        self.update_bird_animation()

    def stop_update_game(self):
        """Останавливаем предыдущие вызовы метода update_game"""
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def update_game(self):
        """Обновление состояния игры"""
        if self.game_running and not self.resetting:
            self.canvas.move(self.bird, 0, self.gravity)
            self.canvas.move(self.wall, -self.speed, 0)
            self.canvas.move(self.wall_top, -self.speed, 0)

            self.canvas.move(self.bg1, -self.speed, 0)
            self.canvas.move(self.bg2, -self.speed, 0)

            # Перемещаем фон обратно, если он выходит за пределы окна
            if self.canvas.coords(self.bg1)[0] <= -self.bg_image.width:
                self.canvas.coords(self.bg1, self.bg_image.width, 0)
            if self.canvas.coords(self.bg2)[0] <= -self.bg_image.width:
                self.canvas.coords(self.bg2, self.bg_image.width, 0)

            bird_coords = self.canvas.bbox(self.bird)
            wall_coords = self.canvas.bbox(self.wall)
            wall_top_coords = self.canvas.bbox(self.wall_top)
            ground_coords = self.canvas.coords(self.ground)

            if wall_coords[2] < 0:
                x = 800
                wall_height = random.randint(200, 400)
                self.canvas.coords(self.wall, x, wall_height + self.pipe_gap)
                self.canvas.coords(self.wall_top, x, wall_height - self.pipe_gap)
                self.score += 1

            if (self.intersects(bird_coords, wall_coords) or
                    self.intersects(bird_coords, wall_top_coords) or
                    bird_coords[3] >= ground_coords[1] - 50):
                self.game_running = False
                self.score_label.config(text=f"Игра окончена!!!")
                self.show_end_screen()
            else:
                self.score_label.config(text=f"Счет: {self.score}")

            if self.score >= self.score_threshold:
                self.speed += 1
                self.score_threshold += 10

        if not self.resetting:  # Только если игра не перезапускается, вызываем обновление
            self.after_id = self.root.after(50, self.update_game)

    def update_bird_animation(self):
        """Обновление анимации птички"""
        if self.game_running:
            self.bird_index = (self.bird_index + 1) % len(self.bird_imgs)
            self.bird_photo = self.bird_imgs[self.bird_index]
            self.canvas.itemconfig(self.bird, image=self.bird_photo)
            self.root.after(100, self.update_bird_animation)  # Скорость анимации (кадры в секунду)

    def intersects(self, r1, r2):
        """Проверка пересечения двух прямоугольников"""
        return not (r1[2] < r2[0] or r1[0] > r2[2] or r1[3] < r2[1] or r1[1] > r2[3])


if __name__ == "__main__":
    root = tk.Tk()
    game = StupidBirdGame(root)
    root.mainloop()