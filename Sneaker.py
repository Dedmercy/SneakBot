class Sneaker:

    def __init__(self):
        # self.id = ''
        self.link = ''
        self.drop_date = ''
        self.image = ''
        self.name = ''
        self.price_usd = 0
        self.price_rub = 0
        self.size = ''
        self.color = ''
        self.style_code = ''
        self.regions = ''

    def show_info(self):
        print(f'image: {self.image}, name: {self.name} '
              f'price $: {self.price_usd} price rub: {self.price_rub}'
              f'size: {self.size} color: {self.color}'
              f'style code: {self.style_code} regions:{self.regions}'
              f'link {self.link} drop date {self.drop_date}')

