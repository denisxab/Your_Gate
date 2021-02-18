
from re import match, findall
from yourgate_logic import Yourgate_Logic
from front import Front_YG
from kivy.utils import get_color_from_hex
from kivy.uix.pagelayout import PageLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import RoundedRectangle
from kivy.graphics import RoundedRectangle, Color
# Подключение виртуальной клавиатуры
Config.set("kivy", "keyboard_mode", "systemanddock")
# Операционная система
# pc | phone
PLATFORM = 'pc'


class Container (PageLayout):
    #--------------------------------------------------#
    # Классы
    # Логика
    YGL = Yourgate_Logic()
    # Внешний вид таблицы
    Front = Front_YG()
    #--------------------------------------------------#
    # Переменные
    # Переменная с помощью которой определяем пределы
    length_swap_flag = 0
    # Массив с текстом ключа
    data_key = []
    # Массив с примичаниями
    data_notes = []
    # Таблица со всеми элементами ключей
    all_table = []
    # Выбранный ключ
    selected_key = ''
    # Тригер для менеджера ключей для выхода из рекурсии
    trigger_table = False
    # Вспомогательный словарь с ключами и премечаниями
    dict_data_key = {}
    # Переменная сохраняющая прошлое значения текста примечания
    tmp_text_notes = ''
    # Через сколько символов обрезать текст
    cap_text = 24
    #--------------------------------------------------#

    #--------------------------------------------------#
    # Меню
    mega_m = ()
    mega_b = ()

    main_menu = ObjectProperty()
    menu_create_key = ObjectProperty()
    menu_get_key = ObjectProperty()
    menu_info = ObjectProperty()
    menu_manage_key = ObjectProperty()

    bolvanka_main = ObjectProperty()
    bolvanka_create_key = ObjectProperty()
    bolvanka_get_key = ObjectProperty()
    bolvanka_info = ObjectProperty()
    bolvanka_manage_key = ObjectProperty()

    menu_tmp = ObjectProperty()

    label_swap_node = ObjectProperty()

    #--------------------------------------------------#

    # Page 0
    text_input_main = ObjectProperty()
    label_info_key = ObjectProperty()
    text_input_main_cdc = ObjectProperty()

    # Page 1
    label_text_input_public_key = ObjectProperty()
    text_input_response_key = ObjectProperty()
    label_key_create = ObjectProperty()

    # Page 2
    text_input_public_key = ObjectProperty()
    label_text_input_response_key = ObjectProperty()
    label_key_get = ObjectProperty()

    # Page 4
    box_manage_key = ObjectProperty()

    text_right = ObjectProperty()
    right_swap_node = ObjectProperty()

    text_left = ObjectProperty()
    left_swap_node = ObjectProperty()

    # Page 5
    text_input_add_key = ObjectProperty()
    text_input_add_notes = ObjectProperty()

    Color_Content = get_color_from_hex("#424246")
    Color_True = get_color_from_hex("#52AF37")

    #--------------------------------------------------#

    #--------------------------------------------------#
    # Навигация
    def Swap_Main(self):
        self.menu_tmp.state = "normal"
        if self.dict_data_key.get(self.selected_key):

            tmp = self.dict_data_key[self.selected_key]

            # Обрезать стоку
            tmp = self.YGL.YL_Short_Str(tmp, self.cap_text)

            self.label_info_key.text = tmp
            self.YGL.YL_Create_Encryption_Table(self.selected_key)
        else:
            self.YGL.YL_Del_Data()
            self.label_info_key.text = "*Ключ не выбран*"

        self.page = 0
        pass

    def Swap_Create_Public_Key(self):
        self.menu_tmp.state = "normal"
        self.page = 1
        pass

    def Swap_Get_Key(self):
        self.menu_tmp.state = "normal"
        self.page = 2
        pass

    def Swap_Info(self):
        self.menu_tmp.state = "normal"
        self.page = 3
        pass

    def Swap_Manage_Key(self):
        self.menu_tmp.state = "normal"
        self.page = 4
        self.Manage_Key()
        pass

    def Swap_Add_Key(self):
        self.page = 5
        pass

    # Создаем массив с меню
    def Make_Menu(self):
        if not self.mega_m or self.mega_b:
            self.mega_m = (
                self.main_menu,
                self.menu_create_key,
                self.menu_get_key,
                self.menu_info,
                self.menu_manage_key)

            self.mega_b = (
                self.bolvanka_main,
                self.bolvanka_create_key,
                self.bolvanka_get_key,
                self.bolvanka_info,
                self.bolvanka_manage_key)

    def Menu_Main(self, tg):
        # Киви не дает возможность создать массив в инициализации поэтому создаем его при вызове функции.
        self.Make_Menu()

        self.menu_tmp = tg
        if tg.state == "down":
            for x in self.mega_m:
                x.size_hint_y = 0.3
                x.opacity = 1

            for y in self.mega_b:
                y.height = '0'
                y.size_hint_y = None

        else:
            for y in self.mega_m:
                y.size_hint_y = None
                y.opacity = 0
                y.height = '0'

            for x in self.mega_b:
                x.size_hint_y = 0.3
        pass

    #--------------------------------------------------#

    #--------------------------------------------------#

    def Translate_cdc_21(self):
        if self.selected_key:
            self.text_input_main_cdc.text = self.YGL.YL_Encryption_Text(
                self.text_input_main.text)
        pass

    def Translate_ascii(self):
        if self.selected_key:
            self.text_input_main.text = self.YGL.YL_Decoding_Text(
                self.text_input_main_cdc.text)
        pass

    #--------------------------------------------------#

    #--------------------------------------------------#
    # Менеджер ключей

    def Manage_Key(self):

        self.data_key = self.YGL.YL_Data_Key()
        self.data_notes = self.YGL.YL_Data_Notes()
        self.dict_data_key = {k: n for k, n in zip(
            self.data_key, self.data_notes)}
        # Переменная с помощью которой определяем предел
        self.length_swap_flag = 0
        self.right_swap_node.opacity = 0
        self.left_swap_node.opacity = 0

        if len(self.data_key) > 5:
            self.right_swap_node.opacity = 1
            self.right_swap_node.size_hint_y = 1
            self.text_right.text = str(len(self.data_key) - 5)

        if not self.all_table:
            # Отчищаем список выбранной кнопки
            self.selected_user_flag = ''
            # Создаем массив со всеми возможными кнопками
            for k, n in zip(self.data_key, self.data_notes):
                w = self.Front.Table()

                w.children[1].children[0].children[1].text = k
                w.children[0].children[0].text = n
                self.all_table.append(w)

        else:
            # Снимаем выбор со всех кнопка
            for x in self.all_table:
                x.children[1].children[0].state = 'normal'

            # При добавление новых флагов
            if len(self.all_table) < len(self.data_key):
                # Создаем массив со всеми имеющимися ключами
                flg = [
                    x.children[1].children[0].children[1].text for x in self.all_table]
                # Проверяем базу и отображенные ключи
                for x in self.data_key:
                    # Если такого ключа нет то добавляем его
                    if not x in flg:
                        w = self.Front.Table()
                        w.children[1].children[0].children[1].text = x
                        w.children[0].children[0].text = self.dict_data_key[x]
                        self.all_table.append(w)

            # При удаление флага
            elif len(self.all_table) > len(self.data_key):
                for x in self.all_table:
                    if not x.children[1].children[0].children[1].text in self.data_key:
                        x.clear_widgets()
                        self.all_table.remove(x)

            # На случай если будут переименованны флаги
            else:
                i = 0
                for k, n in zip(self.data_key, self.data_notes):
                    self.all_table[i].children[1].children[0].children[1].text = k
                    self.all_table[i].children[0].children[0].text = n
                    i += 1

        self.Display_Table()
        pass

    # Удаление элемента
    def Del_Key(self, element_table):
        self.data_key.remove(
            element_table.children[1].children[0].children[1].text)

        self.Front.notes.remove(element_table.children[0].children[0])
        self.Front.key.remove(
            element_table.children[1].children[0].children[1])

        self.YGL.YL_Save_Result(self.data_key, self.data_notes)
        self.Manage_Key()
        pass

    # Добавление ключа
    def Add_Key(self):
        # Если введен что-то есть в поле для ключ
        if self.text_input_add_key.text:
            # Добавляем это в базу
            self.data_key.append(self.text_input_add_key.text)
            self.data_notes.append(self.text_input_add_notes.text)
        # Обновляем базу
        self.YGL.YL_Save_Result(self.data_key, self.data_notes)
        self.Manage_Key()
        self.page = 4
        pass

    # Отображение элементов
    def Display_Table(self):
        # Отчищаем таблицу
        self.box_manage_key.clear_widgets()
        # Вставляем 5 элементов
        for x in self.all_table[5*self.length_swap_flag:5*self.length_swap_flag+5:]:
            self.box_manage_key.add_widget(x)
        # Добавляем болванки если не хвататет элементов
        i = 5-(len(self.data_key)-(self.length_swap_flag*5))
        while i > 0:
            self.box_manage_key.add_widget(Widget(size_hint_y=1))
            i -= 1
        pass

    # Перелистнуть список флагов влево
    def Swap_Left_List_Flag(self):
        # Ограничители передвижения влево
        if self.length_swap_flag-2 < 0:
            self.left_swap_node.opacity = 0
            self.left_swap_node.size_hint_y = None
            self.left_swap_node.height = '0'

        else:
            self.left_swap_node.opacity = 1
            self.left_swap_node.size_hint_y = 1

        self.right_swap_node.opacity = 1
        self.right_swap_node.size_hint_y = 1

        # Отмечаем о переходе влево
        self.length_swap_flag -= 1
        self.Display_Table()
        pass

    # Перелистнуть список флагов вправо
    def Swap_Right_List_Flag(self):
        # Ограничители передвижения вправо
        if self.length_swap_flag+2 > (len(self.data_key)-1)//5:
            self.right_swap_node.opacity = 0
            self.right_swap_node.size_hint_y = None
            self.right_swap_node.height = '0'
        else:
            self.right_swap_node.opacity = 1
            self.right_swap_node.size_hint_y = 1

        self.left_swap_node.opacity = 1
        self.left_swap_node.size_hint_y = 1

        # Отмечаем о переходе вправо
        self.length_swap_flag += 1
        self.Display_Table()
        pass

    # Записать выбранный ключ
    def _Select_Key(self, but_t, root_bt):
        # Тригер нужен для остановки рекурсии
        if not self.trigger_table:
            # Если кнопка нажата
            if but_t.state == "down":
                # Переключаме тригер снимаем все нажатия с других кнопок, а после ставим нажатие на выбранную кнопку
                self.trigger_table = True
                for x in self.all_table:
                    x.children[1].children[0].children[1].state = "normal"
                but_t.state = "down"
                # Записываем ключ для того чтобы на его основе была создана база для перевода текста
                self.selected_key = but_t.text
                # Перекрашивам в зеленый свет поле с примечаниями
                root_bt.children[0].canvas.before.children[0].rgba = self.Color_True
                # Обрезать текст и Обновляем нижний Лейбал о том какой флаг выбран
                self.label_swap_node.text = self.YGL.YL_Short_Str(
                    root_bt.children[0].children[0].text, self.cap_text)
                self.trigger_table = False

            # Если ни одна кнопка не нажата то все убираем
            else:
                self.selected_key = ''
                self.label_swap_node.text = ''
                root_bt.children[0].canvas.before.children[0].rgba = self.Color_Content

        # Все примечанями перекрашиваем в исходный цвет
        else:
            root_bt.children[0].canvas.before.children[0].rgba = self.Color_Content
        pass

    # Сохранить текст из примечаний при расфокусировки
    def Change_Text_Notes(self, foc, notes_widget):
        # Если расфокусировался
        if not foc:
            # Если текстовое поле изменилось -> то перезаписываем базу примечаний
            if self.tmp_text_notes != notes_widget.text:
                # Проверяем всю базу с примечаниями
                for i, x in enumerate(self.Front.notes):
                    # Если такое примечание найдено то тогда мы знаем его индекс и по этому идекусу заменяем на изменное предложение, а после сохраняем результат и обновляем базу
                    if x == notes_widget:
                        self.data_notes.insert(i, notes_widget.text)
                        self.data_notes.pop(i+1)
                        self.YGL.YL_Save_Result(self.data_key, self.data_notes)
                        # Обновляем нижний лейбол показывающий выбранный флаг
                        self.label_swap_node.text = self.YGL.YL_Short_Str(
                            notes_widget.text, self.cap_text)
                        self.Manage_Key()
                        break
        # Если в фокусе
        else:
            # Записываем прошлое значение текста примечания
            self.tmp_text_notes = notes_widget.text
        pass

    #--------------------------------------------------#

    #--------------------------------------------------#
    # Создать публичный ключ

    def Create_Public_Key(self):
        self.label_text_input_public_key.text = self.YGL.YL_Create_Public_Key()
        pass

    # Записать публичный ключ и создать на его основе ответный ключ, сохранить приватный ключ
    def Write_Public_Key_Create_Response_Key(self):
        self.label_text_input_response_key.text = self.YGL.YL_Write_Public_Key_Create_Response_Key(
            self.text_input_public_key.text)

        #!!!
        self.label_key_get.text = "Ваш ключ: {}".format(self.YGL._K_Server)
        self.YGL.YL_Save_Key(self.YGL._K_Server)
        pass

    # Записать ответный ключ и сохранить приватный ключ
    def Write_Response_Key(self):
        tmp = self.YGL.YL_Write_Response_Key(self.text_input_response_key.text)

        #!!!
        self.label_key_create.text = "Ваш ключ: {}".format(tmp)
        self.YGL.YL_Save_Key(tmp)
        pass
    #--------------------------------------------------#

    #--------------------------------------------------#


class yourgateApp(App):
    # Сохранять результат работы при закрытие программы
    def _exit_check(self, *args):
        self.layout.YGL.YL_Save_Result(
            self.layout.data_key, self.layout.data_notes)

    def build(self):
        self.layout = Container()
        # Сохранять результат работы при закрытие программы
        Window.bind(on_request_close=self._exit_check)
        if PLATFORM == 'pc':
            # Размер окна
            Window.size = (450, 800)
            # Неизменяемый размер окна
            Config.set('graphics', 'resizable', 0)
            # Закрывать программу по нажатию escape
            Config.set('kivy', 'exit_on_escape', 1)

        return self.layout


if __name__ == "__main__":
    yourgateApp().run()
