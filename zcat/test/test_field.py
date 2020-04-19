#!/usr/bin/env python3



from operator import neg


class Price(float):
    """Price field object. inherite from `float`
    """
    __slots__ = ('value')
    
    def __init__(self, value=0.0):
        if isinstance(value, (int, str)):
            value = float(value)
        self.value = value

    def __repr__(self):
        return "\r%s('%.8f')" % (self.__class__.__name__, self.value)
        
    def __neg__(self):
        return Price(-self.value)
    
    def __abs__(self):
        return Price(abs(self.value))
    
    
class Amount(float):
    """Amount field object. inherite from `float`
    """
    __slots__ = ('value')

    def __init__(self, value=0.0):
        if isinstance(value, (int, str)):
            value = float(value)
        self.value = value

    def __repr__(self):
        return "\r%s('%.8f')" % (self.__class__.__name__, self.value)
    
    def __neg__(self):
        return Amount(-self.value)
    
    def __abs__(self):
        return Amount(abs(self.value))


if __name__ == "__main__":
    pos_price = Price(7200.1234)
    assert Price(7200.1234) == neg(-7200.1234) == neg(Price(-7200.1234)) == Price(neg(-7200.1234)) == abs(Price(-7200.1234)) == pos_price # positive 테스트
    
    assert Price('1000.1234') == 1000.1234000       # str == float 테스트
    assert Price('1000.1234') != 1000.123400000001  # str != float 테스트
    assert Price(1000) != 1000.0000001              # int != float 테스트
    assert Price() == 0                             # int == float 테스트
    
    float_pos_amount = Amount(0.1234)
    str_pos_amount = Amount('0.1234')
    
    float_neg_amount = Amount(-0.1234)
    str_neg_amount = Amount('-0.1234')
    
    assert float_pos_amount == str_pos_amount
    assert float_neg_amount == str_neg_amount
    
    assert -float_pos_amount == str_neg_amount
    assert -str_pos_amount == float_neg_amount
    
    # 잘못된 타입의 args 전달 테스트
    for dtype in [dict, list, tuple, bytes, bytearray]:
        for obj in [Price, Amount]:
            try:
                inappropriate_args = obj(dtype)
            except TypeError:
                pass
            else:
                raise
        