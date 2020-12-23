class Allergen:

    def __init__(self, name):
        self.name = name
        self.confirmed = 0

    def print(self, end='\n'):
        print(self.__str__(), end=end)

    def set_confirmed(self, val):
        self.confirmed = val

    def __str__(self):
        return "{}({})".format(self.name, self.confirmed)


class Ingredient:

    def __init__(self, name):
        self.name = name
        self.food = []
        self.confirmed_allergen = 0

    def print(self, end='\n'):
        print(self.__str__(), end=end)

    def add_food(self, name):
        self.food.append(name) if name not in self.food else self.food

    def set_confirmed(self, val):
        self.confirmed_allergen = val

    def __str__(self):
        return "{}({})[{}]".format(self.name, self.confirmed_allergen, "| ".join([str(f.allergens) for f in self.food]))


class Food:

    def __init__(self, ingredients, allergens):
        self.ingredients = ingredients
        self.allergens = allergens

    def print(self):
        print("ingredients:", end='')
        for i in self.ingredients:
            print(i, end=' ')
        print(", allergens:", end='')
        for a in self.allergens:
            print(a, end=' ')
        print()

    def __str__(self):
        return ", ".join(self.ingredients) + ":" + ", ".join(self.allergens)


def find_allergen(allergens, allergen):
    for a in allergens:
        if a.name == allergen:
            return a
    return None


def find_allergens(menu):
    allergens = []
    for f in menu:
        for a in f.allergens:
            s_allergen = find_allergen(allergens, a)
            if not s_allergen:
                allergens.append(Allergen(a))
    return allergens


def find_ingredient(ingredients, ingredient):
    for i in ingredients:
        if i.name == ingredient:
            return i
    return None


def find_ingredients(menu):
    ingredients = []
    for f in menu:
        for i in f.ingredients:
            if not find_ingredient(ingredients, i):
                ingredients.append(Ingredient(i))
    return ingredients


def confirmed_allergens(allergens):
    result = []
    for a in allergens:
        if a.confirmed == 1:
            result.append(a)
    return result


def difference(list1, list2):
    result = []
    for l1 in list1:
        if not l1 in list2:
            result.append(l1)
    return result


def find_confirmed_allergenes(ingredients, allergens):
    res_allergens = []
    res_ingredients = []

    for i in ingredients:
        for a in allergens:
            cnt_allergens = 0
            for f in i.food:
                if a.name in f.allergens:
                    cnt_allergens += 1
            if cnt_allergens >= 2:
                a.set_confirmed(1)
                if not find_allergen(res_allergens, a.name):
                    res_allergens.append(a)
                i.set_confirmed(1)
                if not find_ingredient(res_ingredients, i.name):
                    res_ingredients.append(i)

    return (res_ingredients, res_allergens)


def find_solo_allergens(menu, conf_ingr, conf_allerg, ingredients):
    res_allergens = []
    res_ingredients = []

    for f in menu:
        inv_ingr = difference(f.ingredients, [i.name for i in conf_ingr])
        inv_allerg = difference(f.allergens, [a.name for a in conf_allerg])
        if len(inv_ingr) == len(inv_allerg):
            for i in inv_ingr:
                ingr = find_ingredient(ingredients, i)
                ingr.set_confirmed(1)
                res_ingredients.append(ingr)
            for a in inv_allerg:
                allerg = Allergen(a)
                allerg.set_confirmed(1)
                res_allergens.append(allerg)
    return (res_ingredients, res_allergens)


if __name__ == '__main__':
    menu = []
    with open("input_test.txt", "r") as inFile:
        for line in inFile:
            tmp1 = line.split(" (")
            ingredients = tmp1[0].split(" ")
            allergens = tmp1[1].rstrip('\n').rstrip(')')[len('contains '):].split(", ")
            menu.append(Food(ingredients, allergens))

    allergens = find_allergens(menu)
    ingredients = find_ingredients(menu)

    # add the food to ingredients
    for m in menu:
        for i in ingredients:
            if i.name in m.ingredients:
                i.add_food(m)
#    for i in ingredients:
#        i.print()

    (confirmed_ingredients, confirmed_allergens) = find_confirmed_allergenes(ingredients, allergens)
    (solo_ingredients, solo_allergens) = find_solo_allergens(menu, confirmed_ingredients, confirmed_allergens, ingredients)
    confirmed_ingredients += solo_ingredients
    confirmed_allergens += solo_allergens

    for a in confirmed_allergens:
        a.print()

    ingredients_names = [i.name for i in ingredients]
    confirmed_ingredients_names = [i.name for i in confirmed_ingredients]
    non_allergent_ingredients = difference(ingredients_names, confirmed_ingredients_names)

    for i in confirmed_ingredients:
        i.print()

    result = 0
    for i in non_allergent_ingredients:
        for f in menu:
            if i in f.ingredients:
                result += 1
    print(result)