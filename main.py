import flet as ft
import time
from manage_database import database

def main(page: ft.Page):
    page.title = "Game Catalog"
    base = database()

    #CHECK FUNCTIONS

    def check_time(time):
        time.split()
        return True

    def check_copies(copies):
        try:
            int(copies)
            return True
        except:
            return False

    def check_fields(e, title, copies, time, status, platform, subscription, box, paid, publisher, developer, series):
        if not (title and copies and time and status and platform and subscription and publisher and box and paid and developer and series):
            page.add(ft.Text("Please fill out all fields!", color="red"))
            return False   
        else:
            if check_copies(copies):
                if check_time(time):
                    return True
                else:
                    page.add(ft.Text('Time is not an integer!', color="red")) 
                    return False
            else:
                page.add(ft.Text('"Copies" are not an integer!', color="red")) 
                return False
        

    # REST OF GUI
    def add_series(e, series):
        base.add_series(series)
        page.update()
        page.add(ft.Text(f'"{series}" - added'))

    def edit_series(e):
        series_field = ft.TextField(label="Enter series name")
        page.clean()
        page.add(series_field)
        page.add(ft.Row(controls=[ft.ElevatedButton("Add", on_click=lambda e:add_series(e, series_field.value)), ft.OutlinedButton("Back", on_click=add_game_menu)]))
        page.add(ft.Text("Series:"))
        for series in base.show_series():
            page.add(ft.Text(f"{series[1]}"))  

    def add_platform(e, platform):
        base.add_platform(platform)
        page.update()
        page.add(ft.Text(f'"{platform}" - added'))

    def edit_platforms(e):
        platform_field = ft.TextField(label="Enter platform name")
        page.clean()
        page.add(platform_field)
        page.add(ft.Row(controls=[ft.ElevatedButton("Add", on_click=lambda e:add_platform(e, platform_field.value)), ft.OutlinedButton("Back", on_click=add_game_menu)]))
        page.add(ft.Text("Platforms:"))
        for platform in base.show_platform():
            page.add(ft.Text(f"{platform[1]}"))       

    def add_publisher(e, publisher):
        base.add_publisher(publisher)
        page.update()
        page.add(ft.Text(f'"{publisher}" - added'))

    def edit_publisher(e):
        publisher_field = ft.TextField(label="Enter publisher name")
        page.clean()
        page.add(publisher_field)
        page.add(ft.Row(controls=[ft.ElevatedButton("Add", on_click=lambda e:add_publisher(e, publisher_field.value)), ft.OutlinedButton("Back", on_click=add_game_menu)]))
        page.add(ft.Text("Publishers:"))
        for publisher in base.show_publisher():
            page.add(ft.Text(f"{publisher[1]}"))       

    def add_developer(e, developer):
        base.add_developer(developer)
        page.update()
        page.add(ft.Text(f'"{developer}" - added'))

    def edit_developer(e):
        developer_field = ft.TextField(label="Enter developer name")
        page.clean()
        page.add(developer_field)
        page.add(ft.Row(controls=[ft.ElevatedButton("Add", on_click=lambda e:add_developer(e, developer_field.value)), ft.OutlinedButton("Back", on_click=add_game_menu)]))
        page.add(ft.Text("Developers:"))
        for developer in base.show_developer():
            page.add(ft.Text(f"{developer[1]}"))       

    def add_subscription(e, subscription, platform):
        base.add_subscription(subscription, platform)
        page.update()
        page.add(ft.Text(f'"{subscription}" - added'))      

    def edit_subscriptions(e):
        subscription_field = ft.TextField(label="Enter subscription name")
        platform_field = ft.Dropdown(label="Platform")
        for database_platforms in base.show_platform():
            platform_field.options.append(ft.dropdown.Option(database_platforms[1]))
        platform_field.value = platform_field.options[0].key

        page.clean()
        page.add(ft.Row(controls=[subscription_field, platform_field]))
        page.add(ft.Row(controls=[ft.ElevatedButton("Add", on_click=lambda e:add_subscription(e, subscription_field.value, platform_field.value)), ft.OutlinedButton("Back", on_click=add_game_menu)]))
        page.add(ft.Text("Subscriptions:"))
        for subscription in base.show_subscription():
            platform_name = base.get_platform_name(int(subscription[2]))
            page.add(ft.Text(f"{subscription[1]}, {platform_name}"))

    def add_game(e, title, copies, time, status, platform, subscription, box, paid, publisher, developer, series):
        if check_fields(e, title, copies, time, status, platform, subscription, box, paid, publisher, developer, series):
            if paid == "No":
                paid = 0
            else:
                paid = 1
            if box == "No":
                box = 0
            else:
                box = 1
            base.add_game(title, copies, time, status, platform, subscription, box, paid, publisher, developer,  series)
            page.clean()
            main(page)
        page.add(ft.Text("Please fill out all fields!", color="red"))   

    def add_game_menu(e):
        page.clean()
        page.add(ft.Text("Add game"))
        title_field = ft.TextField(label="Title")
        copies_field = ft.TextField(label="Number of copies", value="1")
        time_hours_field = ft.TextField(label="Game time: Hours", value="0")
        time_minutes_field = ft.TextField(label="Game time: Minutes", value="0")
        time_seconds_field = ft.TextField(label="Game time: Seconds", value="0")
        status_field = ft.Dropdown(label="Status", options=[ft.dropdown.Option("Finished"), ft.dropdown.Option("Started"), ft.dropdown.Option("Not started")])
        status_field.value = status_field.options[2].key

        platform_field = ft.Dropdown(label="Platform")
        for database_platforms in base.show_platform():
            platform_field.options.append(ft.dropdown.Option(database_platforms[1]))
        platform_field.value = platform_field.options[0].key

        subscription_field = ft.Dropdown(label="Subscription")
        for database_subscriptions in base.show_subscription():
            subscription_field.options.append(ft.dropdown.Option(database_subscriptions[1]))
        subscription_field.value = subscription_field.options[0].key

        box_field = ft.Dropdown(label="Box", options=[ft.dropdown.Option("Yes"), ft.dropdown.Option("No")])
        box_field.value = box_field.options[0].key

        paid_field = ft.Dropdown(label="Paid", options=[ft.dropdown.Option("Yes"), ft.dropdown.Option("No")])
        paid_field.value = paid_field.options[0].key

        publisher_field = ft.Dropdown(label="Publisher")
        for database_publishers in base.show_publisher():
            publisher_field.options.append(ft.dropdown.Option(database_publishers[1]))


        developer_field = ft.Dropdown(label="Developer")
        for database_developer in base.show_developer():
            developer_field.options.append(ft.dropdown.Option(database_developer[1]))

        series_field = ft.Dropdown(label="Series")
        for database_series in base.show_series():
            series_field.options.append(ft.dropdown.Option(database_series[1]))
        
        add_platform = ft.ElevatedButton("Edit platforms", on_click=edit_platforms)
        add_subscription = ft.ElevatedButton("Edit subscriptions", on_click=edit_subscriptions)
        add_series = ft.ElevatedButton("Edit series", on_click=edit_series)
        add_publisher = ft.ElevatedButton("Edit publishers", on_click=edit_publisher)
        add_developer = ft.ElevatedButton("Edit developers", on_click=edit_developer)


        games_fields = ft.Column([title_field,
                            copies_field,
                            ft.Row(controls=[time_hours_field, ft.Text(":"), time_minutes_field, ft.Text(":"), time_seconds_field]),
                            status_field,
                            ft.Row(controls=[platform_field, add_platform]),
                            ft.Row(controls=[subscription_field, add_subscription]),
                            box_field,
                            paid_field,
                            ft.Row(controls=[publisher_field, add_publisher]),
                            ft.Row(controls=[developer_field, add_developer]),
                            ft.Row(controls=[series_field, add_series])], scroll=ft.ScrollMode.AUTO, expand=True)

        page.add(games_fields)
        
        add_game_btn = ft.ElevatedButton("Add", 
                                   on_click=lambda e:add_game(e,
                                                     title_field.value, 
                                                     copies_field.value, 
                                                     f"{time_hours_field.value}:{time_minutes_field.value}:{time_seconds_field.value}", 
                                                     status_field.value, 
                                                     platform_field.value, 
                                                     subscription_field.value,
                                                     box_field.value, 
                                                     paid_field.value, 
                                                     publisher_field.value, 
                                                     developer_field.value, 
                                                     series_field.value), 
                                   data=0)
        back_btn = ft.OutlinedButton("Back", on_click=lambda e:main(page))
        page.add(ft.Row(controls=[add_game_btn, back_btn]))

    def delete_game(e, title):
        base.delete_game(title)
        main(page)

    def modify_game(e, id, title, copies, time, status, platform, subscription, box, paid, publisher, developer, series):
        if check_fields(e, title, copies, time, status, platform, subscription, box, paid, publisher, developer, series):
            if paid == "No":
                paid = 0
            else:
                paid = 1
            if box == "No":
                box = 0
            else:
                box = 1
            base.modify_game(id, title, copies, time, status, platform, subscription, box, paid, publisher, developer,  series)
            page.clean()
            main(page)
        page.add(ft.Text("Please fill out all fields!", color="red"))   

    def modify(e, title):
        game = base.show_game(title)[0]
        page.clean()
        page.add(ft.Text("Modify game"))
        title_field = ft.TextField(label="Title", value = game[1])
        copies_field = ft.TextField(label="Number of copies", value = game[2])
        if game[3] != "-":
            time_hours_field = ft.TextField(label="Game time: Hours", value=game[3].split(":")[0])
            time_minutes_field = ft.TextField(label="Game time: Minutes", value=game[3].split(":")[1])
            time_seconds_field = ft.TextField(label="Game time: Seconds", value=game[3].split(":")[2])
        else:
            time_hours_field = ft.TextField(label="Game time: Hours", value=game[3])
            time_minutes_field = ft.TextField(label="Game time: Minutes", value=game[3])
            time_seconds_field = ft.TextField(label="Game time: Seconds", value=game[3])
        status_field = ft.Dropdown(label="Status", options=[ft.dropdown.Option("Finished"), ft.dropdown.Option("Started"), ft.dropdown.Option("Not started")])
        status_field.value = base.get_status_name(game[4])

        platform_field = ft.Dropdown(label="Platform")
        for database_platforms in base.show_platform():
            platform_field.options.append(ft.dropdown.Option(database_platforms[1]))
        platform_field.value = base.get_platform_name(game[5])

        subscription_field = ft.Dropdown(label="Subscription")
        for database_subscriptions in base.show_subscription():
            subscription_field.options.append(ft.dropdown.Option(database_subscriptions[1]))
        subscription_field.value = base.get_subscription_name(game[6])

        box_field = ft.Dropdown(label="Box", options=[ft.dropdown.Option("Yes"), ft.dropdown.Option("No")])
        box_field.value = box_status(game[7])
        
        paid_field = ft.Dropdown(label="Paid", options=[ft.dropdown.Option("Yes"), ft.dropdown.Option("No")])
        paid_field.value = paid_status(game[8])

        publisher_field = ft.Dropdown(label="Publisher")
        for database_publishers in base.show_publisher():
            publisher_field.options.append(ft.dropdown.Option(database_publishers[1]))
        publisher_field.value = base.get_publisher_name(game[9])


        developer_field = ft.Dropdown(label="Developer")
        for database_developer in base.show_developer():
            developer_field.options.append(ft.dropdown.Option(database_developer[1]))
        developer_field.value = base.get_developer_name(game[10])

        series_field = ft.Dropdown(label="Series")
        for database_series in base.show_series():
            series_field.options.append(ft.dropdown.Option(database_series[1]))
        series_field.value = base.get_series_name(game[11])
        
        add_platform = ft.ElevatedButton("Edit platforms", on_click=edit_platforms)
        add_subscription = ft.ElevatedButton("Edit subscriptions", on_click=edit_subscriptions)
        add_series = ft.ElevatedButton("Edit series", on_click=edit_series)
        add_publisher = ft.ElevatedButton("Edit publishers", on_click=edit_publisher)
        add_developer = ft.ElevatedButton("Edit developers", on_click=edit_developer)


        games_fields = ft.Column([title_field,
                            copies_field,
                            ft.Row(controls=[time_hours_field, ft.Text(":"), time_minutes_field, ft.Text(":"), time_seconds_field]),
                            status_field,
                            ft.Row(controls=[platform_field, add_platform]),
                            ft.Row(controls=[subscription_field, add_subscription]),
                            box_field,
                            paid_field,
                            ft.Row(controls=[publisher_field, add_publisher]),
                            ft.Row(controls=[developer_field, add_developer]),
                            ft.Row(controls=[series_field, add_series])], scroll=ft.ScrollMode.AUTO, expand=True)

        page.add(games_fields)
        
        modify_game_btn = ft.ElevatedButton("Modify", 
                                   on_click=lambda e:modify_game(e,
                                                     int(game[0]),
                                                     title_field.value, 
                                                     copies_field.value, 
                                                     f"{time_hours_field.value}:{time_minutes_field.value}:{time_seconds_field.value}", 
                                                     status_field.value, 
                                                     platform_field.value, 
                                                     subscription_field.value,
                                                     box_field.value, 
                                                     paid_field.value, 
                                                     publisher_field.value, 
                                                     developer_field.value, 
                                                     series_field.value), 
                                   data=0)
        back_btn = ft.OutlinedButton("Back", on_click=lambda e:main(page))
        page.add(ft.Row(controls=[modify_game_btn, back_btn]))

    def edit_game_menu(e):
        page.clean()
        games = ft.Dropdown(label="Games list")
        for game in base.show_games():
            games.options.append(ft.dropdown.Option(game[1]))
        page.add(games)
        page.add(ft.Row(controls=[ft.ElevatedButton("Delete game", on_click=lambda e:delete_game(e, games.value), data=0), 
                                  ft.ElevatedButton("Modify", on_click=lambda e:modify(e, games.value)), 
                                  ft.ElevatedButton("Back", on_click=lambda e:main(page))]))

    def create_database(e):
        base.connect()
        base.create_tables()
        base.configure_tables()
        page.clean()
        main(page)

    def load_database_from_gdrive(e):
        pass

    def box_status(box):
        if box == 1:
            return "Yes"
        elif box == 0:
            return "No"
        else:
            "Error!"

    def paid_status(paid):
        if paid == 1:
            return "Yes"
        elif paid == 0:
            return "No"
        else:
            "Error!"

    def set_color(status):
        if status == 1:
            return "green"
        elif status == 2:
            return "orange"
        elif status == 3:
            return "red"
        else:
            return "black"

    def get_games_datatable(begin = 0, end = -1):
        games_rows = []
        games_list = base.show_games()

        for game in games_list[begin:end]:
            cell_tab = []
            cell_tab.append(ft.DataCell(ft.Text(game[0])))
            cell_tab.append(ft.DataCell(ft.Text(game[1])))
            cell_tab.append(ft.DataCell(ft.Text(game[2])))
            cell_tab.append(ft.DataCell(ft.Text(game[3])))
            cell_tab.append(ft.DataCell(ft.Text(base.get_status_name(game[4]))))
            cell_tab.append(ft.DataCell(ft.Text(base.get_platform_name(game[5]))))
            cell_tab.append(ft.DataCell(ft.Text(base.get_subscription_name(game[6]))))
            cell_tab.append(ft.DataCell(ft.Text(box_status(game[7]))))
            cell_tab.append(ft.DataCell(ft.Text(paid_status(game[8]))))
            cell_tab.append(ft.DataCell(ft.Text(base.get_publisher_name(game[9]))))
            cell_tab.append(ft.DataCell(ft.Text(base.get_developer_name(game[10]))))
            cell_tab.append(ft.DataCell(ft.Text(base.get_series_name(game[11]))))
            games_rows.append(ft.DataRow(cells=cell_tab, color=set_color(game[4])))
        games_columns = []
        games_columns.append(ft.DataColumn(ft.Text("ID")))
        games_columns.append(ft.DataColumn(ft.Text("Title")))
        games_columns.append(ft.DataColumn(ft.Text("Copies")))
        games_columns.append(ft.DataColumn(ft.Text("Game time (H:M:S)")))
        games_columns.append(ft.DataColumn(ft.Text("Status")))
        games_columns.append(ft.DataColumn(ft.Text("Platform")))
        games_columns.append(ft.DataColumn(ft.Text("Subscription")))
        games_columns.append(ft.DataColumn(ft.Text("Box")))
        games_columns.append(ft.DataColumn(ft.Text("Paid")))
        games_columns.append(ft.DataColumn(ft.Text("Publisher")))
        games_columns.append(ft.DataColumn(ft.Text("Developer")))
        games_columns.append(ft.DataColumn(ft.Text("Serie")))           

        table = ft.DataTable(
            sort_column_index=0,
            sort_ascending=True,
            show_checkbox_column=True,
            columns= games_columns,
            rows = games_rows
        )
    
        return ft.Column([table], scroll=ft.ScrollMode.AUTO, expand=True)

    def move_left_game_list(list_begin, list_end):
        if list_begin - 50 < 0:
            return 0
        else:
            list_begin -= 50
            list_end = list_begin + 50
        page.clean()
        init_navbar(list_begin, list_end)

    def move_right_game_list(list_begin, list_end):
        if list_end + 50 > len(base.show_games()) and list_begin + 50 < len(base.show_games()):
            list_begin += 50
            list_end = len(base.show_games())
        elif list_end != len(base.show_games()):
            list_begin += 50
            list_end = list_begin + 50
        page.clean()
        init_navbar(list_begin, list_end)

    ### NAVIGATION MENU

    def manage_database_view(list_begin, list_end):
        if base.exist():
            if base.show_games() != []:
                if list_begin == 0 and list_end == len(base.show_games()):
                    show_all = ft.OutlinedButton("Show less", on_click=lambda e:init_navbar(0, 50), data=0)
                else:
                    show_all = ft.ElevatedButton("Show all", on_click=lambda e:init_navbar(0, len(base.show_games())), data=0)
                return ft.Column([
                    ft.Text("Game list", style="headlineMedium"),
                    ft.Row(controls=[ft.ElevatedButton("Add game", on_click=add_game_menu, data=0),
                                     ft.ElevatedButton("Edit game list", on_click=edit_game_menu, data=0)]),
                    ft.Row(controls=[ft.ElevatedButton("Search", on_click=add_game_menu, data=0),
                                     ft.ElevatedButton("Filters", on_click=edit_game_menu, data=0)]),
                    ft.Row(controls=[ft.ElevatedButton("<", on_click=lambda e:move_left_game_list(list_begin, list_end), data=0),
                                     ft.Text(f"{list_begin} - {list_end}"),
                                     ft.ElevatedButton(">", on_click=lambda e:move_right_game_list(list_begin, list_end), data=0),
                                     show_all]),
                    get_games_datatable(list_begin, list_end)
                    ], scroll=ft.ScrollMode.AUTO, expand=True)
            else:
                return ft.Column([
                    ft.Text("Game list", style="headlineMedium"),
                    ft.ElevatedButton("Add game", on_click=add_game_menu, data=0)
                    ])
        else:
            return ft.Column([
                ft.Text("No database found!"),
                ft.ElevatedButton("Create a new database", on_click=create_database, data=0),
                ft.ElevatedButton("Load database from Google Drive", on_click=add_game_menu, data=0)
                ])

    # ***************
    # STATISTICS VIEW
    # ***************

    def number_of_games_table():
        return ft.DataTable(columns=[
                ft.DataColumn(ft.Text("Number of games:")),
                ft.DataColumn(ft.Text("Value:"))
            ],
            rows =[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Total number of games")),
                        ft.DataCell(ft.Text(str(len(base.show_games()))))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Number of games owned")),
                        ft.DataCell(ft.Text(str(len(base.show_owned_games()))))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Number of subscription games")),
                        ft.DataCell(ft.Text(str(len(base.show_subscription_games()))))
                    ]
                ),
            ]

            )
    
    def total_game_time_table():
        return ft.DataTable(columns=[
                ft.DataColumn(ft.Text("Total playing time:")),
                ft.DataColumn(ft.Text("Value:"))
            ],
            rows =[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Days:")),
                        ft.DataCell(ft.Text(""))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Hours:")),
                        ft.DataCell(ft.Text(""))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Minutes:")),
                        ft.DataCell(ft.Text(""))
                    ]
                ),
            ]
            )    

    def the_longest_game_time_table():
        return ft.DataTable(columns=[
                ft.DataColumn(ft.Text("The longest playing time:")),
                ft.DataColumn(ft.Text("Value:"))
            ],
            rows =[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Playing time:")),
                        ft.DataCell(ft.Text(""))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Title:")),
                        ft.DataCell(ft.Text(""))
                    ]
                )
            ]
            )          

    def the_shortest_game_time_table():
        return ft.DataTable(columns=[
                ft.DataColumn(ft.Text("The shortest playing time:")),
                ft.DataColumn(ft.Text("Value:"))
            ],
            rows =[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Playing time:")),
                        ft.DataCell(ft.Text(""))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Title:")),
                        ft.DataCell(ft.Text(""))
                    ]
                )
            ]
            )     

    def summaries():          
            return ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
            ft.Tab(
                text="Summaries",
                content=ft.Column([
                        ft.Text("Summaries of games database."),
                        number_of_games_table()
            ])),
            ft.Tab(
                text="Playing time",
                content=ft.Column([
                        ft.Text("Playing time."),
                        total_game_time_table(),
                        the_longest_game_time_table(),
                        the_shortest_game_time_table()
            ])),
            ft.Tab(
                text="Tab 3",
                icon=ft.icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
        ],
        expand=1,
    )
            
            
    def statistics_view():
        if base.exist():
            return ft.Column([
                ft.Text("Statistics View", style="headlineMedium"),
                summaries(),
            ], scroll=ft.ScrollMode.AUTO, expand=True)
        else:
            return ft.Column([
                ft.Text("No database found!")
                ])
        
    # ***************
    # WISHLIST VIEW
    # ***************

    def wishlist_view():
        return ft.Column([
            ft.Text("Wishlist View", style="headlineMedium"),
            ft.Text("Explore different options available."),
            ft.ListView([
                ft.Text("Option 1"),
                ft.Text("Option 2"),
                ft.Text("Option 3"),
            ]),
            ft.Image(src="https://placekitten.com/200/300"),
        ])

    # ***************
    # SETTINGS VIEW
    # ***************

    def settings_view():
        return ft.Column([
            ft.Text("Wishlist View", style="headlineMedium"),
            ft.Text("Explore different options available."),
            ft.ListView([
                ft.Text("Option 1"),
                ft.Text("Option 2"),
                ft.Text("Option 3"),
            ]),
            ft.Image(src="https://placekitten.com/200/300"),
        ])

    # Funkcja obsługująca zmianę zakładki
    def on_tab_change(event, list_begin, list_end):
        if event.control.selected_index == 0:
            page.controls[1].content = manage_database_view(list_begin, list_end)
        elif event.control.selected_index == 1:
            page.controls[1].content = wishlist_view()
        elif event.control.selected_index == 2:
            page.controls[1].content = statistics_view()
        elif event.control.selected_index == 3:
            page.controls[1].content = settings_view()
        page.update()

    def init_navbar(list_begin, list_end):
        page.clean()
        # Tworzymy pasek nawigacji
        nav_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Game list"),
                ft.NavigationBarDestination(icon=ft.icons.BOOKMARK_BORDER, label="Wishlist"),
                ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Statistics"),
                ft.NavigationBarDestination(icon=ft.icons.BOOKMARK_BORDER, selected_icon=ft.icons.BOOKMARK, label="Settings"),
            ],
            on_change=lambda e:on_tab_change(e, list_begin, list_end),
        )

        # Dodajemy pasek nawigacji i początkowy widok
        page.add(nav_bar, ft.Container(content=manage_database_view(list_begin, list_end), expand=True))
        
    init_navbar(list_begin=0, list_end=50)

ft.app(target=main)
