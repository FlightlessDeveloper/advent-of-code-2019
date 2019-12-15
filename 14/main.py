import argparse
from math import ceil
from collections import namedtuple, defaultdict


Recipe = namedtuple("Recipe", "chemical_produced chemicals_needed")
Chemical = namedtuple("Chemical", "name quantity")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("--debug", action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    reactions_list = [parse_line(line.strip()) for line in open(args.input_file) if len(line.strip()) > 0]
    reactions_dict = dict((recipe.chemical_produced.name, recipe) for recipe in reactions_list)

    # Part 1
    resource_steps = [x for x in get_ore_for_recipe(reactions_dict['FUEL'], reactions_dict)]
    if args.debug:
        for step in resource_steps:
            print(resources_to_string(step))
    print(f"Final ORE needed: {resource_steps[-1]['ORE']}")


def get_ore_for_recipe(recipe, reactions):
    resource_spend = defaultdict(lambda: 0, [recipe.chemical_produced])
    yield resource_spend
    while not all((chemical_name not in reactions or resource_spend[chemical_name] <= 0) for chemical_name in resource_spend):
        resource_spend = sum_resources([calculate_resources(reactions[chemical_name], resource_spend[chemical_name])
                                        if chemical_name in reactions
                                        else defaultdict(lambda: 0, [(chemical_name, resource_spend[chemical_name])])
                                        for chemical_name in resource_spend])
        yield resource_spend


def calculate_resources(recipe, target_quantity):
    if target_quantity <= 0:
        return defaultdict(lambda: 0, [Chemical(recipe.chemical_produced.name, target_quantity)])
    multiplicand = ceil(target_quantity / recipe.chemical_produced.quantity)
    result_resources = Chemical(recipe.chemical_produced.name,
                                target_quantity - multiplicand * recipe.chemical_produced.quantity)
    result_materials = [Chemical(chemical.name, multiplicand * chemical.quantity)
                        for chemical in recipe.chemicals_needed]
    result_materials.append(result_resources)
    return defaultdict(lambda: 0, result_materials)


def sum_resources(resource_dicts):
    combined_resources = defaultdict(lambda: 0)
    for k in set().union(*[d.keys() for d in resource_dicts]):
        combined_resources[k] = sum(d[k] for d in resource_dicts)
    return combined_resources


def parse_line(line):
    input_strings, output_string = line.split(" => ")
    output_chemical = parse_chemical(output_string)
    return Recipe(output_chemical, [parse_chemical(s) for s in input_strings.split(", ")])


def parse_chemical(s):
    quantity_string, name = s.split(" ")
    return Chemical(name, int(quantity_string))


def resources_to_string(resources):
    sorted_pairs = [x for x in sorted([(i, resources[i]) for i in resources], key=lambda p: p[0])]
    return "[" + ", ".join(f"({name}: {qty})" for (name, qty) in sorted_pairs) + "]"


if __name__ == "__main__":
    main()
