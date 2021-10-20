import random


class Pontifex():
    """A cipher object implementing the Pontifex (also known as Solitaire)
    cipher designed by Bruce Schneier and made popular in Neal Stephenson's
    Cryptonomicon.
    """

    def __init__(self, size=54):
        """Pontifex object

        Args:
            size (int, optional): [description]. Defaults to 54.
        """
        self.deck_size = size
        self._deck = [x for x in range(1, self.deck_size + 1)]
        self._a = self.deck_size - 1
        self._b = self.deck_size
        self._shuffle()

    def _shuffle(self):
        random.shuffle(self._deck)

    def _inspect(self):
        print(self._deck)

    def _relocate(self, value, offset):
        index = self._deck.index(value)
        self._deck.pop(index)
        target = index + offset
        if target >= self.deck_size:
            target = target - self.deck_size + 1
        self._deck.insert(target, value)

    def _triple_cut(self):
        a_idx = self._deck.index(self._a)
        b_idx = self._deck.index(self._b)
        start = min(a_idx, b_idx)
        finish = max(a_idx, b_idx)

        top = self._deck[0:start]
        middle = self._deck[start:finish+1]
        bottom = self._deck[finish+1:]
        self._deck = bottom + middle + top

    def _count_cut(self):
        count = self._deck[-1]
        if count == self._b:
            count =self._a

        top = self._deck[0:count]
        middle = self._deck[count:-1]
        bottom = self._deck[self.deck_size-1]

        self._deck = middle + top + [bottom]

    def _count_get(self):
        count = self._deck[0]
        if count == self._b:
            count = self._a
        drip = self._deck[count]
        if drip >= self._a:
            return 0
        return drip

    def _next_byte(self):
        self._relocate(self._a, 1)
        self._relocate(self._b, 2)
        self._triple_cut()
        self._count_cut()
        byte = self._count_get()
        if not byte:
            byte = self._next_byte()
        return byte

    @property
    def key(self):
        """Key getter

        Returns:
            bytearray: The cipher's initial deck state.
        """
        return bytearray(self._deck)

    @key.setter
    def key(self, key: bytearray):
        deck = [int(x) for x in key]
        self._deck = deck

    def encrypt(self, msg):
        msg = ''.join(x for x in msg if x.isalpha()).upper()
        ciphertext = ""
        for char in msg:
            val = ord(char) - 64
            val += self._next_byte()
            while val > 26:
                val -= 26
            ciphertext += chr(val+64)
        return ciphertext


if __name__ == "__main__":
    cipher = Pontifex(10)
    ciphertext = cipher.encrypt("aaatest kjdf jaldf")
    print(ciphertext)
