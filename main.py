import logging

import flet
from flet import Page

from views.olympics import Olympics


#logging.basicConfig(level=logging.DEBUG)


def main(page: Page):

    olympics = Olympics(page)
    olympics_view = olympics.view()

    def route_change(route):
        page.views.clear()
        if page.route == "/olympics":
            page.views.append(olympics_view)
        if page.route == "/details":
            page.views.append(olympics_view)
            page.views.append(olympics.details_view())

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    olympics.grid_olympics()  

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/olympics")

#flet.app(target=main, assets_dir="assets", view=WEB_BROWSER, upload_dir="assets\images", port=55432)
#
flet.app(target=main, assets_dir="assets", view=flet.WEB_BROWSER)

