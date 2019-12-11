from tools import AESCipher


class Person(object):
    def __init__(self, g, p, primer, name, messages, multi_keys=None):
        # ну это конструктор, понятно всё
        self.g = g
        self.p = p
        self.prime = primer.get_prime()
        self.name = name
        self.keys = {}
        self.messages = messages
        self.A = None
        self.multi_keys = multi_keys
        self.log = []

    def start_communication_with(self, name):
        # эта функция генерирует и отправляет A в начале общения
        self.A = (self.g ** self.prime) % self.p
        return self.name, name, "my param", self.A

    def read_data(self, data):
        name, _, action, data = data
        if action == "my param":
            # если нам прислали A - вычисляем, записываем общий ключ и сразу создаём класс для будущих шифрований/расшифрований
            K = (int(data) ** self.prime) % self.p
            self.keys[name] = AESCipher(str(K))

        elif name in self.keys:
            # если ключ уже есть, то декодируем, что нам прислали
            data = self.decode(self.keys[name], data)
            # логируем
            log_data = "   Получено | {} => {} # {} => {}".format(name, self.name, action, data)
            print(log_data)
            self.log.append(log_data)
            # смотрим, что ответить по заранее заготовленным фразочкам
            if data in self.messages:
                log_data = "   Отправлено | {} => {} # {} => {}".format(self.name, name, action, self.messages[data])
                print(log_data)
                self.log.append(log_data)
                return self.name, name, "message", self.encode(self.keys[name], self.messages[data])
        if self.A is None:
            # если оказалось, что A ещё не сгенерили - то генерим и отправляем
            return self.start_communication_with(name)
        # если вдруг фразочки для ответа не нашлось, ну отправляем стандартное Привет и логируем
        data = "Привет"
        log_data = "   Отправлено | {} => {} # {} => {}".format(self.name, name, action, data)
        print(log_data)
        self.log.append(log_data)
        return self.name, name, "message", self.encode(self.keys[name], data)

    @staticmethod
    def encode(aes, data):
        if data is None:
            return None
        return aes.encrypt(bytes(data, 'utf-8'))

    @staticmethod
    def decode(aes, data):
        if data is None:
            return None
        return aes.decrypt(data)
