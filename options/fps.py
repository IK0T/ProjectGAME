import pygame
from .modules.options.fps import fps


class options:  # noqa

    def __init__(self, game):
        self.game = game

        # Открыто ли меню
        self.open = False
        # Включен ли показ FPS
        self.show_fps = False

        self.fps_module = fps(game)

        # Какой выбран модуль в меню
        self.menu_id = 0

        # Координаты подсказывающей метки
        self.marker_y = 200 + (self.menu_id * 70)
        self.marker_x = 40

        self.show_fps_text_surface = self.game.font_handler.get_font("default").render(f"Показать FPS:{self.show_fps}",
            True, (self.game.color_handler.get_color_rgb("taptap.text")))
        self.reset_save_text_surface = self.game.font_handler.get_font("default").render("Удалить Сохранение", True,
            (self.game.color_handler.get_color_rgb("taptap.text")))

        self.marker_target_width = self.show_fps_text_surface.get_width() + 20
        self.marker_width = self.marker_target_width

        self.bg_target_x = -1000
        self.bg_x = self.bg_target_x

    def update(self):
        self.bg_x += (self.bg_target_x - self.bg_x) / 10
        if self.open:
            self.bg_target_x = 5
            self.game.input.input_state = "options"
            if self.game.input.is_pressed("esc"):
                self.open = False

            self.menu_id = self.menu_id % 2

            if self.game.input.is_just_pressed("DOWN"):
                self.menu_id += 1
            if self.game.input.is_just_pressed("UP"):
                self.menu_id -= 1

            self.show_fps_text_surface = self.game.font_handler.get_font("default").render(f"Показать FPS: {str(self.show_fps)}", # noqa
                True, (self.game.color_handler.get_color_rgb("taptap.text")))

            self.marker_y += (270 + (self.menu_id * 140) - 25 - self.marker_y) / 8
            self.marker_width += (self.marker_target_width - self.marker_width) / 20

            if self.menu_id == 0:
                self.marker_target_width = self.show_fps_text_surface.get_width() + 20
            if self.menu_id == 1:
                self.marker_target_width = self.reset_save_text_surface.get_width() + 20

            if self.game.input.is_just_pressed("1") and self.game.input.is_just_pressed("ALT"):
                quit()

            if self.game.input.is_just_pressed("SPACE") or self.game.input.is_just_pressed("RETURN"):
                if self.menu_id == 0:
                    self.show_fps = not self.show_fps
                if self.menu_id == 1:
                    self.game.taptap.save_file = {"all_plays": []}
                    self.game.notification_handler.send('Сохранение удалено',
                                                        'Файл сохранения "TapTap"  удалён из главного меню')
        else:
            self.game.input.input_state = "game"
            self.bg_target_x = -1000

    def render(self):  # Отрисовка
        pygame.draw.rect(self.game.main_surface, self.game.color_handler.get_color_rgb("options.background"),
                         ((self.bg_x, 5), (500, self.game.display_height - 10)), False, 5)

        if self.open:
            pygame.draw.rect(self.game.main_surface, self.game.color_handler.get_color_rgb("taptap.marker"),
                             ((self.marker_x, self.marker_y), (self.marker_width, 5)), False, 5)

            self.game.main_surface.blit(self.show_fps_text_surface, (50, 200))
            self.game.main_surface.blit(self.reset_save_text_surface, (50, 340))
