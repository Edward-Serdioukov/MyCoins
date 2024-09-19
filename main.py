import logging

import flet
from flet import Page

from views.olympics import Olympics



#logging.basicConfig(level=logging.DEBUG)



def main(page: Page):

    olympics = Olympics(page)
    olympics_view = olympics.view()
    olympics_map = olympics.olympics_map_view()
    countries_map = olympics.countries_map_view()

    def route_change(route):
        page.views.clear()
        if page.route == "/olympics":
            page.views.append(olympics_view)
        if page.route == "/details":
            page.views.append(olympics_view)
            page.views.append(olympics.details_view())
        if page.route == "/information":
            page.views.append(olympics.information_view())
        if page.route == "/olympics_map":
            page.views.append(olympics_map)
        if page.route == "/details_olympic_map":
            page.views.append(olympics_map)
            page.views.append(olympics.details_view())
        if page.route == "/countries_map":
            page.views.append(countries_map)
        if page.route == "/details_country_map":
            page.views.append(countries_map)
            page.views.append(olympics.details_view())

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    

    def show_image_modal(e):
        def close_dlg(e):
            dlg_modal.open = False
            page.update()

        # Создание виджета изображения для модального окна
        image = flet.Image(src='icons/logo1.png', width=200, height=200) 
        
        # Создание модального окна с изображением
        dlg_modal = flet.AlertDialog(
            modal=True,
            title=flet.Text("About"),
            content=flet.Column([image,flet.ListTile(title=flet.Text(
                "My coins collection"), subtitle=
                flet.Text(
                    spans=[ flet.TextSpan(
                    "eduard.serdiukov@gmail.com", 
                    flet.TextStyle(decoration=flet.TextDecoration.UNDERLINE),
                    url="mailto:eduard.serdiukov@gmail.com", ),],size=10,),
                #f"Key: {e.key}, Shift: {e.shift}, Control: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}"
            )],alignment=flet.MainAxisAlignment.CENTER,horizontal_alignment=flet.CrossAxisAlignment.CENTER,height=300,),
            actions=[flet.TextButton("Close", on_click=lambda e: close_dlg(e))],
            actions_alignment=flet.MainAxisAlignment.END,
        )            
        # Отображение модального окна
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def on_keyboard(e: flet.KeyboardEvent):
        if e.key.upper() == 'A':
            show_image_modal(e)
 

    page.on_keyboard_event = on_keyboard
    olympics.grid_olympics()  

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/olympics")
#flet.app(target=main, assets_dir="assets", view="web_browser", upload_dir="assets/images", web_renderer = flet.WebRenderer.HTML, port=55432)
#
#flet.app(target=main, assets_dir="assets")
flet.app(main) ###flet run --web main.py

