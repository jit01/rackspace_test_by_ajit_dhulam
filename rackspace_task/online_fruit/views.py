from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import ItemForm
from .constants import item_price, Chai, Apple, Coffee, Milk, Oatmeal, BOGO, CHMK, APPL, APOM


class CalculatePrice(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = {'form': ItemForm()}
        return self.render_to_response(context=context)

    def post(self, request, *args, **kwargs):
        form = ItemForm(request.POST)
        if form.is_valid():
            context = {'item': [], 'value': [], 'total': 0}
            data = request.POST
            for key, value in data.items():
                item_value = item_price.get(key)
                if item_value and value:
                    if key == Chai:
                        self.calculate_chai(
                            chai_quantity=int(value),
                            milk_quantity=int(data.get('milk')) if data.get('milk') else 0,
                            chai_cur_value=item_value,
                            context=context
                        )
                    if key == Coffee:
                        self.calculate_coffee(quantity=int(value), cur_value=item_value, context=context)
                    if key == Apple:
                        self.calculate_apple(quantity=int(value), cur_value=item_value, context=context)
                    if key == Oatmeal:
                        self.calculate_oatmeal(
                            quantity=int(value),
                            apple_quantity=int(data.get('apple')) if data.get('apple') else 0,
                            context=context
                        )
                    if key == Milk:
                        if int(value) >= 1 and data.get('chai') == '':
                            self.calculate_milk(quantity=int(value), cur_value=item_value, context=context)
                        elif int(data.get('chai') if data.get('chai') else 0) >= 1 and int(value) > 1:
                            self.calculate_milk(quantity=int(value) - 1, cur_value=item_value, context=context)
            context['total'] = sum(context['value'])
            print(context)
            return render(request, 'success.html', context=context)

        return render(request, 'negativeerror.html')

    def calculate_coffee(self, quantity, cur_value, context):
        """
        BOGO Coupon Code, Buy-One-Get-One-Free special on Coffee. (Unlimited)
        """
        if quantity % 2 == 0:
            actual_billable_quantity = quantity // 2
        else:
            actual_billable_quantity = quantity // 2 + 1

        discount_quantity = quantity - actual_billable_quantity
        self.update_context(quantity, 'coffee', cur_value, context)
        self.update_context(discount_quantity, BOGO, -1*cur_value, context)

    def calculate_chai(self, chai_quantity, milk_quantity, chai_cur_value, context):
        """
        CHMK Coupon Code, Purchase a box of chai and get milk free. limit 1
        """
        milk_value = item_price.get('milk')
        self.update_context(chai_quantity, 'chai', chai_cur_value, context)

        if milk_quantity:
            context['item'].append('milk')
            context['value'].append(milk_value)
            context['item'].append(CHMK)
            context['value'].append(-1 * milk_value)

    def calculate_apple(self, quantity, cur_value, context):
        """
        AAPL Coupon Code, if you buy 3 or more bags of apples, the price drops to 4.50
        """
        remaining_quantity = quantity - 3
        if quantity >= 3:
            for item in range(3):
                context['item'].append('apple')
                context['value'].append(cur_value)
                context['item'].append(APPL)
                context['value'].append(-1 * 1.5)
            self.update_context(remaining_quantity, 'apple', cur_value, context)
        else:
            self.update_context(quantity, 'apple', cur_value, context)

    def calculate_milk(self, quantity, cur_value, context):
        self.update_context(quantity, 'milk', cur_value, context)

    def calculate_oatmeal(self, quantity, apple_quantity, context):
        """
        APOM Coupon Code, Purchase a bag of Oatmeal and get 50% off a bag of Apples
        """
        apple_price = item_price['apple']
        oatmeal_price = item_price['oatmeal']
        self.update_context(quantity=quantity, name='oatmeal', value=oatmeal_price, context=context)
        if apple_quantity > 0:
            self.update_context(1, APOM, -((apple_price*apple_quantity)/2), context)
            

    @staticmethod
    def update_context(quantity, name, value, context):
        for item in range(quantity):
            context['item'].append(name)
            context['value'].append(value)

