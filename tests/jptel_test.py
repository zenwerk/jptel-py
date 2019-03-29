# -*- coding=utf-8 -*-
import pytest

from jptel import (
    normalize,
    validate,
    split,
)
from jptel.exception import (
    InvalidCharacterException,
    InvalidTelephoneNumberException,
)


def test_normalize():
    result = normalize('0123456789')
    assert result == '0123-45-6789'

    result = normalize('0222522222')
    assert result == '022-252-2222'

    result = normalize('０１２３４５６７８９')
    assert result == '0123-45-6789'

    result = normalize('０１２ー３４５６７８-９')
    assert result == '0123-45-6789'

    result = normalize('０１２３−４５−6789')
    assert result == '0123-45-6789'

    result = normalize('-0９０-１２３ー4５６-７８-')
    assert result == '090-1234-5678'

    with pytest.raises(InvalidCharacterException):
        normalize('０９０あ−７a９３３ー−４０４３1234567890-')

    with pytest.raises(InvalidCharacterException):
        normalize('---')


def test_validate():
    # valid telephone number
    assert validate('0123456789')
    assert validate('0222522222')
    assert validate('022-252-2222')
    assert validate('０１２３４５６７８９')
    assert validate('０１２３-４５ー６７８９')
    assert validate('０12３-４５ー６78９')
    assert validate('０１２３−４５−6789')

    # invalid telephone number
    assert not validate('022252-2222')
    assert not validate('０１２ー３４５６７８-９')
    assert not validate('０１２３４５ー６７８９')
    assert not validate('-0９０-１２３ー4５６-７８-')
    assert not validate('０９０あ−７a９３３ー−４０４３1234567890-')
    assert not validate('--')


def test_split():
    # valid telephone number
    result = split('0312345678')
    assert '03' == result['area_code']
    assert '1234' == result['city_code']
    assert '5678' == result['subscriber_code']

    result = split('03-1234-5678')
    assert '03' == result['area_code']
    assert '1234' == result['city_code']
    assert '5678' == result['subscriber_code']

    result = split('０３１２３４５６７８')
    assert '03' == result['area_code']
    assert '1234' == result['city_code']
    assert '5678' == result['subscriber_code']

    result = split('０３１-２３４５ー６７８')
    assert '03' == result['area_code']
    assert '1234' == result['city_code']
    assert '5678' == result['subscriber_code']

    result = split('0222522222')
    assert '022' == result['area_code']
    assert '252' == result['city_code']
    assert '2222' == result['subscriber_code']

    result = split('0997123456')
    assert '0997' == result['area_code']
    assert '12' == result['city_code']
    assert '3456' == result['subscriber_code']

    result = split('0996912345')
    assert '09969' == result['area_code']
    assert '1' == result['city_code']
    assert '2345' == result['subscriber_code']

    result = split('09012345678')
    assert '090' == result['area_code']
    assert '1234' == result['city_code']
    assert '5678' == result['subscriber_code']

    result = split('0120123456')
    assert '0120' == result['area_code']
    assert '123' == result['city_code']
    assert '456' == result['subscriber_code']

    result = split('08001234567')
    assert '0800' == result['area_code']
    assert '123' == result['city_code']
    assert '4567' == result['subscriber_code']

    # invalid telephone number
    with pytest.raises(InvalidTelephoneNumberException):
        split('00000000000')

    with pytest.raises(InvalidTelephoneNumberException):
        split('００００００００００')

    with pytest.raises(InvalidTelephoneNumberException):
        split('0312')

    with pytest.raises(InvalidTelephoneNumberException):
        split('０３１２')

    with pytest.raises(InvalidTelephoneNumberException):
        split('090')

    with pytest.raises(InvalidCharacterException):
        split('hogefugapiyo')

    with pytest.raises(InvalidCharacterException):
        split('あいうえお')
