import collections

class Allergen:

    def __init__(self, name):
        self.name = name
        self.confirmed = 0
        self.usage = 1

    def print(self, end='\n'):
        print(self.__str__(), end=end)

    def set_confirmed(self, val):
        self.confirmed = val

    def increment(self):
        self.usage += 1

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

    def remove_ingredient(self, name):
        if name in self.ingredients:
            self.ingredients.remove(name)

    def remove_allergene(self, name):
        if name in self.allergens:
            self.allergens.remove(name)

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

def find_possible_allergens(ingredient):
    allergens = []

    for f in ingredient.food:
        for a in f.allergens:
            s_allergen = find_allergen(allergens, a)
            if not s_allergen:
                allergens.append(Allergen(a))
            else:
                s_allergen.increment()
    return allergens


def find_decrement_allergen_usage(ingredient, name):
    allergens = []

    for f in ingredient.food:
        for a in f.allergens:
            s_allergen = find_allergen(allergens, a)
            if not s_allergen:
                allergens.append(Allergen(a))
            else:
                s_allergen.increment()
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


def find_food_for_allergene(menu, allergen):
    result = []
    for f in menu:
        if allergen.name in f.allergens:
            result.append(f)
    return result


def union(list1, list2):
    result = list2
    for l1 in list1:
        if not l1 in list2:
            result.append(l1)
    return result


def intersection(list1, list2):
    result = []
    for l1 in list1:
        for l2 in list2:
            if l1 == l2:
                result.append(l1)
    return result


def find_common_ingredient(menu):
    result = []
    for idx1 in range(len(menu)):
        for idx2 in range(idx1+1, len(menu)):
            result = union(result, intersection(menu[idx1].ingredients, menu[idx2].ingredients))
    return result


def find_highest_usage_allergen(ingredients):
    highest = 0
    highest_ingr_list = []
    highest_alle_list = []

    for i in ingredients:
        for a in find_possible_allergens(i):
            if a.usage == highest:
                highest_ingr_list.append(i)
                highest_alle_list.append(a)
            if a.usage > highest:
                highest = a.usage
                highest_ingr_list = [i]
                highest_alle_list = [a]

    return (highest, highest_ingr_list, highest_alle_list)


def find_usage_allergen(ingredients, nbr):
    highest = 0
    highest_ingr_list = []
    highest_alle_list = []

    for i in ingredients:
        for a in find_possible_allergens(i):
            if a.usage == nbr:
                highest_ingr_list.append(i)
                highest_alle_list.append(a)

    return (nbr, highest_ingr_list, highest_alle_list)


def remove_ingredientfrom_list(ingredients, name):
    for idx in range(len(ingredients)):
        if ingredients[idx].name == name:
            del ingredients[idx]
            break


def find_ingredient_in_food(menu, ingredient):
    result = 0
    for m in menu:
        if ingredient in m.ingredients:
            result += 1
    return result


def duplicate_allergens(high_alle):
    for idx1 in range(len(high_alle)):
        for idx2 in range(idx1, len(high_alle)):
            if high_alle[idx1] == high_alle[idx2]:
                return True
    return False


