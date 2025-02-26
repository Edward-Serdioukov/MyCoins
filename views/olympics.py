import json
import flet.map as map
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
    MainAxisAlignment,
    CrossAxisAlignment,
    ThemeMode,
    AlertDialog,
    TextButton,
    FontWeight,
    icons,
    Tabs,
    Tab,
    Markdown,
    MarkdownExtensionSet,
    ListView,
    SubmenuButton,
    MenuItemButton,
)
import flet

from collections import Counter

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
            #leading=Icon(flet.icons.HOME),
            leading=IconButton(
                icon=flet.icons.HOME,
                data='0',
                on_click=self.select_view
            ),
            leading_width=40,
            title=Text("Olympic Coins"),
            center_title=False,
            bgcolor=colors.SURFACE_VARIANT,
            actions=[
                IconButton(icon=flet.icons.WB_SUNNY_OUTLINED, on_click=self.theme_changed),
                PopupMenuButton(
                    icon=flet.icons.MENU,
                    items=[
                        PopupMenuItem(text="  View: Olympics", data='0', on_click=self.select_view),
                        PopupMenuItem(text="  View: Countries", data='1', on_click=self.select_view),
                        PopupMenuItem(text="  View: Coins", data='2', on_click=self.select_view),
                        PopupMenuItem(
                            #text="View: Maps",
                            content=SubmenuButton(content=Text("View: Maps ..."), 
                                                   controls = [
                                                        MenuItemButton(content=Text("Olympics Map"), data='6', on_click=self.olympics_map_clicked),
                                                        MenuItemButton(content=Text("Countries Map"), data='7', on_click=self.countries_map_clicked),
                            
                                                 ])
                            
                        ),
                        PopupMenuItem(), 
                        PopupMenuItem(text="Information", data='5', on_click=self.information_clicked),
                        PopupMenuItem(text="Statistics", data='4', on_click=self.show_stats_modal),
                        PopupMenuItem(text="About", data='3', on_click=self.show_about_modal),
                    ]
                )
            ],
        )

    
        self.filter = Tabs(
            scrollable=True,
            selected_index=0,

            on_change=self.tabs_changed,
            tabs=[Tab(text="All"), 
                  Tab(tab_content=Icon(icons.SPORTS_SCORE_ROUNDED, color="green", tooltip="There is a coin of the country of the Olympics owner")),
                  Tab(tab_content=Icon(icons.SPORTS_SCORE_ROUNDED, color="yellow", tooltip="There is no coin of the country of the Olympics owner")),
                  Tab(tab_content=Icon(icons.SPORTS_SCORE_ROUNDED, color="red", tooltip="There is no Olimpics coin ")),
                  Tab(tab_content=Icon(icons.SPORTS_SCORE_ROUNDED, color="grey", tooltip="There is a silver coin")),
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
        
        self.informations_listtiles = ListView(
            spacing=True,
            divider_thickness=1,

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
        """Fill the gallery with olympic cards.

        This function loads olympic data from a JSON file, and creates a card for each olympic.
        The cards are added to the gallery control.
        """
        filename = 'images.json'
        filename2 = 'coins.json'

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

        if not color == "":
            # Filter olympics by color
            self.images = [item for item in data if item['color'] == color]
        elif self.filter.selected_index == 4:
            # Filter olympics by silver coins
            color = "silver"
            with open(filename2, 'r') as f:
                data2 = json.load(f)
            coins = [item['code'] for item in data2 if "Silver".lower() in item['composition'].lower()]
            self.images = [item for item in data if item['code'] in coins]
        elif self.filter.selected_index == 5:
            # Filter olympics by not silver coins
            color = "silver"
            with open(filename2, 'r') as f:
                data2 = json.load(f)
            coins = [item['code'] for item in data2 if "Silver".lower() in item['composition'].lower()]
            self.images = [item for item in data if item['code'] not in coins]

        items = self.get_cards()  # Create cards for each olympic
        self.gallery.controls = items  # Add cards to the gallery control


    def grid_countries(self):
        """Fill the gallery with country cards.

        This function loads country data from a JSON file, and creates a card for each country.
        The cards are added to the gallery control.
        """
        filename = 'countries.json'

        # Read data from the file and load it into a list of dictionaries
        with open(filename, 'r') as f:
            self.images = json.load(f)
 
        items = self.get_cards_countries() 
        self.gallery.controls = items

    def grid_coins(self):
        """
        Fill the gallery with coin cards.

        This function loads coin data from a JSON file, and creates a card for each coin.
        The cards are added to the gallery control.

        The function also filters the coins based on the selected value in the dropdown menu.
        """
        # List of images and captions
        # Path to your JSON file
        filename = 'coins.json'

        # Read data from the file and load it into a list of dictionaries
        with open(filename, 'r') as f:
            data = json.load(f)

        if self.filter_coins.selected_index == 0:
            # No filter - show all coins
            self.images = data
        elif self.filter_coins.selected_index == 1:
            # Filter by silver coins
            self.images = [item for item in data if "Silver".lower() in  item['composition'].lower()]
        elif self.filter_coins.selected_index == 2:
            # Filter by Euro coins
            self.images = [item for item in data if "Euro".lower() in  item['title'].lower()]
        elif self.filter_coins.selected_index == 3:
            # Filter by tokens
            self.images = [item for item in data if "Token".lower() in  item['title'].lower()]

        # Create cards for each coin
        items = self.get_cards_coinsview() 
        # Add cards to the gallery control
        self.gallery.controls = items


    def get_cards(self):
        """
        Create a list of Card controls for the gallery.

        The function loops through the list of images and creates a Card control
        for each one. The Card contains an Image control with the image source
        set to the first image source, a Text control with the title of the coin,
        and a Row control with the composition as a tooltip. The on_hover event is
        handled by the coin_on_hover function, which changes the image source
        between the first and second image sources when the cursor hovers over
        the element.

        The function also counts the number of images with the same code.

        Returns:
            A list of Card controls for the gallery.
        """
        with open('coins.json', 'r') as f:
            coins = json.load(f)

        # Count the number of images with the same code
        code_counts = {img['code']: sum(1 for item in coins if item['code'] == img['code']) for img in self.images}

        # Create the gallery of images
        return [
            Column(
                #col={"sm": 6, "md": 4, "xl": 1.5},
                controls=[Card(
                elevation=1,  # Level of shadow
                content=Container(
                        content=Column([
                            # Image
                            Image(src=img["src"], width=105, height=105),
                            # Title and composition
                            Row([
                                # Title
                                Text(img["title"], weight=FontWeight.BOLD, size="small"),
                                # Composition
                                #Text(f" ({code_counts[img['code']]})", weight=FontWeight.BOLD)
                            ], 
                            spacing=0, alignment="center"),
                            # Count of images with the same code
                            Row([
                                # Count
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
        """
        Create a list of Card controls for the countries view gallery.

        The function loops through the list of images and creates a Card control
        for each one. The Card contains an Image control with the image source
        set to the first image source, a Text control with the country title, and a
        Row control with the composition as a tooltip. The on_hover event is
        handled by the coin_on_hover function, which changes the image source
        between the first and second image sources when the cursor hovers over
        the element.

        Returns:
            A list of Card controls for the countries view gallery.
        """
        # Load the JSON file containing the list of coins
        with open('coins.json', 'r') as f:
            coins = json.load(f)

        # Count the number of images with the same country code
        # This is done by creating a dictionary where the keys are the country codes
        # and the values are the counts of images with that code
        code_counts = {img['country']: sum(1 for item in coins if item['country'] == img['country']) for img in self.images}

        # Create the gallery of images
        # The gallery is a list of Column controls, each containing a Card control
        # The Card control contains an Image control with the image source set to the first image source,
        # a Text control with the country title, and a Row control with the composition as a tooltip
        # The on_hover event is handled by the coin_on_hover function, which changes the image source
        # between the first and second image sources when the cursor hovers over the element
        return [
            Column(
                #col={"sm": 6, "md": 4, "xl": 1.5},
                controls=[Card(
                elevation=1,  # Level of shadow
                content=Container(
                    Column([
                        # Image
                        Image(src=img["src"], width=110, height=110),
                        # Title
                        Row([
                            Text(img["title"], weight=FontWeight.BOLD),
                        ], 
                        spacing=1, alignment="center"),
                        # Count of images with the same code
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

    def coin_on_hover(self, e):
        """
        Handles the hover event on a coin image. Changes the image source when the cursor hovers over it.

        Args:
            e: The event object containing data about the hover state and control information.
        """
        # Check if the cursor is hovering over the element
        if e.data == "true":
            # Change the image source to the alternate image when hovered
            e.control.content.controls[0].src = e.control.data["src2"]
        else:
            # Revert to the original image source when the cursor leaves
            e.control.content.controls[0].src = e.control.data["src1"]

        # Update the interface to reflect the changes
        e.control.update()
        
    def get_cards_coinsview(self):
        """
        Generate a list of Card controls for the coins view gallery.

        The function loops through the list of images and creates a Card control
        for each one. The Card contains an Image control with the image source
        set to the first image source, a Text control with the coin title, and a
        Row control with the composition as a tooltip. The on_hover event is
        handled by the coin_on_hover function, which changes the image source
        between the first and second image sources when the cursor hovers over
        the element.

        Returns:
            A list of Card controls for the coins view gallery.
        """
        # Создание галереи картинок
        return  [
            Column(
                #col={"sm": 6, "md": 4, "xl": 1.5},
                controls=[Card(
                    elevation=1,  # Уровень тени
                    content= Container(
                        Column([
                            Image(
                                src=img["src1"],
                                tooltip=img["composition"],
                                width=115,
                                height=115
                            ),
                            Row([
                                Text(img["title"], weight=FontWeight.BOLD),
                            ], 
                            spacing=1,alignment="center"),
                        ], 
                        horizontal_alignment="center",
                        alignment="center"),
                    on_hover=self.coin_on_hover, 
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

    def click_home(self, e):
        self.selected_view = e.control.data
        self.refresher()
        self.page.go("/olympics")
        
    def select_view(self, e):
        self.selected_view = e.control.data
        self.refresher()
        self.page.go("/olympics")
   

    def on_image_click(self, e):
        """Handles the image click event in the olympics view.

        When an image is clicked, this function is called. It determines the
        selected view and sets the corresponding attributes of the class. The
        page is then navigated to the details page.

        Args:
            e (Event): The event object.
        """
        if self.selected_view == '0':
            # Selected view is the games view
            self.image_games = e.control.data["games"]
        if self.selected_view == '1':
            # Selected view is the countries view
            self.image_country = e.control.data["country"]
        if self.selected_view == '2':
            # Selected view is the coins view
            self.image_src = e.control.data["src1"]
        else:
            # Selected view is the default view
            self.image_src = e.control.data["src"]
        self.image_title = e.control.data["title"]
        self.image_url = e.control.data["url"]
        self.image_code = e.control.data["code"]
        self.page.go("/details")


    def on_marker_click(self, e):
        """Handles the marker click event in the olympics map view.

        When a marker is clicked, this function is called. It determines the
        selected view and sets the corresponding attributes of the class. The
        page is then navigated to the details page.

        Args:
            e (Event): The event object.
        """
        self.image_src = e.control.data["src"]
        self.image_games = e.control.data["games"]    
        self.image_title = e.control.data["title"]
        self.image_url = e.control.data["url"]
        self.image_code = e.control.data["code"]  
        self.page.go("/details_olympic_map")


    def on_country_click(self, e):
        """Handles the country click event in the countries map view.

        When a country is clicked, this function is called. It determines the
        selected view and sets the corresponding attributes of the class. The
        page is then navigated to the details page.

        Args:
            e (Event): The event object.
        """
        self.image_src = e.control.data["src"]
        self.image_country = e.control.data["country"]
        self.image_title = e.control.data["title"]
        self.image_url = e.control.data["url"]
        self.image_code = e.control.data["code"]  
        self.page.go("/details_country_map")

    def information_clicked(self, e):
        self.page.go("/information")
  
    def olympics_map_clicked(self, e):
        self.selected_view = e.control.data
        self.page.go("/olympics_map")

    def countries_map_clicked(self, e):
        self.selected_view = e.control.data
        self.page.go("/countries_map")

    def check_item_clicked(self, e):
        e.control.checked = not e.control.checked
        self.page.update()

    def show_stats_modal(self, e):
        """Shows a modal dialog with the statistics about the coins and olympics.

        The dialog shows the number of coins, olympics, countries, silver olympics,
        silver coins and tokens.
        """
        def close_dlg(e):
            """Closes the dialog."""
            dlg_modal.open = False
            self.page.update()

        # Read the data from the JSON files
        with open('coins.json', 'r') as f:
            data1 = json.load(f)
        coins = len(data1)
        with open('images.json', 'r') as f:
            data2 = json.load(f)
        olympics = len(data2)
        with open('countries.json', 'r') as f:
            data3 = json.load(f)
        contries = len(data3)

        # Count the number of silver coins and tokens
        silver_coins = [item['code'] for item in data1 if "Silver".lower() in item['composition'].lower()]
        olympics_silver = [item for item in data2 if item['code'] in silver_coins]
        tokens = [item['code'] for item in data1 if "Token".lower() in item['title'].lower()]
        coins = coins - len(tokens)

        # Create the modal dialog
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
                            ], spacing=0, ), border=flet.border.all(color=flet.colors.BLACK, width=1), padding=0, ),
            actions=[flet.TextButton("Close", on_click=lambda e: close_dlg(e))],
            actions_alignment=flet.MainAxisAlignment.END,
        )
        # Show the modal dialog
        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.page.update()

    def show_about_modal(self, e):
        """Show the 'About' modal dialog."""
        def close_dlg(e):
            """Close the modal dialog."""
            dlg_modal.open = False
            self.page.update()

        # Create the image widget for the modal dialog
        image = flet.Image(src='icons/logo1.png', width=200, height=200) 
        
        # Create the modal dialog with the image
        dlg_modal = flet.AlertDialog(
            modal=True,
            title=flet.Text("About"),
            content=flet.Column([
                image,
                flet.ListTile(
                    title=flet.Text("My coins collection"),
                    subtitle=flet.Text(
                        spans=[
                            flet.TextSpan(
                                "e-mail: mycoins92@gmail.com", 
                                flet.TextStyle(decoration=flet.TextDecoration.UNDERLINE),
                                url="mailto: mycoins92@gmail.com", 
                            )
                        ],
                        size=10,
                    )
                )
            ], 
            alignment=flet.MainAxisAlignment.CENTER,
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            height=300,
            ),
            actions=[
                flet.TextButton("Close", on_click=lambda e: close_dlg(e))
            ],
            actions_alignment=flet.MainAxisAlignment.END,
        )            
        # Show the modal dialog
        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.page.update() 

    def view(self):
        return 	self.main_view


    def create_cell_with_border(self, text: str, width: int = 150, height: int = 100) -> Container:
        """Create a cell with a border for the table.

        The cell contains a `Text` widget with the given `text` and will have the given `width` and `height`.
        The `border` property is set to a black border with a width of 1 pixel.

        Args:
            text (str): The text to display in the cell.
            width (int, optional): The width of the cell. Defaults to 150.
            height (int, optional): The height of the cell. Defaults to 100.

        Returns:
            Container: The cell container with the given properties.
        """
        return Container(
            # Take the available space in the row
            expand=True,
            # The content of the cell is a Text widget with the given text
            content=Text(text),
            # Set the width and height of the cell
            width=width,
            height=height,
            # Add some padding to the cell
            padding=5,
            # Center the text in the cell
            alignment=flet.alignment.center,
            # Set the border of the cell
            border=flet.border.all(color=flet.colors.BLACK, width=1),  # Set the border to a black border with a width of 1 pixel
        )
    
    def details_view(self):
        """
        This function is called when the user selects a row in the main view
        and then clicks on the "Details" button.

        It creates a new view that displays the details of the selected coin.

        The view contains a card with the image of the coin, and a gallery
        of images of the coin with the same denomination but from different
        countries.

        The view also contains a text field with the title of the coin, and
        a text field with the composition of the coin.

        The view is created with a scroll mode of AUTO, which means that the
        user can scroll vertically to see more content.

        The view is returned to the main view so that it can be displayed.
        """
        def show_image_modal(e):
            """
            This function is called when the user clicks on an image in the
            gallery.

            It creates a modal dialog with the image and displays it to the
            user.

            The dialog contains a close button that the user can click to
            close the dialog.
            """
            def close_dlg(e):
                """
                This function is called when the user clicks on the close
                button in the dialog.

                It closes the dialog and updates the page.
                """
                dlg_modal.open = False
                self.page.update()
            
            # Create the image that will be displayed in the dialog
            image = Image(src=e.control.content.src, width=300, height=300)  
            # Create the description that will be displayed in the dialog
            description = Container( Text(coins[0]['description'], no_wrap=False, size=14), width=400, padding=10)

            # Create the dialog
            dlg_modal = AlertDialog(
                modal=True,
                #title=Text("Просмотр изображения"),
                content=Container(Column([image,description],alignment=flet.MainAxisAlignment.START,horizontal_alignment=flet.CrossAxisAlignment.CENTER,scroll=flet.ScrollMode.ALWAYS,),),
                actions=[TextButton("Close", on_click=lambda e: close_dlg(e))],
                actions_alignment=MainAxisAlignment.END,
            )            
            # Show the dialog
            self.page.dialog = dlg_modal
            dlg_modal.open = True
            self.page.update()
            
        # Read the data from the JSON file
        filename = 'coins.json'

        # Read the data from the file and load it into a list of dictionaries
        with open(filename, 'r') as f:
            data = json.load(f)
        
        str_name = ''
        str_value= ''
        # Determine which field to filter by based on the selected view
        if self.selected_view in {'0','6'}:
            str_name = 'code'
            str_value = self.image_code
        elif self.selected_view in {'1','7'}:
            str_name = 'country'
            str_value = self.image_country
        elif self.selected_view == '2':
            str_name = 'src1'
            str_value = self.image_src
        
        # Filter the data based on the selected field
        coins = [item for item in data if item[str_name] == str_value]

        # Create the app bar for the details view
        appbar = AppBar(
                title=Text(self.image_title),
                center_title=False,
                bgcolor=colors.SURFACE_VARIANT,
            )
        # Create the gallery of images
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

        # Create the content for the details view
        detail_content = None
        if self.selected_view in {'0','6'}:
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

        # Create and return the new view with the details
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
        self.informations_listtiles.controls.clear()
        links = Row(controls=[Column([
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
                    Markdown(
                            "[__Collector and commemorative coins__](https://www.coin-database.com/)",
                            selectable=True,
                            extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            on_tap_link=lambda e: self.page.launch_url(e.data),
                            ),                      
                    Markdown(
                            "[__Colnect, coin catalog__](https://colnect.com/en/coins)",
                            selectable=True,
                            extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            on_tap_link=lambda e: self.page.launch_url(e.data),
                            ),  
                    
                    Markdown(
                            "[__Coin grading__](https://en.wikipedia.org/wiki/Coin_grading)",
                            selectable=True,
                            extension_set=MarkdownExtensionSet.GITHUB_WEB,
                            on_tap_link=lambda e: self.page.launch_url(e.data),
                            ),   


                ], alignment=MainAxisAlignment.CENTER,horizontal_alignment=CrossAxisAlignment.CENTER,  ),              
                ], alignment=MainAxisAlignment.CENTER,     
            )
        self.informations_listtiles.controls.append(links)

        return View(
            route="/information",
            scroll=flet.ScrollMode.AUTO,
            controls=[
                self.appbar,
                self.informations_listtiles,
            ]
        )
    
   
    """
    Displays a map of Olympic games locations.

    The map is based on OpenStreetMap tiles and includes markers for each Olympic
    games location. Each marker has a tooltip that displays the name of the games
    and the year, and clicking on the marker displays a modal dialog with the
    name, year, and country of the games.

    """
    def olympics_map_view(self):

        def show_image_modal(e):
            """
            Shows a modal dialog with the details of the Olympic games.

            The dialog includes the name, year, and country of the games, as well
            as a link to the official website of the Olympic Games.

            Args:
                e (Event): The event that triggered the modal dialog.
            """
            def close_dlg(e):
                """
                Closes the modal dialog.

                Args:
                    e (Event): The event that triggered the dialog close.
                """
                dlg_modal.open = False
                self.page.update()

            # Create the content of the modal dialog
            image = Image(src=e.control.data["src"], width=300, height=300)  
            description = Text(e.control.data["games"], no_wrap=False, size=20, weight=FontWeight.BOLD)
            url = Text(spans=[ flet.TextSpan( e.control.data["title"], 
                    flet.TextStyle(decoration=flet.TextDecoration.UNDERLINE),
                    url=e.control.data["url"], ),],size=20, weight=FontWeight.BOLD)

            # Create the modal dialog
            dlg_modal = AlertDialog(
                modal=True,
                #title=Text("Olympic Games Details"),
                content=Container(Column([image,description,url],alignment=flet.MainAxisAlignment.START,horizontal_alignment=flet.CrossAxisAlignment.CENTER,scroll=flet.ScrollMode.ALWAYS,),),
                actions=[TextButton("Close", on_click=lambda e: close_dlg(e))],
                actions_alignment=MainAxisAlignment.END,
            )            
            # Show the modal dialog
            self.page.dialog = dlg_modal
            dlg_modal.open = True
            self.page.update()

        with open('images.json', 'r') as f:
            data = json.load(f)

        marker_layer_ref = flet.Ref[map.MarkerLayer]()
        circle_layer_ref = flet.Ref[map.CircleLayer]()


        olympics_map = map.Map(
            expand=True,
            configuration=map.MapConfiguration(
                initial_center=map.MapLatitudeLongitude(48, 2),
                initial_zoom=3,
                interaction_configuration=map.MapInteractionConfiguration(
                    flags=map.MapInteractiveFlag.ALL
                ),
                on_init=lambda e: print(f"Initialized Map"),
                #on_tap=handle_tap,
                #on_secondary_tap=handle_tap,
                #on_long_press=handle_tap,
                #on_event=handle_event,
            ),
            layers=[
                map.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    #url_template="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
                    on_image_error=lambda e: print("TileLayer Error"),
                ),
                map.MarkerLayer(
                    ref=marker_layer_ref,
                    markers=[
                        
                        map.Marker(
                            content=Container(content=Image(src="icons/location2-red.png" if img["code"].endswith("s") else "icons/location2.png",
                                                            width=345, height=345),
                                            alignment=flet.alignment.center,
                                            data=img,  width=345, height=345,
                                            on_click=self.on_marker_click,
                                            tooltip=flet.Tooltip(
                                                message=img["title"],
                                                padding=20,
                                                border_radius=10,
                                                bgcolor=colors.WHITE,
                                                text_style=flet.TextStyle(size=20, color=colors.BLACK),),
                                            ),
                             coordinates=map.MapLatitudeLongitude(img["coordinates"]["lat"], img["coordinates"]["lon"]),
                        ) for img in data
                    ],
                ), 
            ],
        )
                                                            
        return View(
            route="/olympics_map",
            #scroll=flet.ScrollMode.AUTO,
            controls=[
                self.appbar,
                olympics_map,
            ]
        )

        
    """
    flet.Tooltip(
                                        message=img["title"],
                                        content= IconButton(content=Icon(icons.LOCATION_ON, 
                                                    color="red" if img["code"].endswith("s") else "blue",
                                                    #tooltip=img["title"]
                                                ),
                                            alignment=flet.alignment.center,
                                            icon_size=25,
                                            data=img,
                                            #on_click=lambda e: show_image_modal(e)
                                            on_click=self.on_marker_click,
                                        ),
                
                                        padding=20,
                                        border_radius=10,
                                        bgcolor=colors.WHITE,
                                        text_style=flet.TextStyle(size=20, color=colors.BLACK),
                                    ),
    """

    def countries_map_view(self):

        with open('countries.json', 'r') as f:
            data = json.load(f)

        marker_layer_ref = flet.Ref[map.MarkerLayer]()
        circle_layer_ref = flet.Ref[map.CircleLayer]()


        countries_map = map.Map(
            expand=True,
            configuration=map.MapConfiguration(
                initial_center=map.MapLatitudeLongitude(47, 13),
                initial_zoom=3.5,
                interaction_configuration=map.MapInteractionConfiguration(
                    flags=map.MapInteractiveFlag.ALL
                ),
                on_init=lambda e: print(f"Initialized Map"),
                #on_tap=handle_tap,
                #on_secondary_tap=handle_tap,
                #on_long_press=handle_tap,
                #on_event=handle_event,
            ),
            layers=[
                map.TileLayer(
                    #url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    url_template="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
                    on_image_error=lambda e: print("TileLayer Error"),
                ),
                map.MarkerLayer(
                    ref=marker_layer_ref,
                    markers=[
                        map.Marker(
                            content=Container(image_src=img["avatar"], width=30, height=30, tooltip=img["title"],
                                            data=img,

                                            on_click=self.on_country_click,),
                            coordinates=map.MapLatitudeLongitude(img["coordinates"]["latitude"], img["coordinates"]["longitude"]),
                        ) for img in data
                    ],
                ), 
            ],
        )
                                                            
        return View(
            route="/countries_map",
            #scroll=flet.ScrollMode.AUTO,
            controls=[
                self.appbar,
                countries_map,
            ]
        )



    """    
    IconButton(content=Icon(icons.LOCATION_ON, 
                                        color="red" if img["code"].endswith("s") else "blue",
                                        #tooltip=img["title"]
                                    ),
                        alignment=flet.alignment.center,
                        icon_size=25,
                        data=img,
                        #on_click=lambda e: show_image_modal(e)
                        on_click=self.on_marker_click,
                        ),
    """    