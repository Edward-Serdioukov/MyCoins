from flet import (
    Page,
    View,
    Container,
    Text,
    Column,
    Row,
    colors,
    Card,
    Image,
    GridView,
    AppBar,
    Icon,
    IconButton,
    PopupMenuItem,
    PopupMenuButton,
    Text, TextSpan, TextStyle, TextDecoration,
)
import flet

class Coins():

    def __init__(self, page, url, code, title, src):
        self.page = page    
        self.link = url
        self.code = code
        self.title = title
        self.src = src
        # Список картинок и надписей
        self.coins = [
        {
            "src": "images/coins/austria-50-schilling-1964.jpg ",
            "title": "50 Schilling 1964",
            "code": "1964w",
        },
        {
            "src": "images/coins/austria-50-schilling-1964-2.jpg ",
            "title": "50 Schilling 1964",
            "code": "1964w",
        },

        ]
        self.appbar = AppBar(
                leading=Icon(flet.icons.MONEY_ROUNDED),
                leading_width=40,
                title=Text(self.title),
                center_title=False,
                bgcolor=colors.SURFACE_VARIANT,
            )
        # Создание галереи картинок
        self.gallery =  GridView(
            expand=1,
            runs_count=5,
            max_extent=200,
            child_aspect_ratio=1.0,
            spacing=15,
            run_spacing=5,
            controls=[
                Card(
                    width=400,
                    height=600,
                    color= colors.WHITE,
                    elevation=1,  # Уровень тени

                    content= Container( Column([
                            Image(src=img["src"], width=100, height=100),
                            Text(img["title"]),
                    ], 
                    horizontal_alignment="center",
                    alignment="center"),
                    #padding=10,
                    #on_click=lambda e, img=img: self.on_image_click(e, img["src"], img["title"])
                    ),
                ) for img in self.coins
            ]
        )


 
    def view(self):
    
        Text(
            spans=[TextSpan(
                "Instruction",
                TextStyle(decoration=TextDecoration.UNDERLINE), 
                url=self.link.value)],
        )
    
        return View(
            route="/coins",
            scroll=flet.ScrollMode.AUTO,
            controls=[
                self.appbar,
                self.gallery,
            ]
        )






