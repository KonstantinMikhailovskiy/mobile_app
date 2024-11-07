import pandas as pd
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import webview

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        background = Image(source='123.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        # Инфа про версию
        icon = Image(source='34.png', size_hint=(None, None), size=(40, 40))
        icon_button = Button(background_normal='', size_hint=(None, None), size=(40, 40))
        icon_button.add_widget(icon)

        icon_button.bind(on_press=self.show_info)
        layout.add_widget(icon_button)

        self.id_input = TextInput(
            hint_text='Введите ваш 9-значный ID',
            multiline=False,
            size_hint=(0.8, None),
            height=40,
            pos_hint={'center_x': 0.5, 'top': 0.6}
        )
        layout.add_widget(self.id_input)

        self.submit_button = Button(
            text='Войти',
            size_hint=(0.5, None),
            height=50,
            pos_hint={'center_x': 0.5, 'top': 0.5},
            background_color=(0.678, 0.847, 0.902, 1)
        )
        self.submit_button.bind(on_press=self.check_id)
        layout.add_widget(self.submit_button)

        self.message_label = Label(text='', size_hint_y=None, height=30,
                                   pos_hint={'center_x': 0.5, 'top': 0.4})
        layout.add_widget(self.message_label)

        self.add_widget(layout)

    def check_id(self, instance):
        user_id = self.id_input.text.strip()

        # Проверяем длину ID
        if len(user_id) != 9 or not user_id.isdigit():
            self.show_length_error_popup()
            return

        # Правильность ID
        if self.is_valid_id(user_id):
            self.manager.current = 'lessons'  # Переход к урокам
        else:
            self.show_not_found_popup()

    def show_info(self, instance):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        version_label = Label(text='Версия: 1.0.0\nРазработчики: Люди какие-то!')
        popup_content.add_widget(version_label)

        close_button = Button(text='Закрыть', size_hint=(1, 0.2))
        close_button.bind(on_press=lambda x: popup.dismiss())
        popup_content.add_widget(close_button)

        popup = Popup(title='Информация', content=popup_content, size_hint=(0.6, 0.4))
        popup.open()

    def show_length_error_popup(self):
        popup = Popup(title='Ошибка', content=Label(text='ID должен содержать 9 цифр.'), size_hint=(None, None),
                      size=(400, 200))
        popup.open()

    def show_not_found_popup(self):
        popup = Popup(title='Ошибка', content=Label(text='Такого ID нет! Попробуйте снова.'), size_hint=(None, None),
                      size=(400, 200))
        popup.open()

    def is_valid_id(self, user_id):
        file_path = 'info.xlsx'
        df = pd.read_excel(file_path)
        ids = df['ID'].astype(str).tolist()
        return user_id in ids


class LessonsScreen(Screen):
    def __init__(self, **kwargs):
        super(LessonsScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        background = Image(source='4.jpg', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)

        label = Label(text='Уроки', font_size='24sp', size_hint=(0.5, None), height=50,
                      pos_hint={'center_x': 0.5, 'top': 0.97}, color=(0, 0, 0, 1))
        layout.add_widget(label)

        # Названия и URL видео для каждого урока
        lesson_titles = [
            'Урок 1 Гимнастика',  # Урок 1
            'Урок 2 Йога',  # Урок 2
            'Урок 3 Фитнес',  # Урок 3
            'Урок 4 Растяжка',  # Урок 4
            'Урок 5 Кардио тренировка',  # Урок 5
        ]

        lesson_videos = [
            'https://rutube.ru/video/f645156450f8d71984791034215c3554/',  # Урок 1
            'https://rutube.ru/video/f645156450f8d71984791034215c3554/',  # Урок 2
            'https://rutube.ru/video/video3/',  # Урок 3
            'https://rutube.ru/video/video4/',  # Урок 4
            'https://rutube.ru/video/fed18ac22350f28a37fb246151bcda1b/?playlist=304904',  # Урок 5
        ]

        for i in range(len(lesson_titles)):
            lesson_button = Button(text=lesson_titles[i], size_hint=(0.5, None), height=50,
                                   pos_hint={'center_x': 0.5, 'y': 0.8 - i * 0.1})
            lesson_button.bind(on_press=lambda x, lesson_index=i: self.play_video(lesson_videos[lesson_index]))
            layout.add_widget(lesson_button)

        back_button = Button(text='Назад', size_hint=(0.5, None), height=50,
                             pos_hint={'center_x': 0.5, 'y': 0.2})
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        layout.add_widget(back_button)

        self.add_widget(layout)

    def play_video(self, video_url):
        webview.create_window('Rutube Video', video_url, width=800, height=600)
        webview.start()


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))  # Предполагается, что экран 'login' также определен
        sm.add_widget(LessonsScreen(name='lessons'))
        return sm


if __name__ == '__main__':  # Исправлено на нужный синтаксис
    MyApp().run()

