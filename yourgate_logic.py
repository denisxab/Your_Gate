import random
import json
import time
from data_code import CHAR_LIST, CDC_21, Number
from kivy.lang import Builder
from kivy.utils import get_color_from_hex


class Yourgate_Logic():
    def __init__(self):
        self.__a = -1
        self.__b = -1
        self.p = -1
        self._K_User = str
        self._K_Server = str
        self.KF = Key_Formation()
        self.trigger_data_encryption = str

    #################################################
    def YL_Create_Public_Key(self) -> str:
        # Сбрасываем зерно
        random.seed(int(time.time()))
        self.p = random.randint(1, 1000000000000)
        g = random.randint(1, 1000)
        self.__a = random.randint(1, 100)
        # A = g^a (mod p)
        A = (g**self.__a) % self.p
        return '{}_{}_{}'.format(CDC_21(A), CDC_21(g), CDC_21(self.p))

    def YL_Write_Public_Key_Create_Response_Key(self, A_g_p_send_cdc_21: str) -> str:
        # Сбрасываем зерно
        random.seed(int(time.time()))
        self.__b = random.randint(1, 100)
        send_num = [Number(x) for x in A_g_p_send_cdc_21.split('_')]
        A = send_num[0]
        g = send_num[1]
        p = send_num[2]
        self._K_Server = CDC_21((A**self.__b) % p)
        # B = g^b (mod p)
        B = (g**self.__b) % p
        return CDC_21(B)

    def YL_Write_Response_Key(self, b_send_cdc_21: str) -> int:
        b_send_cdc_21 = Number(b_send_cdc_21)
        # K = B^a (mod p)
        self._K_User = CDC_21((b_send_cdc_21 ** self.__a) % self.p)
        return self._K_User
    #################################################

    #################################################
    # Создать и сохранить ключ
    def YL_Save_Key(self, cdc_21_key: str):
        trigger = True
        try:
            with open('k.txt', 'r', encoding='utf-8') as add_text:
                tmp = add_text.read().split('\n')
                tmp = tmp[0::2]
                if cdc_21_key in tmp:
                    trigger = False
                    return trigger
        except FileNotFoundError:
            add_text = open('k.txt', 'w')
            add_text.close()
            return self.YL_Save_Key(cdc_21_key)

        if trigger:
            with open('k.txt', 'a', encoding='utf-8') as add_text:
                add_text.write("{}\n{}\n".format(
                    cdc_21_key, time.ctime(time.time())))
            return True

    # Сохранить базу
    def YL_Save_Result(self,  key: list, notes: list):
        with open('k.txt', 'w', encoding='utf-8') as add_text:
            tmp_k_n = ""
            for k, n in zip(key, notes):
                tmp_k_n += "{}\n{}\n".format(k, n)
            add_text.write(tmp_k_n)

    # Прочитать только ключи
    def YL_Data_Key(self) -> list:
        try:
            with open('k.txt', 'r', encoding='utf-8') as add_text:
                tmp = add_text.read().split('\n')
                tmp = tmp[0::2]
                tmp = tmp[:-1]
                return tmp[::-1]

        except FileNotFoundError:
            add_text = open('k.txt', 'w')
            add_text.close()
            return []

    # Прочитать только примечания

    def YL_Data_Notes(self) -> list:
        with open('k.txt', 'r', encoding='utf-8') as add_text:
            tmp = add_text.read().split('\n')
            tmp = tmp[1::2]
        return tmp[::-1]

    # Создает базу шифрования, если ключ измениться то создаст новую базу
    def YL_Create_Encryption_Table(self, cdc_21_key: str):
        if cdc_21_key != self.trigger_data_encryption:
            self.KF.Formation_кey(Number(cdc_21_key))
            self.trigger_data_encryption = cdc_21_key
            self.KF.Restart_Data()

    # Удалить базу
    def YL_Del_Data(self):
        add_text = open('key.json', 'w', encoding='utf-8')
        add_text.close()
    #################################################

    def YL_Encryption_Text(self, text: str):
        return self.KF.Encryption(text)

    def YL_Decoding_Text(self, cdc_21: str):
        return self.KF.Decoding(cdc_21)

    #################################################

    # Обрезать стоку
    def YL_Short_Str(self, text_long: str, len_cap: int) -> str:
        if len(text_long) > len_cap:
            text_long = list(text_long)[0:len_cap]
            text_long = "{}...".format(''.join(text_long))
        return text_long

    #################################################


class Key_Formation():
    def __init__(self):
        # Список букв
        self.character_list = CHAR_LIST
        # База с ключами
        self.__user_key = None

    def Restart_Data(self):
        self.__user_key = None

    def Get_User_Key(self) -> dict:
        if not self.__user_key:
            with open('key.json', 'r', encoding='utf-8') as json_j:
                self.__user_key = json.load(json_j)
                tmp = self.__user_key.keys()
                for x in tmp:
                    self.__user_key[x] = set(self.__user_key[x])
            return self.__user_key
        return self.__user_key

    # Создаем таблицу кодирования из зерна полученного от сервера
    def Formation_кey(self, us_seed: int):

        # Зерно из ключа
        random.seed(us_seed)
        # от 8 bit чем меньше бит тем чаще будут повторяться цифры
        bit = 16
        # Количество возможных интерпретаций
        rand = 32
        l = {}
        v = []
        try_num = False

        for x_tmp_head in self.character_list:
            l[x_tmp_head] = []

            rand = 32
            while(rand):
                # В пределах скольки бит сгенерировать случайное псевдо число
                deb = CDC_21(random.getrandbits(bit))
                # Если таких ключей нет то добавляем
                if not deb in v:
                    v.append(deb)
                # Если такой ключ уже есть то мы увеличиваем битнасть и ищем уникальный ключ
                else:
                    if not try_num:
                        tmp_i = 1
                        while(not try_num):
                            deb = CDC_21(random.getrandbits(bit+tmp_i))
                            tmp_i += 1
                            if not deb in v:
                                v.append(deb)
                                try_num = True

                try_num = False
                l[x_tmp_head].append(deb)
                rand -= 1

        # Сбрасываем ключи чтобы записались из новые базы
        self.user_key = None
        with open('key.json', 'w', encoding='utf-8') as file_j:
            json.dump(l, file_j, sort_keys=False, ensure_ascii=False)

        # Сбрасываем зерно
        random.seed(int(time.time()))

    # Кодируем сообщение
    def Encryption(self, text: str) -> str:

        red = self.Get_User_Key()
        v = [random.sample(red[x], 1)[0] for x in text if x in red]
        f = ''.join(['{}{}'.format(x, random.sample(red['|'], 1)[0])
                     for x in v])
        return f

    # Декодируем сообщение

    def Decoding(self, text: str) -> str:

        red = self.Get_User_Key()

        # Разделение по "|"
        tmp = [x for x in red['|']]
        for x in tmp:
            if len(text.split(x)) > 1:
                text = text.replace(x, ' ')

        list_code = text.split(' ')[: -1]

        red = self.Get_User_Key()
        v = {z: x[0]for x in red.items() for z in list_code if z in x[1]}
        zx = [v[x] for x in list_code if x in v]

        return str(''.join(zx))
