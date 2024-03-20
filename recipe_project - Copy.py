import flet as ft
import pandas as pd

def process_ingredients_to_pandas(ingredients):
    processed = []
    for char in ingredients:
        if char.isupper():
            processed.append("\n" + char)
        else:
            processed.append(char)
    lines = ''.join(processed).split('\n')
    lines = [line for line in lines if line != '' and '-' in line] 
    for i in range(len(lines)):
        if '(' in lines[i]:
                for k in range(len(lines[i]) - 1):
                    if k < len(lines[i]):
                        if lines[i][k] == '(':
                            for y in range(k, len(lines[i])):
                                if lines[i][y] == ')':
                                    lines[i] = lines[i][:k] + lines[i][y + 1:]
                                    lines[i] = lines[i].strip().strip('\n')
                                    break
        lines[i].strip().strip('\n')
    grocceries = []
    amounts = []
    measures = []
    for line in lines:
        parts = line.split(' - ')
        grocceries.append(parts[0].strip())
        new_parts = parts[1].split()
        amounts.append(eval(new_parts[0]))
        measures.append(' '.join(new_parts[1:]))
    recipe = pd.DataFrame({'entities': grocceries, 'amounts': amounts, 'measures': measures})
    return recipe

def list_ingridients_to_str(ingredients):
    result_str = ''  
    ingredients_dict = ingredients.to_dict()
    for item in ingredients_dict:
        item_str = '' 
        for obj in ingredients_dict[item]:
            item_str += str(obj) + ': ' + str(ingredients_dict[item][obj]) + '\n'
        result_str += item + ': \n' + item_str + '\n'
    return result_str

# def to_pandas(ingridients):
#     grocceries = []
#     amounts = []
#     measures = []
#     for line in ingridients:
#         parts = line.split(' - ')
#         grocceries.append(parts[0].strip())
#         new_parts = parts[1].split()
#         amounts.append(eval(new_parts[0]))
#         measures.append(' '.join(new_parts[1:]))
#     recipe = pd.DataFrame({'entities': grocceries, 'amounts': amounts, 'measures': measures})
#     return recipe

    


def main(page):

    #global the_list = pd.DataFrame()
    the_list2 = pd.DataFrame()

    def btn_click(e):
        if not txt_name.value:
            txt_name.error_text = "Please enter the ingridients list"
            page.update()
        else:
            ingridients = process_ingredients_to_pandas(txt_name.value)
            the_list = pd.concat([the_list2, ingridients], ignore_index=True)
            page.clean()
            str_ingridients = list_ingridients_to_str(the_list)
            page.add(ft.Text(f"{str_ingridients}"))
            
    
    def add_click(e):
        if not txt_name.value:
            txt_name.error_text = "Please enter the ingridients list"   
            page.update()
        else:
            ingridients = process_ingredients_to_pandas(txt_name.value)
            the_list = pd.concat([the_list, ingridients], ignore_index=True)

    txt_name = ft.TextField(label="Ingridients:")

    page.add(txt_name, ft.ElevatedButton("Display", on_click=btn_click))

ft.app(target=main)