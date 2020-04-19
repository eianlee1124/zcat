#!/usr/bin/env python3


from decimal import Decimal



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


if __name__ == "__main__":
    assert Price('1000.1234') == 1000.1234000
    assert Price('1000.1234') != 1000.123400000001
    assert Price(1000) == 1000.0000000
    assert Price() == 0
    
    float_pos_amount = Amount(0.1234)
    str_pos_amount = Amount('0.1234')
    
    float_neg_amount = Amount(-0.1234)
    str_neg_amount = Amount('-0.1234')
    
    assert float_pos_amount == str_pos_amount
    assert float_neg_amount == str_neg_amount
    
    assert -float_pos_amount == str_neg_amount
    assert -str_pos_amount == float_neg_amount
    
    # 잘못된 타입의 args 전달 테스트
    for obj in [Price, Amount]:
        try:
            inappropriate_args = obj({})
        except TypeError:
            pass
        else:
            raise
        