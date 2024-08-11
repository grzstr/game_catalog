import flet as ft
import time
from manage_database import database

def main(page: ft.Page):
    page.title = "Game Catalog"
    base = database()

    #CHECK FUNCTIONS

    def check_time(time):
        return True

    def check_copies(copies):
        try:
            int(copies)
            return True
        except:
            return False

    def check_fields(e, title, copies, time, status, platform, subscription, paid, publisher, developer, series):
        if not (title and copies and time and status and platform and subscription and publisher and paid and developer and series):
            return False
            page.add(ft.Text("Please fill out all fields!", color="red"))   
        else:
            if check_copies(copies):
                if check_time(time):
                    return True
                else:
                    page.add(ft.Text('FIX CHECK TIME FUNCITON XD!', color="red")) 
                    return False
            else:
                page.add(ft.Text('"Copies" are not an integer!', color="red")) 
                return False
        

    # REST OF GUI
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
        
    def add_subscription(e, subscription, platform):
        base.add_subscription(subscription, platform)
        page.update()
        page.add(ft.Text(f'"{subscription}" - added'))      

    def edit_subscriptions(e):
        subscription_field = ft.TextField(label="Enter subscription name")
        platform_field = ft.Dropdown(label="Platform")
        for database_platforms in base.show_platform():
            platform_field.options.append(ft.dropdown.Option(database_platforms[1]))

        page.clean()
        page.add(ft.Row(controls=[subscription_field, platform_field]))
        page.add(ft.Row(controls=[ft.ElevatedButton("Add", on_click=lambda e:add_subscription(e, subscription_field.value, platform_field.value)), ft.OutlinedButton("Back", on_click=add_game_menu)]))
        page.add(ft.Text("Subscriptions:"))
        for subscription in base.show_subscription():
            platform_name = base.get_platform_name(int(subscription[2]))
            page.add(ft.Text(f"{subscription[1]}, {platform_name}"))

    def add_game(e, title, copies, time, status, platform, subscription, paid, publisher, developer, series):
        if check_fields(e, title, copies, time, status, platform, subscription, paid, publisher, developer, series):
            if paid == "No":
                paid = 0
            else:
                paid = 1
            base.add_game(title, copies, time, status, platform, subscription, paid, publisher, developer,  series)
            page.clean()
            main(page)
        page.add(ft.Text("Please fill out all fields!", color="red"))   

    def add_game_menu(e):
        page.clean()
        page.add(ft.Text("Add game view"))
        title_field = ft.TextField(label="Title")
        copies_field = ft.TextField(label="Number of copies")
        time_field = ft.TextField(label="Game time")
        status_field = ft.Dropdown(label="Status", options=[ft.dropdown.Option("Finished"), ft.dropdown.Option("Started"), ft.dropdown.Option("Unstarted")])
        
        platform_field = ft.Dropdown(label="Platform")
        for database_platforms in base.show_platform():
            platform_field.options.append(ft.dropdown.Option(database_platforms[1]))

        subscription_field = ft.Dropdown(label="Subscription")
        for database_subscriptions in base.show_subscription():
            subscription_field.options.append(ft.dropdown.Option(database_subscriptions[1]))
        
        
        
        paid_field = ft.Dropdown(label="Paid", options=[ft.dropdown.Option("Yes"), ft.dropdown.Option("No")])
        publisher_field = ft.TextField(label="Publisher")
        developer_field = ft.TextField(label="Developer")
        series_field = ft.TextField(label="Series")

        add_platform = ft.ElevatedButton("Edit platforms", on_click=edit_platforms)
        add_subscription = ft.ElevatedButton("Edit subscriptions", on_click=edit_subscriptions)


        games_fields = ft.Column([title_field,
                            copies_field,
                            time_field,
                            status_field,
                            #platform_field,
                            #subscription_field,
                            ft.Row(controls=[platform_field, add_platform]),
                            ft.Row(controls=[subscription_field, add_subscription]),
                            paid_field,
                            publisher_field,
                            developer_field, 
                            series_field])

        page.add(games_fields)
        
        add_game_btn = ft.ElevatedButton("Add", 
                                   on_click=lambda e:add_game(e,
                                                     title_field.value, 
                                                     copies_field.value, 
                                                     time_field.value, 
                                                     status_field.value, 
                                                     platform_field.value, 
                                                     subscription_field.value, 
                                                     paid_field.value, 
                                                     publisher_field.value, 
                                                     developer_field.value, 
                                                     series_field.value), 
                                   data=0)
        back_btn = ft.OutlinedButton("Back", on_click=lambda e:main(page))
        page.add(ft.Row(controls=[add_game_btn, back_btn]))

    def delete_game_menu(e):
        page.clean()
        games = ft.Dropdown(label="Games list")
        for game in base.show_games():
            games.options.append(ft.dropdown.Option(game[1]))
        page.add(games)

    def create_database(e):
        base.connect()
        base.create_tables()
        base.configure_tables()
        page.clean()
        main(page)

    def load_database_from_gdrive(e):
        pass

    def paid_status(paid):
        if paid == 1:
            return "Yes"
        elif paid == 0:
            return "No"
        else:
            "Error!"

    def get_games_datatable():
        games_rows = []
        for game in base.show_games():
            games_rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(game[1])),
                ft.DataCell(ft.Text(game[2])),
                ft.DataCell(ft.Text(game[3])),
                ft.DataCell(ft.Text((base.get_status_name(game[4])))),
                ft.DataCell(ft.Text(base.get_platform_name(game[5]))),
                ft.DataCell(ft.Text(base.get_subscription_name(game[6]))),
                ft.DataCell(ft.Text(paid_status(game[7]))),
                ft.DataCell(ft.Text(game[8])),
                ft.DataCell(ft.Text(game[9])),
                ft.DataCell(ft.Text(base.get_series_name(game[10]))),
            ]))
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Title")),
                ft.DataColumn(ft.Text("Copies")),
                ft.DataColumn(ft.Text("Game time")),
                ft.DataColumn(ft.Text("Status")),
                ft.DataColumn(ft.Text("Platform")),
                ft.DataColumn(ft.Text("Subscription")),
                ft.DataColumn(ft.Text("Paid")),
                ft.DataColumn(ft.Text("Publisher")),
                ft.DataColumn(ft.Text("Developer")),
                ft.DataColumn(ft.Text("Serie"))
            ],
            rows = games_rows
        )
        


    ### NAVIGATION MENU

    def manage_database_view():
        if base.exist():
            if base.show_games() != []:
                games_datatable = get_games_datatable()
                return ft.Column([
                    ft.ElevatedButton("Add game", on_click=add_game_menu, data=0),
                    ft.ElevatedButton("Delete game", on_click=delete_game_menu, data=0),
                    games_datatable
                    ])
            else:
                return ft.Column([
                    ft.ElevatedButton("Add game", on_click=add_game_menu, data=0),
                    ft.ElevatedButton("Delete game", on_click=delete_game_menu, data=0)
                    ])
        else:
            return ft.Column([
                ft.Text("No database found!"),
                ft.ElevatedButton("Create a new database", on_click=create_database, data=0),
                ft.ElevatedButton("Load database from Google Drive", on_click=add_game_menu, data=0)
                ])
    def statistics_view():
        if base.exist():
            return ft.Column([
                ft.Text("Statistics View", style="headlineMedium"),
                ft.Text("This section shows the statistics."),
                ft.Text("Summary of statistics goes here."),
            ])
        else:
            return ft.Column([
                ft.Text("No database found!")
                ])
        
    def explore_view():
        return ft.Column([
            ft.Text("Explore View", style="headlineMedium"),
            ft.Text("Explore different options available."),
            ft.ListView([
                ft.Text("Option 1"),
                ft.Text("Option 2"),
                ft.Text("Option 3"),
            ]),
            ft.Image(src="https://placekitten.com/200/300"),
        ])

    # Funkcja obsługująca zmianę zakładki
    def on_tab_change(event):
        if event.control.selected_index == 0:
            page.controls[1].content = manage_database_view()
        elif event.control.selected_index == 1:
            page.controls[1].content = statistics_view()
        elif event.control.selected_index == 2:
            page.controls[1].content = explore_view()
        page.update()

    page.clean()
    # Tworzymy pasek nawigacji
    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Manage Database"),
            ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Statistics"),
            ft.NavigationBarDestination(icon=ft.icons.BOOKMARK_BORDER, selected_icon=ft.icons.BOOKMARK, label="Explore"),
        ],
        on_change=on_tab_change,
    )

    # Dodajemy pasek nawigacji i początkowy widok
    page.add(nav_bar, ft.Container(content=manage_database_view()))

ft.app(target=main)
