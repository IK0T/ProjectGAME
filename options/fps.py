import pygame


# Показывает FPS клиента

class fps:  # noqa

    def __init__(self, game):
        self.game = game  # Логично

        # Три обьекта (Обновление, Отрисовка ну и Итог):
        self.update = self.game.font_handler.get_font("default_18").render(
            "Обновление:         Fps   (           ms)", True, self.game.color_handler.get_color_rgb("options.text"))
        self.render = self.game.font_handler.get_font("default_18").render(
            "Отрисовка:            Fps   (           ms)", True, self.game.color_handler.get_color_rgb("options.text"))
        self.total = self.game.font_handler.get_font("default_18").render(
            "Итого:                     Fps   (           ms)", True,
            self.game.color_handler.get_color_rgb("options.text"))

    def draw_stats(self, update_time, draw_time):  # Рисует на экране Статистику
        cub = pygame.Surface((410, 90), pygame.SRCALPHA)
        pygame.draw.rect(cub, self.game.color_handler.get_color_rgb("options.background"), ((0, 0), (410, 100)), False,
                         10)
        cub.set_alpha(128)
        self.game.main_surface.blit(cub, (self.game.display_width - 310, self.game.display_height - 90))

        # Здесь Показыается FPS:
        update_fps = self.game.font_handler.get_font("default_18").render(
            str(1 / max(update_time, 0.0001)).split(".")[0], True,
            self.game.color_handler.get_color_rgb("options.text"))

        render_fps = self.game.font_handler.get_font("default_18").render(
            str(1 / max(draw_time, 0.0001)).split(".")[0], True, self.game.color_handler.get_color_rgb("options.text"))

        total_fps = self.game.font_handler.get_font("default_18").render(
            str(1 / max(draw_time + update_time, 0.0001)).split(".")[0], True,
            self.game.color_handler.get_color_rgb("options.text"))

        # Здесь Показыается PING:
        update_ping = self.game.font_handler.get_font("default_18").render(str(update_time * 1000)[0: 5], True,
                                                                           self.game.color_handler.get_color_rgb(
                                                                               "options.text"))
        render_ping = self.game.font_handler.get_font("default_18").render(str(draw_time * 1000)[0: 5], True,
                                                                           self.game.color_handler.get_color_rgb(
                                                                               "options.text"))
        total_ping = self.game.font_handler.get_font("default_18").render(
            str((draw_time + update_time) * 1000)[0: 5], True, self.game.color_handler.get_color_rgb("options.text"))

        # Отрисовка:
        for i in range(1, 4):
            # Текст:
            self.game.main_surface.blit([self.update, self.render, self.total][i - 1], (
                self.game.display_width - 300, self.game.display_height - update_fps.get_height() * i - 10))

            # FPS:
            self.game.main_surface.blit([update_fps, render_fps, total_fps][i - 1], (
                self.game.display_width - 182, self.game.display_height - update_fps.get_height() * i - 10))
            # Ping:
            self.game.main_surface.blit([update_ping, render_ping, total_ping][i - 1], (
                self.game.display_width - 90, self.game.display_height - update_ping.get_height() * i - 10))
