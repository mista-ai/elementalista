class Nutrient:
    CONVERSION_FACTORS = {
        'mcg': {'g': 1000000, 'mg': 1000, 'mcg': 1},
        'g': {'mcg': 0.000001, 'mg': 0.001, 'g': 1},
        'mg': {'mcg': 0.001, 'g': 1000, 'mg': 1}
    }

    def __init__(self, name: str, unit: str, lower: float, higher: float, max_daily_dose, ui=1):
        """
        Инициализация объекта микроэлемента.

        Args:
            name (str): Имя микроэлемента, например 'Vitamin_A'
            unit (str): Единицы измерения, например 'mg'
        """
        self.name = name
        self.unit = unit
        self.ui = ui
        self.lower = lower
        self.higher = higher
        self.max_daily_dose = max_daily_dose

    def convert_unit(self, new_unit: str):
        if new_unit in self.CONVERSION_FACTORS:
            if self.unit == 'ui':
                return self.ui * self.CONVERSION_FACTORS[new_unit]['mcg']
            else:
                return self.CONVERSION_FACTORS[new_unit][self.unit]
        else:
            raise Exception('error')


class NutrientList:
    def __init__(self, nutrients):
        self.nutrients = dict()
        for nutrient in nutrients:
            self.nutrients[nutrient.name] = nutrient

    def add_nutrient(self, nutrient: Nutrient):
        self.nutrients[nutrient.name] = nutrient

    def remove_nutrient(self, nutrient_name: str):
        if nutrient_name in self.nutrients:
            del self.nutrients[nutrient_name]
        else:
            raise Exception('Nutrient not found')

    def get_nutrient(self, nutrient_name: str) -> Nutrient:
        return self.nutrients.get(nutrient_name, None)

    def update_nutrient(self, nutrient: Nutrient):
        if nutrient.name in self.nutrients:
            self.nutrients[nutrient.name] = nutrient
        else:
            raise Exception('Nutrient not found')

    def list_all_nutrients(self) -> list:
        return list(self.nutrients.keys())


class Product:
    def __init__(self, name: str, nutrient_content: dict):
        """
        Args:
            name (str): Имя продукта, например 'Apple'
            nutrient_content (dict): Словарь с содержанием микроэлементов.
                                     Ключи - имена микроэлементов, значения - их количество.
        """
        self.name = name
        self.nutrient_content = nutrient_content  # {'Vitamin_A': {'amount': 50, 'unit': 'mcg'}, ...}

    def get_nutrient_amount(self, nutrient_name: str) -> dict:
        """
        Получает количество и единицы измерения микроэлемента в продукте.

        Args:
            nutrient_name (str): Имя микроэлемента, например 'Vitamin_A'

        Returns:
            dict: Словарь с 'amount' и 'unit', или None если микроэлемент отсутствует
        """
        return self.nutrient_content.get(nutrient_name, None)

    def update_nutrient_amount(self, nutrient_name: str, amount: float, unit: str):
        """
        Обновляет содержание микроэлемента в продукте.

        Args:
            nutrient_name (str): Имя микроэлемента
            amount (float): Количество
            unit (str): Единицы измерения
        """
        self.nutrient_content[nutrient_name] = {'amount': amount, 'unit': unit}

    def list_all_nutrients(self) -> list:
        """
        Возвращает список всех микроэлементов в продукте.

        Returns:
            list: Список имен микроэлементов
        """
        return list(self.nutrient_content.keys())


class UserProfile:
    def __init__(self, username: str, current_levels: dict):
        self.username = username
        self.current_levels = current_levels  # {'Vitamin_A': {'amount': 50, 'unit': 'mcg'}, ...}

    def update_level(self, nutrient_name: str, amount: float, unit: str):
        self.current_levels[nutrient_name] = {'amount': amount, 'unit': unit}


class Supplement:
    def __init__(self, name: str, nutrient_content: dict):
        self.name = name
        self.nutrient_content = nutrient_content  # {'Vitamin_A': {'amount': 50, 'unit': 'mcg'}, ...}


class NutrientAnalyzer:
    def __init__(self, user_profile: UserProfile, nutrient_list: NutrientList):
        self.user_profile = user_profile
        self.nutrient_list = nutrient_list

    def calculate_deficiency(self) -> dict:
        deficiencies = {}

        for nutrient in self.nutrient_list.nutrients.values():
            nutrient_name = nutrient.name

            if nutrient_name in self.user_profile.current_levels:
                current_amount = self.user_profile.current_levels[nutrient_name]['amount']
                current_unit = self.user_profile.current_levels[nutrient_name]['unit']

                # Конвертируем текущий уровень к единицам измерения нормы
                if current_unit != nutrient.unit:
                    conversion_factor = nutrient.convert_unit(current_unit)
                    current_amount *= conversion_factor

                # Проверяем на дефицит
                if current_amount < nutrient.lower:
                    deficiencies[nutrient_name] = {
                        'amount': nutrient.lower - current_amount,
                        'unit': nutrient.unit
                    }

        return deficiencies

    def recommend_supplements(self, deficiencies: dict, supplement: Supplement) -> dict:
        recommendations = {}

        for nutrient_name, deficiency in deficiencies.items():
            if nutrient_name in supplement.nutrient_content:  # Изменение здесь
                nutrient = self.nutrient_list.get_nutrient(nutrient_name)
                supplement_amount = supplement.nutrient_content[nutrient_name]['amount']  # И изменение здесь
                supplement_unit = supplement.nutrient_content[nutrient_name]['unit']  # И здесь

                # Конвертация единиц измерения
                if supplement_unit != deficiency['unit']:
                    conversion_factor = Nutrient.CONVERSION_FACTORS[supplement_unit][deficiency['unit']]
                    supplement_amount *= conversion_factor

                # Расчет необходимого количества добавки
                required_amount = deficiency['amount'] / supplement_amount

                # Определяем максимально допустимую дозу и количество дней
                daily_dose = min(required_amount, nutrient.max_daily_dose)
                days_needed = required_amount / daily_dose

                recommendations[nutrient_name] = {
                    'supplement_name': supplement.name,
                    'daily_dose': daily_dose,
                    'days_needed': days_needed,
                    'unit': deficiency['unit']
                }
            return recommendations


nutrient_a = Nutrient("Vitamin_A", "mcg", 300, 900, 700)
nutrient_d = Nutrient("Vitamin_D", "mcg", 10, 20, 25)

nutrient_list = NutrientList([nutrient_a, nutrient_d])

trout_nutrients = {
    'Vitamin_A': {'amount': 50, 'unit': 'mcg'},
    'Vitamin_D': {'amount': 5, 'unit': 'mcg'},
}

trout = Product("Trout", trout_nutrients)

user_levels = {
    'Vitamin_A': {'amount': 100, 'unit': 'mcg'},
    'Vitamin_D': {'amount': 8, 'unit': 'mcg'},
}

user_profile = UserProfile("JohnDoe", user_levels)

supplement_data = {
    'Vitamin_A': {'amount': 200, 'unit': 'mcg'},
    'Vitamin_D': {'amount': 10, 'unit': 'mcg'},
}

supplement = Supplement("MultiVitamin", supplement_data)

analyzer = NutrientAnalyzer(user_profile, nutrient_list)

# Расчеты и вывод
deficiencies = analyzer.calculate_deficiency()
print("Deficiencies:", deficiencies)

recommendations = analyzer.recommend_supplements(deficiencies, supplement)
print("Recommendations:", recommendations)
