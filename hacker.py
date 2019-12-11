from person import Person
from tools import AESCipher


class Hacker(Person):
    def read_data(self, sent):
        # ловим пакет с данным
        send_from, send_to, action, data = sent
        if action == "my param":
            # если прислали A - мы высчитываем общий ключ, сохраняем, а A в сообщении подмениваем на своё
            K = (int(data) ** self.prime) % self.p
            self.keys[send_from] = AESCipher(str(K))
            _, _, action, data = self.start_communication_with("")
            return send_from, send_to, action, data
        elif send_from in self.keys and send_to in self.keys:
            # если идет общение и у нас есть нужные ключи - то декодируем сообщение
            data = self.decode(self.keys[send_from], data)
            # смотрим, можем ли мы заменить фразочку, если можем - то меняем
            if data in self.messages:
                data = self.messages[data]
            # кодируем сообщение и отправляем
            # важный момент: даже если мы не хотим пока что читать и менять пересписку, нам всё равно надо все сообщения раскодировать и кодировать заново
            return send_from, send_to, "message", self.encode(self.keys[send_to], data)
        return sent