if __name__ == '__main__':
    menu = []
    with open("input.txt", "r") as inFile:
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

    print(len(allergens))
    print(len(ingredients))

    # for a in allergens:
    #     print(a)
    for i in ingredients:
        print(i.name, end=': ')
        for a in find_possible_allergens(i):
            print("{}({})".format(a.name, a.usage), end=', ')
        print()

    dangerous_list = {}

    (highest_usage, high_ingr, high_alle) = find_highest_usage_allergen(ingredients)
    print(highest_usage)
    for idx in range(len(high_ingr)):
        print(high_ingr[idx].name, end=', ')
        print(high_alle[idx].name)
        print("--> Remove {}:{}".format(high_ingr[idx].name, high_alle[idx].name))
        dangerous_list[high_alle[idx].name] = high_ingr[idx].name
        for f in menu:
            f.remove_ingredient(high_ingr[idx].name)
            f.remove_allergene(high_alle[idx].name)
        remove_ingredientfrom_list(ingredients, high_ingr[idx].name)

    (highest_usage, high_ingr, high_alle) = find_highest_usage_allergen(ingredients)
    print(highest_usage)
    for idx in range(len(high_ingr)):
        print(high_ingr[idx].name, end=', ')
        print(high_alle[idx].name)

    (highest_usage, high_ingr, high_alle) = find_usage_allergen(ingredients, highest_usage - 1)
    print(highest_usage)
    for idx in range(len(high_ingr)):
        print(high_ingr[idx].name, end=', ')
        print(high_alle[idx].name)
    print("--> Remove {}:{}".format(high_ingr[4].name, high_alle[4].name))
    dangerous_list[high_alle[4].name] = high_ingr[4].name
    for f in menu:
        f.remove_ingredient(high_ingr[4].name)
        f.remove_allergene(high_alle[4].name)
    remove_ingredientfrom_list(ingredients, high_ingr[4].name)

    (highest_usage, high_ingr, high_alle) = find_highest_usage_allergen(ingredients)
    print(highest_usage)
    for idx in range(len(high_ingr)):
        print(high_ingr[idx].name, end=', ')
        print(high_alle[idx].name)
    print("--> Remove {}:{}".format(high_ingr[0].name, high_alle[0].name))
    dangerous_list[high_alle[0].name] = high_ingr[0].name
    for f in menu:
        f.remove_ingredient(high_ingr[0].name)
        f.remove_allergene(high_alle[0].name)
    remove_ingredientfrom_list(ingredients, high_ingr[0].name)

    (highest_usage, high_ingr, high_alle) = find_highest_usage_allergen(ingredients)
    print(highest_usage)
    for idx in range(len(high_ingr)):
        print(high_ingr[idx].name, end=', ')
        print(high_alle[idx].name)
    print("--> Remove {}:{}".format(high_ingr[0].name, high_alle[0].name))
    dangerous_list[high_alle[0].name] = high_ingr[0].name
    for f in menu:
        f.remove_ingredient(high_ingr[0].name)
        f.remove_allergene(high_alle[0].name)
    remove_ingredientfrom_list(ingredients, high_ingr[0].name)

    (highest_usage, high_ingr, high_alle) = find_highest_usage_allergen(ingredients)
    print(highest_usage)
    for idx in range(len(high_ingr)):
        print(high_ingr[idx].name, end=', ')
        print(high_alle[idx].name)

    (highest_usage, high_ingr, high_alle) = find_usage_allergen(ingredients, highest_usage - 1)
    print(highest_usage)
    for idx in range(len(high_ingr)):
        print(high_ingr[idx].name, end=', ')
        print(high_alle[idx].name)
    print("--> Remove {}:{}".format(high_ingr[5].name, high_alle[5].name))
    dangerous_list[high_alle[5].name] = high_ingr[5].name
    for f in menu:
        f.remove_ingredient(high_ingr[5].name)
        f.remove_allergene(high_alle[5].name)
    remove_ingredientfrom_list(ingredients, high_ingr[5].name)

    (highest_usage, high_ingr, high_alle) = find_highest_usage_allergen(ingredients)
    print(highest_usage)
    for idx in range(len(high_ingr)):
        print(high_ingr[idx].name, end=', ')
        print(high_alle[idx].name)

    (highest_usage, high_ingr, high_alle) = find_usage_allergen(ingredients, highest_usage - 1)
    print(highest_usage)
    for idx in range(len(high_ingr)):
        print(high_ingr[idx].name, end=', ')
        print(high_alle[idx].name)
    print("--> Remove {}:{}".format(high_ingr[3].name, high_alle[3].name))
    dangerous_list[high_alle[3].name] = high_ingr[3].name
    for f in menu:
        f.remove_ingredient(high_ingr[3].name)
        f.remove_allergene(high_alle[3].name)
    remove_ingredientfrom_list(ingredients, high_ingr[3].name)

    (highest_usage, high_ingr, high_alle) = find_highest_usage_allergen(ingredients)
    print(highest_usage)
    for idx in range(len(high_ingr)):
        print(high_ingr[idx].name, end=', ')
        print(high_alle[idx].name)
    print("--> Remove {}:{}".format(high_ingr[0].name, high_alle[0].name))
    dangerous_list[high_alle[0].name] = high_ingr[0].name
    for f in menu:
        f.remove_ingredient(high_ingr[0].name)
        f.remove_allergene(high_alle[0].name)
    remove_ingredientfrom_list(ingredients, high_ingr[0].name)

    (highest_usage, high_ingr, high_alle) = find_highest_usage_allergen(ingredients)
    print(highest_usage)
    for idx in range(len(high_ingr)):
        print(high_ingr[idx].name, end=', ')
        print(high_alle[idx].name)
    print("--> Remove {}:{}".format(high_ingr[0].name, high_alle[0].name))
    dangerous_list[high_alle[0].name] = high_ingr[0].name
    for f in menu:
        f.remove_ingredient(high_ingr[0].name)
        f.remove_allergene(high_alle[0].name)
    remove_ingredientfrom_list(ingredients, high_ingr[0].name)

    (highest_usage, high_ingr, high_alle) = find_highest_usage_allergen(ingredients)
    print(highest_usage)
    for idx in range(len(high_ingr)):
        print(high_ingr[idx].name, end=', ')
        print(high_alle[idx].name)

    print(len(ingredients))
    result = 0
    for i in ingredients:
        result += find_ingredient_in_food(menu, i.name)
    print(result)

    ordered_dangerous_list = collections.OrderedDict(sorted(dangerous_list.items()))

    dangerous_ingredients = []
    for allergen in ordered_dangerous_list.keys():
        print(allergen)
        dangerous_ingredients.append(dangerous_list[allergen])
    print(",".join(dangerous_ingredients))
# 2329 -> too low



    # list_food = find_food_for_allergene(menu, allergens[3])
    # allergens[3].print()
    # for f in list_food:
    #     f.print()
    # common_ingr = find_common_ingredient(list_food)
    # for ingr in common_ingr:
    #     for f in menu:
    #         f.remove_ingredient(ingr)
    #         f.remove_allergene(allergens[0].name)
    # for f in list_food:
    #     f.print()
    # print(common_ingr)

    # list_food = find_food_for_allergene(menu, allergens[2])
    # allergens[2].print()
    # common_ingr = find_common_ingredient(list_food)
    # print(common_ingr)
    # for f in list_food:
    #     f.print()

#    for i in ingredients:
#        i.print()
#
#     (confirmed_ingredients, confirmed_allergens) = find_confirmed_allergenes(ingredients, allergens)
#     (solo_ingredients, solo_allergens) = find_solo_allergens(menu, confirmed_ingredients, confirmed_allergens, ingredients)
#     confirmed_ingredients += solo_ingredients
#     confirmed_allergens += solo_allergens
#
#     for a in confirmed_allergens:
#         a.print()
#
#     ingredients_names = [i.name for i in ingredients]
#     confirmed_ingredients_names = [i.name for i in confirmed_ingredients]
#     non_allergent_ingredients = difference(ingredients_names, confirmed_ingredients_names)
#
#     for i in confirmed_ingredients:
#         i.print()
#
#     result = 0
#     for i in non_allergent_ingredients:
#         for f in menu:
#             if i in f.ingredients:
#                 result += 1
#    print(result)