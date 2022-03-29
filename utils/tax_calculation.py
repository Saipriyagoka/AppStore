
class Commodity():

	def __init__(self, commodity, extra_discount=0):

		self.category = commodity['item_category'].lower()
		self.price = commodity['price']
		self.quantity = commodity['quantity']
		self.commodity = commodity
		self.extra_discount = extra_discount
		self.tax_lookup = {
			'medicine': 0.05,# '5%'
			'food': 0.05, # '5%'
			'clothes': {
				'1000': {
					'price_above': 0.12, # '12%'
					'price_below': 0.05 # '5%'
				}
			},
			'music': 0.03, # '3%'
			'imported': 0.18, # '18%'
			'books': 0, # exempted
		}

	def get_tax_perc(self):
		''' Matching with Tax lookup dictionary, which is imported from settings'''

		try:
			tax_rates = self.tax_lookup.get(self.category, 0)
			if isinstance(tax_rates, dict):
				for k, v in tax_rates.items():
					if self.price > int(k):
						tax_perc = v.get('price_above', 0)
					elif self.price < int(k):
						tax_perc = v.get('price_below', 0)
					return tax_perc
			else:
				return tax_rates
				
		except Exception as error:
			return 0
			
	def calculate_tax(self):

		try:
			tax_perc = self.get_tax_perc()
			final_price =  self.price * self.quantity
			tax_amount = final_price * tax_perc if tax_perc else 0
			discount_amount = final_price * self.extra_discount if self.extra_discount else 0
			applicable_price = final_price + tax_amount - discount_amount
			print(self.commodity, tax_amount, discount_amount, applicable_price)

			self.commodity.update({
				'final_price': final_price,
				'tax_amount': tax_amount,
				'tax_percentage': str(round(tax_perc * 100)),
				'discount_amount': discount_amount,
				'applicable_price': applicable_price
			})
			return self.commodity

		except Exception as error:
			self.commodity.update({
				'final_price': 0, 'tax_amount': 0, 'applicable_price': 0
			})
			return self.commodity

	def __call__(self):
		return self.calculate_tax()

# class TaxPriceDependent(Commodity):
# 	''' 
# 	This is to handle if Commodity Tax is dependant on price
# 	'''
# 	def __init__(self, commodity):
# 		super().__init__(commodity)

# 	def get_tax_perc(self):
		
# 		price_wise_category = tax_lookup.get(self.category, {})

# 		for each in price_wise_category:
# 			if self.price > each:
# 				self.tax_perc = price_wise_category.get('price_above', 0)
# 			elif self.price < each:
# 				self.tax_perc = price_wise_category.get('price_below', 0)

# 	def __call__(self):
# 		self.get_tax_perc()