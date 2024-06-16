import json
from flet import (
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
    ElevatedButton,
    MainAxisAlignment,
    CrossAxisAlignment,
    ThemeMode,
    ResponsiveRow,
    AlertDialog,
    TextButton,
    FontWeight,
    icons,
    Stack,
    Tabs,
    Tab,
    Markdown,
    MarkdownExtensionSet,
    BarChart,
    BarChartGroup,
    ChartAxis,
    BarChartRod,
    ChartAxisLabel,
    ChartGridLines,
)
import flet

from views.coins import Coins


class Olympics():

    def __init__(self, page):
        self.page = page    
        self.page.theme_mode = ThemeMode.LIGHT
        self.selected_view = '0'
        """
        self.gallery = ResponsiveRow(
            controls=[],
            #run_spacing=5,
            #spacing=5,
            #columns=18,
        )
        """
        self.gallery = GridView(
            runs_count=1,
            max_extent=200,
            child_aspect_ratio=0.7,
            spacing=5,
            run_spacing=5,
            controls=[],         
        )     
        
        self.appbar = AppBar(
                leading=Icon(flet.icons.PALETTE),
                leading_width=40,
                title=Text("Olympic Coins"),
                center_title=False,
                bgcolor=colors.SURFACE_VARIANT,
                actions=[
                    IconButton(icon = flet.icons.WB_SUNNY_OUTLINED, on_click=self.theme_changed),
                    PopupMenuButton(
                    items=[
                        PopupMenuItem(text="View: Olympics",data='0', on_click=self.select_view),
                        PopupMenuItem(text="View: Countries",data='1', on_click=self.select_view),
                        PopupMenuItem(text="View: Coins",data='2', on_click=self.select_view),
                        PopupMenuItem(text="Information",data='5', on_click=self.information_clicked),
                        PopupMenuItem(text="Statistics",data='4', on_click=self.show_stats_modal),
                        PopupMenuItem(text="About",data='3', on_click=self.show_about_modal),
                    ]
                    )
                ],
            )

        # Создание галереи картинок
        #self.gallery2 =  Row(controls=items, wrap=True)

        self.filter = Tabs(
            scrollable=True,
            selected_index=0,

            on_change=self.tabs_changed,
            tabs=[Tab(text="All"), 
                  Tab(tab_content=Icon(icons.SPORTS_SCORE_ROUNDED, color="green", tooltip="Green")),
                  Tab(tab_content=Icon(icons.SPORTS_SCORE_ROUNDED, color="yellow", tooltip="Yellow")),
                  Tab(tab_content=Icon(icons.SPORTS_SCORE_ROUNDED, color="red", tooltip="Red")),
                  Tab(tab_content=Icon(icons.SPORTS_SCORE_ROUNDED, color="grey", tooltip="Silver")),
                  Tab(tab_content=""),#Icon(icons.SIGNAL_CELLULAR_NO_SIM_OUTLINED, color="grey", tooltip="Not Silver")),
                  ],
        )

        self.filter_coins = Tabs(
            scrollable=True,
            selected_index=0,

            on_change=self.tabs_changed,
            tabs=[Tab(text="All"), 
                  Tab(text="Silver"),
                  Tab(text="Euro"),
                  Tab(text="Token"),
                  ],
        )

        self.image_src = ""
        self.image_title = ""
        self.image_url = ""
        self.image_code = ""
        self.image_country = ""
        self.image_games = ""
        self.ctrl = [self.appbar, self.filter, Container(content=self.gallery, alignment=flet.alignment.top_center, padding=10)]

        self.main_view = View(
            route="/olympics",
            scroll=flet.ScrollMode.AUTO,
            controls=self.ctrl
            #js=[Javascript(analytics_script)]
			)
        # Insert Google Analytics script
        analytics_script = """
            <!-- Google tag (gtag.js) -->
            <script async src="https://www.googletagmanager.com/gtag/js?id=G-ED2BNEW5E2"></script>
            <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());

            gtag('config', 'G-ED2BNEW5E2');
            </script>
        """

    def tabs_changed(self, e):
        self.refresher()

    def refresher(self):
        self.gallery.controls.clear()
        self.main_view.controls.clear()
        self.main_view.controls.append(self.appbar)
        if self.selected_view == '0':
            self.grid_olympics()
            self.main_view.controls.append(self.filter)
        elif  self.selected_view == '1':
            self.grid_countries()
        elif  self.selected_view == '2':
            self.grid_coins()            
            self.main_view.controls.append(self.filter_coins)
        self.main_view.controls.append(self.gallery)
        self.page.update() 

    def grid_olympics(self):
        # Список картинок и надписей
        # Путь к вашему JSON файлу
        filename = 'images.json'
        filename2 = 'coins.json'

        # Чтение данных из файла и их загрузка в список словарей
        with open(filename, 'r') as f:
            data = json.load(f)
 
        color = ""
        if self.filter.selected_index == 0:
            self.images = data
        elif self.filter.selected_index == 1:
            color = "green"
        elif self.filter.selected_index == 2:
            color = "yellow"    
        elif self.filter.selected_index == 3:
            color = "red"

              
        # Фильтрация элементов по заданному коду
        if not color == "":
            self.images = [item for item in data if item['color'] == color]
        elif self.filter.selected_index == 4:
            color = "silver"
            with open(filename2, 'r') as f:
                data2 = json.load(f)
            coins = [item['code'] for item in data2 if "Silver".lower() in item['composition'].lower()]
            self.images = [item for item in data if item['code'] in coins]
        elif self.filter.selected_index == 5:
            color = "silver"
            with open(filename2, 'r') as f:
                data2 = json.load(f)
            coins = [item['code'] for item in data2 if "Silver".lower() in item['composition'].lower()]
            self.images = [item for item in data if item['code'] not in coins]
 
            

        items = self.get_cards() 
        self.gallery.controls=items


    def grid_countries(self):
        # Список картинок и надписей
        # Путь к вашему JSON файлу
        filename = 'countries.json'

        # Чтение данных из файла и их загрузка в список словарей
        with open(filename, 'r') as f:
            self.images = json.load(f)
 
        items = self.get_cards_countries() 
        self.gallery.controls = items

    def grid_coins(self):
        # Список картинок и надписей
        # Путь к вашему JSON файлу
        filename = 'coins.json'

        # Чтение данных из файла и их загрузка в список словарей
        with open(filename, 'r') as f:
            data = json.load(f)

        if self.filter_coins.selected_index == 0:
            self.images = data
        elif self.filter_coins.selected_index == 1:
            self.images = [item for item in data if "Silver".lower() in  item['composition'].lower()]
        elif self.filter_coins.selected_index == 2:
            self.images = [item for item in data if "Euro".lower() in  item['title'].lower()]  
        elif self.filter_coins.selected_index == 3:
            self.images = [item for item in data if "Token".lower() in  item['title'].lower()]

        items = self.get_cards_coinsview() 
        self.gallery.controls = items


    def get_cards(self):
        with open('coins.json', 'r') as f:
            coins = json.load(f)
        # Подсчет количества изображений с одинаковым кодом
        code_counts = {img['code']: sum(1 for item in coins if item['code'] == img['code']) for img in self.images}

        # Создание галереи картинок
        return [
            Column(
                #col={"sm": 6, "md": 4, "xl": 1.5},
                controls=[Card(
                elevation=1,  # Уровень тени
                content=Container(
                        content=Column([
                            Image(src=img["src"], width=105, height=105),
                            Row([
                                Text(img["title"], weight=FontWeight.BOLD, size="small"),
                                #Text(f" ({code_counts[img['code']]})", weight=FontWeight.BOLD)
                            ], 
                            spacing=0, alignment="center"),
                            Row([
                                Text(f" ({code_counts[img['code']]})", weight=FontWeight.BOLD, size="small"),
                            ], 
                            spacing=0, alignment="center"),
                            ], 
                            horizontal_alignment="center",
                            #expand=1,
                            alignment="center"
                        ),  

                    padding=10,
                    data=img,
                    on_click=self.on_image_click,
                    width=200,
                    #height=200,
                ),)], #height=100,width=100,
            ) for img in self.images
        ]

    def get_cards_countries(self):

        with open('coins.json', 'r') as f:
            coins = json.load(f)
        # Подсчет количества изображений с одинаковым кодом
        code_counts = {img['country']: sum(1 for item in coins if item['country'] == img['country']) for img in self.images}

        # Создание галереи картинок
        return [
            Column(
                #col={"sm": 6, "md": 4, "xl": 1.5},
                controls=[Card(
                elevation=1,  # Уровень тени
                content=Container(
                    Column([
                        Image(src=img["src"], width=110, height=110),
                        Row([
                            Text(img["title"], weight=FontWeight.BOLD),
                        ], 
                        spacing=1, alignment="center"),
                        Row([
                            Text(f" ({code_counts[img['country']]})", weight=FontWeight.BOLD, size="small"),
                        ], 
                        spacing=0, alignment="center"),
                    ], 
                    horizontal_alignment="center",
                    alignment="center"),
                    padding=10,
                    data=img,
                    on_click=self.on_image_click,
                    width=300,
                ),)]
            ) for img in self.images
        ]


    def get_cards_coinsview(self):
        # Создание галереи картинок
        return  [
            Column(
                #col={"sm": 6, "md": 4, "xl": 1.5},
                controls=[Card(
                    elevation=1,  # Уровень тени
                    content= Container(
                        Column([
                            Image(src=img["src1"], width=115, height=115),
                            Row([Text(img["title"], weight=FontWeight.BOLD),], 
                                spacing=1,alignment="center"),

                    ], 
                    horizontal_alignment="center",
                    alignment="center"),
                    padding=10,
                    data=img,
                    on_click= self.on_image_click,
                    width=300,
                    ),)]
                ) for img in self.images
            ]



    def theme_changed(self, e):
        if self.page.theme_mode == ThemeMode.LIGHT:
            self.page.theme_mode = ThemeMode.DARK
        else:
            self.page.theme_mode = ThemeMode.LIGHT

        self.page.update()

    def select_view(self, e):
        self.selected_view = e.control.data
        self.refresher()
        self.page.go("/olympics")
   

    # Обработчик нажатия на картинку
    def on_image_click(self,e):
        if self.selected_view == '0':
            self.image_games = e.control.data["games"]
        if self.selected_view == '1':
            self.image_country = e.control.data["country"]
        if self.selected_view == '2':
            self.image_src = e.control.data["src1"]
        else:
            self.image_src = e.control.data["src"]
        self.image_title = e.control.data["title"]
        self.image_url = e.control.data["url"]
        self.image_code = e.control.data["code"]
        self.page.go("/details")

    def information_clicked(self, e):
        self.page.go("/information")
  

    def check_item_clicked(self, e):
        e.control.checked = not e.control.checked
        self.page.update()

    def show_stats_modal(self,e):
        def close_dlg(e):
            dlg_modal.open = False
            self.page.update()

        with open('coins.json', 'r') as f:
            data1 = json.load(f)
        coins = len(data1)
        with open('images.json', 'r') as f:
            data2 = json.load(f)
        olympics = len(data2)
        with open('countries.json', 'r') as f:
            data3 = json.load(f)
        contries = len(data3)
        silver_coins = [item['code'] for item in data1 if "Silver".lower() in  item['composition'].lower()]
        olympics_silver = [item for item in data2 if item['code'] in silver_coins]
        tokens = [item['code'] for item in data1 if "Token".lower() in  item['title'].lower()]
        coins = coins - len(tokens)

        # Создание модального окна с изображением
        dlg_modal = flet.AlertDialog(
            modal=True,
            title=flet.Text("Statistics"),
            content=Container(height=300, 
                              content=Column([
                                Row([
                                    self.create_cell_with_border("Coins", 150, 50), 
                                    self.create_cell_with_border(str(coins), 150, 50),
                                ], alignment=flet.MainAxisAlignment.CENTER, spacing=0),
                                Row([
                                    self.create_cell_with_border("Olympics", 150, 50), 
                                    self.create_cell_with_border(str(olympics), 150, 50),
                                ], alignment=flet.MainAxisAlignment.CENTER, spacing=0),
                                Row([
                                    self.create_cell_with_border("Countries", 150, 50), 
                                    self.create_cell_with_border(str(contries), 150, 50),
                                ], alignment=flet.MainAxisAlignment.CENTER, spacing=0),
                                Row([
                                    self.create_cell_with_border("Silver Olympics", 150, 50), 
                                    self.create_cell_with_border(str(len(olympics_silver)), 150, 50),
                                ], alignment=flet.MainAxisAlignment.CENTER, spacing=0),
                                Row([
                                    self.create_cell_with_border("Silver coins", 150, 50), 
                                    self.create_cell_with_border(str(len(silver_coins)), 150, 50),
                                ], alignment=flet.MainAxisAlignment.CENTER, spacing=0),
                                Row([
                                    self.create_cell_with_border("Tokens", 150, 50), 
                                    self.create_cell_with_border(str(len(tokens)), 150, 50),
                                ], alignment=flet.MainAxisAlignment.CENTER, spacing=0),
                            ], spacing=0,),border=flet.border.all(color=flet.colors.BLACK, width=1),padding=0,),
            actions=[flet.TextButton("Close", on_click=lambda e: close_dlg(e))],
            actions_alignment=flet.MainAxisAlignment.END,
        )            
        # Отображение модального окна
        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.page.update() 

    def show_about_modal(self,e):
        def close_dlg(e):
            dlg_modal.open = False
            self.page.update()

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
                    "e-mail: mycoins92@gmail.com", 
                    flet.TextStyle(decoration=flet.TextDecoration.UNDERLINE),
                    url="mailto: mycoins92@gmail.com", ),],size=10,),
            )],alignment=flet.MainAxisAlignment.CENTER,horizontal_alignment=flet.CrossAxisAlignment.CENTER,height=300,),
            actions=[flet.TextButton("Close", on_click=lambda e: close_dlg(e))],
            actions_alignment=flet.MainAxisAlignment.END,
        )            
        # Отображение модального окна
        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.page.update() 

    def view(self):
        return 	self.main_view

    # Функция для создания ячейки таблицы с границей
    def create_cell_with_border(self, text, width=150, height=100):
        return Container(
            expand=True,
            content=Text(text),
            width=width,
            height=height,
            padding=5,
            alignment=flet.alignment.center,
            border=flet.border.all(color=flet.colors.BLACK, width=1),  # Настройка границы для каждой ячейки
        )
    
    def details_view(self):

        def show_image_modal(e):
            def close_dlg(e):
                dlg_modal.open = False
                self.page.update()

            # Создание виджета изображения для модального окна
            image = Image(src=e.control.content.src, width=300, height=300)  # Замените на ваш путь к изображению
            #description = Container( Markdown(coins[0]['description'],selectable=True), width=400, padding=10)
            description = Container( Text(coins[0]['description'], no_wrap=False, size=14), width=400, padding=10)

            # Создание модального окна с изображением
            dlg_modal = AlertDialog(
                modal=True,
                #title=Text("Просмотр изображения"),
                content=Container(Column([image,description],alignment=flet.MainAxisAlignment.START,horizontal_alignment=flet.CrossAxisAlignment.CENTER,scroll=flet.ScrollMode.ALWAYS,),),
                actions=[TextButton("Close", on_click=lambda e: close_dlg(e))],
                actions_alignment=MainAxisAlignment.END,
            )            
            # Отображение модального окна
            self.page.dialog = dlg_modal
            dlg_modal.open = True
            self.page.update()
            
        # Путь к вашему JSON файлу
        filename = 'coins.json'

        # Чтение данных из файла и их загрузка в список словарей
        with open(filename, 'r') as f:
            data = json.load(f)
        
        str_name = ''
        str_value= ''
        #print(f"SEV: - {self.selected_view}")
        if self.selected_view == '0':
            str_name = 'code'
            str_value = self.image_code
        elif self.selected_view == '1':
            str_name = 'country'
            str_value = self.image_country
        elif self.selected_view == '2':
            str_name = 'src1'
            str_value = self.image_src
        
        #print(f"SEV - {str_name}")
        # Фильтрация элементов по заданному коду
        coins = [item for item in data if item[str_name] == str_value]



        appbar = AppBar(
                title=Text(self.image_title),
                center_title=False,
                bgcolor=colors.SURFACE_VARIANT,
            )
        # Создание галереи картинок
        details_gallery =  Row([
                Card(
                    width=300,
                    height=400,
                    color= colors.WHITE,
                    elevation=1,  # Уровень тени

                    content= Container( Column([
                            #Row([Image(src=img["src1"], width=100, height=100),Image(src=img["src2"], width=100, height=100),]),
                            Row([Container(Image(src=img["src1"], width=125, height=125,), on_click=lambda e: show_image_modal(e),),
                                 Container(Image(src=img["src2"], width=125, height=125,), on_click=lambda e: show_image_modal(e),)]),
                            Container(Column([
                                Row([
                                    self.create_cell_with_border("Denomination"), 
                                    self.create_cell_with_border(img['title']),
                                ], alignment=flet.MainAxisAlignment.CENTER, spacing=0),
                                Row([
                                    self.create_cell_with_border("Composition"), 
                                    self.create_cell_with_border(img['composition']),
                                ], alignment=flet.MainAxisAlignment.CENTER, spacing=0),
                            ], spacing=0),border=flet.border.all(color=flet.colors.BLACK, width=1),)
                            ], 
                            alignment="center",#MainAxisAlignment.CENTER,
                            #horizontal_alignment=CrossAxisAlignment.CENTER,
                            spacing=15,
                        ),
                        padding=15,
                    ),
                ) for img in coins
                
            ], wrap=True, spacing=10, alignment=flet.MainAxisAlignment.CENTER,
        )

        # Создание контента для детального просмотра
        detail_content = None
        if self.selected_view == '0':
            detail_content = Column([
                Image(src=self.image_src, width=200, height=200),
                #Text(self.image_title, size=20),
                Text(
                    spans=[ flet.TextSpan(
                    self.image_games, 
                    flet.TextStyle(decoration=flet.TextDecoration.UNDERLINE),
                    url=self.image_url, ),],size=20,),
                #Text(self.image_games, size=15),
            ], alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.CENTER)
        elif self.selected_view == '2':
             detail_content = Column([
                Image(src=self.image_src, width=200, height=200),
                Text(
                    spans=[ flet.TextSpan(
                    self.image_title, 
                    flet.TextStyle(decoration=flet.TextDecoration.UNDERLINE),
                    url=self.image_url, ),],size=20,),
            ], alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.CENTER)           
        else:
            detail_content = Column([
                Image(src=self.image_src, width=200, height=200),
                Text(self.image_title, size=20),
            ], alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.CENTER)

        # Создание и возвращение нового View с деталями
        return View(
            route="/details",
            scroll=flet.ScrollMode.AUTO,
            controls=[
                appbar,
                #ElevatedButton(text="Back", on_click=back_button_clicked),
                Row(controls=[Column([detail_content, details_gallery,], alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.CENTER,),],
                alignment=MainAxisAlignment.CENTER,  wrap=True, width=self.page.width,
                          )
            ]
        )

    def information_view(self):
        md1 = """
        ## Links

        [inline-style](https://www.google.com)
        """
        return View(
            route="/information",
            scroll=flet.ScrollMode.AUTO,
            controls=[
                self.appbar,
                Row(controls=[Column([
                    Markdown("# Some Useful Information", selectable=True,) ,
                    Markdown(
                            "[__Olympic Games Information__](https://olympics.com/en/)",
                            selectable=True,
                            extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            on_tap_link=lambda e: self.page.launch_url(e.data),
                            ),   
                    Markdown(
                            "[__Winter Olympic coins__](https://en.wikipedia.org/wiki/Winter_Olympic_coins)",
                            selectable=True,
                            extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            on_tap_link=lambda e: self.page.launch_url(e.data),
                            ),
                    Markdown(
                            "[__Summer Olympic coins__](https://en.wikipedia.org/wiki/Summer_Olympic_coins)",
                            selectable=True,
                            extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            on_tap_link=lambda e: self.page.launch_url(e.data),
                            ),  
                    Markdown(
                            "[__Numista, coin & token catalog__](https://en.numista.com/)",
                            selectable=True,
                            extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            on_tap_link=lambda e: self.page.launch_url(e.data),
                            ), 
                    Markdown(
                            "[__uCoin, coin catalog__](https://en.ucoin.net/)",
                            selectable=True,
                            extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            on_tap_link=lambda e: self.page.launch_url(e.data),
                            ),   

                ], alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.CENTER, ), 
                    
                ], 
                      
                   alignment=MainAxisAlignment.CENTER,     
                )
            ]
        )
    
    def mychart1(self):
        # Создание данных для диаграммы
        data = [
            BarChartGroup(
                label="Category 1",
                bars=[BarChartRod(
                        from_y=0,
                        to_y=60,
                        width=40,
                        color=colors.ORANGE,
                        tooltip="Orange",
                        border_radius=0,

                )]
            ),
            BarChartGroup(
                label="Category 2",
                bars=[BarChartRod(
                        from_y=0,
                        to_y=60,
                        width=40,
                        color=colors.ORANGE,
                        tooltip="Orange",
                        border_radius=0,

                )]
            ),
            BarChartGroup(
                bars=[BarChartRod(
                        from_x=0,
                        to_x=40,
                        width=40,
                        color=colors.ORANGE,
                        tooltip="Orange",
                        border_radius=0,

                )]
            )
        ]

        # Создание диаграммы
        chart = BarChart(
            data=data,
            vertical=False,  # Настройка диаграммы на горизонтальную ориентацию, если поддерживается
            width=600,
            height=400,
        )
        return chart
    
