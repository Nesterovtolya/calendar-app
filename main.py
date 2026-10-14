# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image as KivyImage
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window

import calendar
import datetime
from PIL import Image, ImageDraw, ImageFont
import os

Window.clearcolor = (1, 1, 1, 1)
try:
    Window.softinput_mode = 'resize'
except Exception:
    pass


class DateRow(BoxLayout):
    def __init__(self, index, day, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(35)
        self.padding = [dp(15), 0]

        left = Label(text=f"день {index}", halign='left', valign='middle',
                     color=(0, 0, 0, 1), size_hint_x=0.5)
        left.bind(size=lambda s, v: setattr(s, 'text_size', (v[0], None)))

        right = Label(text=str(day), halign='right', valign='middle',
                      color=(0, 0, 0, 1), size_hint_x=0.5)
        right.bind(size=lambda s, v: setattr(s, 'text_size', (v[0], None)))

        self.add_widget(left)
        self.add_widget(right)


class CalendarApp(App):
    month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                   "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

    def build(self):
        self.work_days = []
        root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))

        title = Label(text="Календарь смен", size_hint_y=None, height=dp(45),
                      font_size=dp(24), bold=True, color=(0.9, 0.2, 0.2, 1))
        root.add_widget(title)

        month_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        month_box.add_widget(Label(text="Месяц:", size_hint_x=0.3,
                                   color=(0, 0, 0, 1), bold=True))
        current_month = self.month_names[datetime.datetime.now().month - 1]
        self.month_spinner = Spinner(
            text=current_month, values=self.month_names, size_hint_x=0.7,
            background_color=(0.9, 0.9, 0.9, 1), background_normal='',
            color=(0, 0, 0, 1))
        month_box.add_widget(self.month_spinner)
        root.add_widget(month_box)

        hint = Label(text="Введите число и нажмите Добавить:",
                     size_hint_y=None, height=dp(30), color=(0.5, 0.5, 0.5, 1))
        root.add_widget(hint)

        input_box = BoxLayout(size_hint_y=None, height=dp(55), spacing=dp(5))
        self.date_input = TextInput(
            multiline=False, input_filter='int', font_size=dp(22),
            halign='center', size_hint_x=0.35,
            background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 0, 1), write_tab=False,
            keyboard_suggestions=False)
        self.date_input.bind(on_text_validate=self.add_date)
        input_box.add_widget(self.date_input)

        add_btn = Button(text="Добавить", size_hint_x=0.65,
                         background_color=(0.3, 0.7, 0.3, 1),
                         background_normal='', color=(1, 1, 1, 1), bold=True)
        add_btn.bind(on_press=self.add_date)
        input_box.add_widget(add_btn)
        root.add_widget(input_box)

        list_title = Label(text="Ваши рабочие дни:", size_hint_y=None, height=dp(30),
                           color=(0.5, 0.5, 0.5, 1))
        root.add_widget(list_title)

        self.scroll = ScrollView(size_hint=(1, None), height=dp(140), bar_width=dp(8))
        self.list_layout = BoxLayout(orientation='vertical', size_hint_y=None,
                                     spacing=dp(2), padding=[0, dp(5)])
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        self.scroll.add_widget(self.list_layout)
        root.add_widget(self.scroll)

        del_btn = Button(text="Удалить последнюю", size_hint_y=None, height=dp(45),
                         background_color=(0.6, 0.6, 0.6, 1), background_normal='',
                         color=(1, 1, 1, 1))
        del_btn.bind(on_press=self.remove_last)
        root.add_widget(del_btn)

        build_btn = Button(text="Построить календарь", size_hint_y=None, height=dp(55),
                           background_color=(0.9, 0.2, 0.2, 1), background_normal='',
                           color=(1, 1, 1, 1), bold=True, font_size=dp(17))
        build_btn.bind(on_press=self.build_calendar)
        root.add_widget(build_btn)

        self.image_widget = KivyImage(size_hint_y=None, height=dp(170),
                                      allow_stretch=True, keep_ratio=True)
        root.add_widget(self.image_widget)

        self.path_label = Label(
            text="Файл не сохранён", size_hint_y=None, height=dp(50),
            color=(0.3, 0.3, 0.3, 1), font_size=dp(11), halign='center',
            valign='middle', text_size=(Window.width - dp(20), None))
        root.add_widget(self.path_label)

        Clock.schedule_once(lambda dt: setattr(self.date_input, 'focus', True), 0.8)
        return root

    def add_date(self, instance):
        text = self.date_input.text.strip()
        if not text:
            return
        try:
            day = int(text)
        except ValueError:
            return
        if not (1 <= day <= 31):
            return
        if day in self.work_days:
            self.date_input.text = ""
            return
        self.work_days.append(day)
        idx = len(self.work_days)
        row = DateRow(idx, day)
        self.list_layout.add_widget(row)
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.05)
        self.date_input.text = ""
        Clock.schedule_once(self._refocus, 0.05)

    def _refocus(self, dt):
        self.date_input.focus = True

    def remove_last(self, instance):
        if not self.work_days:
            return
        self.work_days.pop()
        if self.list_layout.children:
            self.list_layout.remove_widget(self.list_layout.children[0])
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.05)

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message, color=(0, 0, 0, 1),
                                 halign='center', valign='middle'))
        close_btn = Button(text="OK", size_hint_y=None, height=dp(45),
                          background_color=(0.9, 0.2, 0.2, 1),
                          background_normal='', color=(1, 1, 1, 1), bold=True)
        content.add_widget(close_btn)
        popup = Popup(title=title, content=content, size_hint=(0.85, 0.35),
                      background='', background_color=(1, 1, 1, 1),
                      separator_color=(0.9, 0.2, 0.2, 1),
                      title_color=(0, 0, 0, 1), title_size=dp(20))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def draw_calendar_image(self, month, work_days):
        year = datetime.datetime.now().year
        cal = calendar.monthcalendar(year, month)
        width, height = 700, 900
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)

        font_paths = ["/system/fonts/Roboto-Regular.ttf",
                      "/system/fonts/DroidSans.ttf",
                      "/system/fonts/NotoSans-Regular.ttf"]
        font_title = font_days = font_num = font_total = None
        for fp in font_paths:
            if os.path.exists(fp):
                try:
                    font_title = ImageFont.truetype(fp, 50)
                    font_days = ImageFont.truetype(fp, 28)
                    font_num = ImageFont.truetype(fp, 36)
                    font_total = ImageFont.truetype(fp, 32)
                    break
                except Exception:
                    continue
        if font_title is None:
            font_title = ImageFont.load_default()
            font_days = font_title
            font_num = font_title
            font_total = font_title

        title = f"{self.month_names[month - 1]} {year}"
        bbox = draw.textbbox((0, 0), title, font=font_title)
        tw = bbox[2] - bbox[0]
        draw.text(((width - tw) / 2, 25), title, font=font_title, fill='black')

        days_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        start_x = 40
        col_width = (width - 80) / 7
        for i, dn in enumerate(days_names):
            bbox = draw.textbbox((0, 0), dn, font=font_days)
            w = bbox[2] - bbox[0]
            x = start_x + i * col_width + (col_width - w) / 2
            draw.text((x, 110), dn, font=font_days, fill='gray')

        grid_start_y = 170
        row_height = 95
        for wi, week in enumerate(cal):
            for di, day in enumerate(week):
                if day == 0:
                    continue
                x_center = start_x + di * col_width + col_width / 2
                y_center = grid_start_y + wi * row_height + row_height / 2
                if day in work_days:
                    draw.ellipse([x_center - 32, y_center - 32,
                                  x_center + 32, y_center + 32], fill='#E53935')
                    color = 'white'
                else:
                    color = 'black'
                s = str(day)
                bbox = draw.textbbox((0, 0), s, font=font_num)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                draw.text((x_center - w / 2, y_center - h / 2 - 8), s,
                          font=font_num, fill=color)

        total_text = f"Итого рабочих дней: {len(work_days)}"
        bbox = draw.textbbox((0, 0), total_text, font=font_total)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        padding = 20
        box_x1 = (width - tw) / 2 - padding
        box_y1 = 780
        box_x2 = (width + tw) / 2 + padding
        box_y2 = box_y1 + th + padding * 2
        draw.rectangle([box_x1, box_y1, box_x2, box_y2],
                       fill='#FFEBEE', outline='#E53935', width=3)
        draw.text(((width - tw) / 2, box_y1 + padding), total_text,
                  font=font_total, fill='#C62828')
        return img

    def build_calendar(self, instance):
        if not self.work_days:
            self.show_popup("Ошибка", "Вы не добавили ни одной даты!")
            return
        try:
            month = self.month_names.index(self.month_spinner.text) + 1
        except ValueError:
            self.show_popup("Ошибка", "Выберите месяц из списка")
            return
        img = self.draw_calendar_image(month, self.work_days)
        save_dir = '/storage/emulated/0/Download'
        if not os.path.exists(save_dir):
            save_dir = self.user_data_dir
        path = os.path.join(save_dir, 'calendar_result.png')
        try:
            img.save(path)
        except Exception:
            path = os.path.join(self.user_data_dir, 'calendar_result.png')
            try:
                img.save(path)
            except Exception as e:
                self.show_popup("Ошибка", f"Не удалось сохранить: {e}")
                return
        self.image_widget.source = path
        self.image_widget.reload()
        self.path_label.text = f"Файл сохранён:\n{path}"
        Clock.schedule_once(self._refocus, 0.3)


if __name__ == '__main__':
    CalendarApp().run()
