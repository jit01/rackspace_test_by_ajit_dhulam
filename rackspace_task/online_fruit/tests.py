import unittest
from .constants import item_price
from .views import CalculatePrice


class TestCalculatePrice(unittest.TestCase):
    def setUp(self):
        self.context = {'item': [], 'value': [], 'total': 0}
        self.coffee = 2
        self.chai = 2
        self.milk = 2
        self.apple = 3
        self.oatmeal = 2
    
    def test_calculate_coffee(self):
        assert self.context['item'] == []
        CalculatePrice().calculate_coffee(
            quantity=self.coffee,
            cur_value=item_price['coffee'],
            context=self.context
        )
        # Rule 1st BOGO -- Buy-One-Get-One-Free Special on Coffee. (Unlimited)
        assert self.context['item'] == ['coffee', 'coffee', 'BOGO']
        assert self.context['value'] == [11.23, 11.23, -11.23]

    def test_calculate_apple(self):
        assert self.context['item'] == []
        CalculatePrice().calculate_apple(
            quantity=self.apple,
            cur_value=item_price['apple'],
            context=self.context
        )
        # Rule 2nd APPL -- If you buy 3 or more bags of Apples, the price drops to $4.50.
        assert self.context['item'] == ['apple', 'APPL', 'apple', 'APPL', 'apple', 'APPL']
        assert self.context['value'] == [6.0, -1.5, 6.0, -1.5, 6.0, -1.5]

    def test_calculate_chai(self):
        assert self.context['item'] == []
        CalculatePrice().calculate_chai(
            chai_quantity=self.chai,
            milk_quantity=self.milk,
            chai_cur_value=item_price['chai'],
            context=self.context
        )
        # Rule 3rd CHMK -- Purchase a box of Chai and get milk free. (Limit 1)
        assert self.context['item'] == ['chai', 'chai', 'milk', 'CHMK']
        assert self.context['value'] == [3.11, 3.11, 4.75, -4.75]

    def test_calculate_oatmeal(self):
        assert self.context['item'] == []
        CalculatePrice().calculate_oatmeal(
            quantity=self.oatmeal,
            apple_quantity=self.apple,
            context=self.context
        )
        # Rule 4th APOM -- Purchase a bag of Oatmeal and get 50% off a bag of Apples
        # Here I consider limit 1, so on 1 oatmeal pack purchase 50% off on apples pack
        # i.e. 3 apple so 18 rs 50% is 9, therefor -9.0 of 18 rs
        self.assertEqual(self.context['item'], ['oatmeal', 'oatmeal', 'APOM'])
        self.assertEqual(self.context['value'], [3.69, 3.69, -9.0])


if __name__ == "__main__":
    unittest.main()