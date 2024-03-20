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
		if type(eval(new_parts[0])) == tuple:
			num = 0
			tup = eval(new_parts[0])
			for j in range(len(tup)):
					num += tup[j]/(10 ** j)
			amounts.append(num)
		else:
			amounts.append(eval(new_parts[0]))
		measures.append(' '.join(new_parts[1:]))
	recipe = pd.DataFrame({'entities': grocceries, 'amounts': amounts, 'measures': measures})
	return recipe

the_list = pd.DataFrame() 

def main(page):
	page.bgcolor = "#ffddd2e5"
	page.update()
	page.title = "My shopping list app"
	page.update()
	page.padding = 100
	page.update()
	page.scroll = "always"
	page.update()
	page.theme = ft.Theme(color_scheme_seed="pink")
	page.update()


	def btn_click(e):
		global the_list
		if not txt_name.value:
			txt_name.error_text = "Please enter the ingridients list"
			page.update()
		else:
			ingridients = process_ingredients_to_pandas(txt_name.value)
			the_list = pd.concat([the_list, ingridients], ignore_index=True)
			page.clean()
			dict_ingridients = the_list.groupby('entities', as_index=False).agg({'amounts': 'sum', 'measures' : 'first'}).to_dict(orient='split', index=False)
			page.add(
		ft.DataTable(
			columns=[
				ft.DataColumn(ft.Text(f"{item}")) for item in dict_ingridients['columns']
			],
			rows=[
				ft.DataRow(
					cells=[
						ft.DataCell(ft.Text(f"{item}")) for item in dict_ingridients['data'][i]
					],
				) for i in range(len(dict_ingridients['data']))
			],  bgcolor = '#fadce6', horizontal_lines=ft.border.BorderSide(1)
	),)
			page.scroll = "always"
			page.update()
			
	
	def add_click(e):
		global the_list
		if not txt_name.value:
			txt_name.error_text = "Please enter the ingridients list"   
			page.update()
		else:
			the_list = pd.concat([the_list, process_ingredients_to_pandas(txt_name.value)], ignore_index=True)
			txt_name.value = ""
			page.update()

	txt_name = ft.TextField(label="Ingridients:", multiline=True)

	page.add(txt_name, ft.ElevatedButton("Display", on_click=btn_click), ft.ElevatedButton("Add", on_click=add_click))

	images = ft.Row(wrap=2)
	page.add(images)


	srcs = ["https://www.fabmood.com/wp-content/uploads/2023/07/food-snapchat-3.jpg", "https://images.unsplash.com/photo-1565506130372-ee45c65c4f29?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8YWVzdGhldGljJTIwZm9vZHxlbnwwfHwwfHx8MA%3D%3D", "https://worthybornedit.com/wp-content/uploads/2022/11/IMG_5652-821x1024.jpg", "https://img.freepik.com/free-photo/food-celebrating-world-tapas-day_23-2149361451.jpg?size=626&ext=jpg&ga=GA1.1.87170709.1707523200&semt=ais", "https://worthybornedit.com/wp-content/uploads/2022/11/IMG_5625-825x1024.jpg"]

	for source in srcs:
		images.controls.append(
            ft.Image(
                src=f"{source}",
                width=200,
                height=200,
                fit=ft.ImageFit.CONTAIN
            )
        )
			
	page.update()


ft.app(target=main)
