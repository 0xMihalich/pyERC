from string import hexdigits
from struct import pack, unpack


class ERCError(Exception):
    "any error"


def erc_decoder(input_erc: str) -> str:
    "калькулятор ERC для автомагнитол"
    
    if not all(i in hexdigits for i in input_erc):
        raise ERCError("Invalid ERC code.")
    
    input_erc = bytes.fromhex(input_erc)

    if len(input_erc) != 8:
        raise ERCError("Invalid number of characters.")
        
    fp_int, sp_int = unpack(">2I", input_erc)


    def _reverse(sp_int: int) -> int:
        "функция побитного сдвига"

        reverse_sp_int = 0

        for i in range(0, 32):
            temp = sp_int >> (31 - i)
            temp &= 1
            temp = temp << i
            reverse_sp_int |= temp

        return reverse_sp_int


    sp_int = _reverse(sp_int)

    xor = fp_int ^ sp_int
    ret = (xor - 0xE010A11) + 2**32

    return pack(">I", ret & 0xffffffff).hex().upper()


if __name__ == "__main__":
    # Please enter your ERC: A4000E00359A7760
    test_erc = input("Введите ERC-код: ")
    # Returned answer is: 94ED4D9B
    print(f"Код разблокировки: {erc_decoder(test_erc)}")
