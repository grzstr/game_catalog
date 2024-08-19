import flet as ft
import time
from stats import games_stats

def main(page: ft.Page):
    page.title = "Game Catalog"
    stats = games_stats()
    base = stats.base

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

    def check_fields(e, title, copies, time, status, platform, games_store, subscription, box, paid, publisher, developer, series):
        if not (title and copies and time and status and platform and games_store and subscription and publisher and box and paid and developer and series):
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
    def add_series(e, series, dlg_modal, series_field):
        if isinstance(series, str):
            base.add_series(series)
            series_field.options.append(ft.dropdown.Option(series))
            page.close(dlg_modal)
            page.update()
        else:
            dlg_modal.content.append(ft.Text("It is not a STRING!"))

    def edit_series(e, series_field):
        text = ""
        text += "Series:\n"
        for series in base.show_series():
            if series[1] != "":
                text+=f"{series[1]}\n"
        enter_series_field = ft.TextField(label="Enter serie name")
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add serie"),
            content=ft.Column([enter_series_field, ft.Text(text)]),
            actions=[
                ft.Row(controls=[ft.TextButton("Add", on_click=lambda e:add_series(e, enter_series_field.value, dlg_modal, series_field)), ft.TextButton("Back", on_click=lambda e:page.close(dlg_modal))]),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg_modal)

    def delete_series(e, series_field):
        for i in range(len(series_field.options)):
            if series_field.options[i].key == series_field.value:
                series_field.options.pop(i)
                break

        base.delete_series(series_field.value)
        page.update()  

    def add_games_store(e, games_store, dlg_modal, games_store_field):
        if isinstance(games_store, str):
            base.add_games_store(games_store)
            games_store_field.options.append(ft.dropdown.Option(games_store))
            page.close(dlg_modal)
            page.update()
        else:
            dlg_modal.content.append(ft.Text("It is not a STRING!"))

    def edit_games_stores(e, games_store_field):
        text = ""
        text += "Game stores:\n"
        for games_store in base.show_games_store():
            if games_store[1] != "":
                text+=f"{games_store[1]}\n"
        enter_games_store_field = ft.TextField(label="Enter games store name")
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add games store"),
            content=ft.Column([enter_games_store_field, ft.Text(text)]),
            actions=[
                ft.Row(controls=[ft.TextButton("Add", on_click=lambda e:add_games_store(e, enter_games_store_field.value, dlg_modal, games_store_field)), ft.TextButton("Back", on_click=lambda e:page.close(dlg_modal))]),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg_modal)

    def delete_games_store(e, games_store_field):
        for i in range(len(games_store_field.options)):
            if games_store_field.options[i].key == games_store_field.value:
                games_store_field.options.pop(i)
                break

        base.delete_games_store(games_store_field.value)
        page.update()  

    def add_platform(e, platform, dlg_modal, platform_field):
        if isinstance(platform, str):
            base.add_platform(platform)
            platform_field.options.append(ft.dropdown.Option(platform))
            page.close(dlg_modal)
            page.update()
        else:
            dlg_modal.content.append(ft.Text("It is not a STRING!"))

    def edit_platform(e, platform_field):
        text = ""
        text += "Platforms:\n"
        for platform in base.show_platform():
            if platform[1] != "":
                text+=f"{platform[1]}\n"
        enter_platform_field = ft.TextField(label="Enter platform name")
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add platform"),
            content=ft.Column([enter_platform_field, ft.Text(text)]),
            actions=[
                ft.Row(controls=[ft.TextButton("Add", on_click=lambda e:add_platform(e, enter_platform_field.value, dlg_modal, platform_field)), ft.TextButton("Back", on_click=lambda e:page.close(dlg_modal))]),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg_modal)

    def delete_platform(e, platform_field):
        for i in range(len(platform_field.options)):
            if platform_field.options[i].key == platform_field.value:
                platform_field.options.pop(i)
                break

        base.delete_platform(platform_field.value)
        page.update()  

    def add_publisher(e, publisher, dlg_modal, publisher_field):
        if isinstance(publisher, str):
            base.add_publisher(publisher)
            publisher_field.options.append(ft.dropdown.Option(publisher))
            page.close(dlg_modal)
            page.update()
        else:
            dlg_modal.content.append(ft.Text("It is not a STRING!"))

    def edit_publisher(e, publisher_field):
        text = ""
        text += "Publishers:\n"
        for publisher in base.show_publisher():
            if publisher[1] != "":
                text+=f"{publisher[1]}\n"
        enter_publisher_field = ft.TextField(label="Enter publisher name")
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add publisher"),
            content=ft.Column([enter_publisher_field, ft.Text(text)]),
            actions=[
                ft.Row(controls=[ft.TextButton("Add", on_click=lambda e:add_publisher(e, enter_publisher_field.value, dlg_modal, publisher_field)), ft.TextButton("Back", on_click=lambda e:page.close(dlg_modal))]),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg_modal)

    def delete_publisher(e, publisher_field):
        for i in range(len(publisher_field.options)):
            if publisher_field.options[i].key == publisher_field.value:
                publisher_field.options.pop(i)
                break

        base.delete_publisher(publisher_field.value)
        page.update()  

    def add_developer(e, developer, dlg_modal, developer_field):
        if isinstance(developer, str):
            base.add_developer(developer)
            developer_field.options.append(ft.dropdown.Option(developer))
            page.close(dlg_modal)
            page.update()
        else:
            dlg_modal.content.append(ft.Text("It is not a STRING!"))

    def edit_developer(e, developer_field):
        text = ""
        text += "Developers:\n"
        for developer in base.show_developer():
            if developer[1] != "":
                text+=f"{developer[1]}\n"
        enter_developer_field = ft.TextField(label="Enter developer name")
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add developer"),
            content=ft.Column([enter_developer_field, ft.Text(text)]),
            actions=[
                ft.Row(controls=[ft.TextButton("Add", on_click=lambda e:add_developer(e, enter_developer_field.value, dlg_modal, developer_field)), ft.TextButton("Back", on_click=lambda e:page.close(dlg_modal))]),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg_modal)

    def delete_developer(e, developer_field):
        for i in range(len(developer_field.options)):
            if developer_field.options[i].key == developer_field.value:
                developer_field.options.pop(i)
                break

        base.delete_developer(developer_field.value)
        page.update()  


    def add_subscription(e, subscription, games_store, subscription_field, dlg_modal):
        if isinstance(subscription, str) and isinstance(games_store, str):
            base.add_subscription(subscription, games_store)
            subscription_field.options.append(ft.dropdown.Option(subscription))
            
            page.close(dlg_modal)
            page.update()
        else:
            dlg_modal.content.append(ft.Text("It is not a STRING!"))

    def delete_subscription(e, subscription_field):
        for i in range(len(subscription_field.options)):
            if subscription_field.options[i].key == subscription_field.value:
                subscription_field.options.pop(i)
                break

        base.delete_subscription(subscription_field.value)
        page.update()  

    def edit_subscriptions(e, subscription_dropdown):
        subscription_field = ft.TextField(label="Enter subscription name")
        games_store_field = ft.Dropdown(label="Games store")
        for database_games_stores in base.show_games_store():
            games_store_field.options.append(ft.dropdown.Option(database_games_stores[1]))
        games_store_field.value = games_store_field.options[0].key

        text = ""
        text += "Subscriptions:\n"
        for subscription in base.show_subscription():
            games_store_name = base.get_games_store_name(int(subscription[2]))
            text+=f"{subscription[1]} - {games_store_name}\n"

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add subscription"),
            content=ft.Column([subscription_field, games_store_field, ft.Text(text)]),
            actions=[
                ft.Row(controls=[ft.TextButton("Add", on_click=lambda e:add_subscription(e, subscription_field.value, games_store_field.value, subscription_dropdown, dlg_modal)), ft.TextButton("Back", on_click=lambda e:page.close(dlg_modal))]),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape = ft.RoundedRectangleBorder(radius=50)
        )
        page.open(dlg_modal)

    def add_game(e, title, copies, time, status, platform, games_store, subscription, box, paid, publisher, developer, series):
        if check_fields(e, title, copies, time, status, platform, games_store, subscription, box, paid, publisher, developer, series):
            if paid == "No":
                paid = 0
            else:
                paid = 1
            if box == "No":
                box = 0
            else:
                box = 1
            base.add_game(title, copies, time, status, platform, games_store, subscription, box, paid, publisher, developer, series)
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
        for database_platform in base.show_platform():
            if database_platform[1] != "" and isinstance(database_platform[1], str):
                platform_field.options.append(ft.dropdown.Option(database_platform[1]))
        platform_field.value = platform_field.options[0].key

        games_store_field = ft.Dropdown(label="Games store")
        for database_games_stores in base.show_games_store():
            if database_games_stores[1] != "" and isinstance(database_games_stores[1], str):
                games_store_field.options.append(ft.dropdown.Option(database_games_stores[1]))
        games_store_field.value = games_store_field.options[0].key

        subscription_field = ft.Dropdown(label="Subscription")
        for database_subscriptions in base.show_subscription():
            if database_subscriptions[1] != "" and isinstance(database_subscriptions[1], str):
                subscription_field.options.append(ft.dropdown.Option(database_subscriptions[1]))
        subscription_field.value = subscription_field.options[0].key

        box_field = ft.Dropdown(label="Box", options=[ft.dropdown.Option("Yes"), ft.dropdown.Option("No")])
        box_field.value = box_field.options[0].key

        paid_field = ft.Dropdown(label="Paid", options=[ft.dropdown.Option("Yes"), ft.dropdown.Option("No")])
        paid_field.value = paid_field.options[0].key

        developer_field = ft.Dropdown(label="Developer")
        for database_developer in base.show_developer():
            if database_developer[1] != "" and isinstance(database_developer[1], str):
                developer_field.options.append(ft.dropdown.Option(database_developer[1]))

        publisher_field = ft.Dropdown(label="Publisher")
        for database_publishers in base.show_publisher():
            if database_publishers[1] != "" and isinstance(database_publishers[1], str):
                publisher_field.options.append(ft.dropdown.Option(database_publishers[1]))

        series_field = ft.Dropdown(label="Series")
        for database_series in base.show_series():
            if database_series[1] != "" and isinstance(database_series[1], str):
                series_field.options.append(ft.dropdown.Option(database_series[1]))
        
        add_platform = ft.ElevatedButton("Edit platform", on_click=lambda e:edit_platform(e, platform_field))
        add_games_store = ft.ElevatedButton("Edit games stores", on_click=lambda e:edit_games_stores(e, games_store_field))
        add_subscription = ft.ElevatedButton("Edit subscriptions", on_click=lambda e:edit_subscriptions(e, subscription_field))
        add_series = ft.ElevatedButton("Edit series", on_click=lambda e:edit_series(e, series_field))
        add_publisher = ft.ElevatedButton("Edit publishers", on_click=lambda e:edit_publisher(e, publisher_field))
        add_developer = ft.ElevatedButton("Edit developers", on_click=lambda e:edit_developer(e, developer_field))

        delete_platform_btn = ft.ElevatedButton("Delete platform", on_click=lambda e:delete_platform(e, platform_field)) 
        delete_games_store_btn = ft.ElevatedButton("Delete games store", on_click=lambda e:delete_games_store(e, games_store_field)) 
        delete_series_btn = ft.ElevatedButton("Delete serie", on_click=lambda e:delete_series(e, series_field)) 
        delete_developer_btn = ft.ElevatedButton("Delete developer", on_click=lambda e:delete_developer(e, developer_field))
        delete_subscription_btn = ft.ElevatedButton("Delete subscription", on_click=lambda e:delete_subscription(e, subscription_field))
        delete_publisher_btn = ft.ElevatedButton("Delete publisher", on_click=lambda e:delete_publisher(e, publisher_field)) 

        page.add(ft.Column([title_field,
                            copies_field,
                            ft.Row(controls=[time_hours_field, ft.Text(":"), time_minutes_field, ft.Text(":"), time_seconds_field]),
                            status_field,
                            ft.Row(controls=[platform_field, add_platform, delete_platform_btn]),
                            ft.Row(controls=[games_store_field, add_games_store, delete_games_store_btn]),
                            ft.Row(controls=[subscription_field, add_subscription, delete_subscription_btn]),
                            box_field,
                            paid_field,
                            ft.Row(controls=[publisher_field, add_publisher, delete_publisher_btn]),
                            ft.Row(controls=[developer_field, add_developer, delete_developer_btn]),
                            ft.Row(controls=[series_field, add_series, delete_series_btn])], scroll=ft.ScrollMode.AUTO, expand=True))
        
        add_game_btn = ft.ElevatedButton("Add", 
                                   on_click=lambda e:add_game(e,
                                                     title_field.value, 
                                                     copies_field.value, 
                                                     f"{time_hours_field.value}:{time_minutes_field.value}:{time_seconds_field.value}", 
                                                     status_field.value, 
                                                     platform_field.value,
                                                     games_store_field.value, 
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

    def modify_game(e, id, title, copies, time, status, platform, games_store, subscription, box, paid, publisher, developer, series):
        if check_fields(e, title, copies, time, status, platform, games_store, subscription, box, paid, publisher, developer, series):
            if paid == "No":
                paid = 0
            else:
                paid = 1
            if box == "No":
                box = 0
            else:
                box = 1
            base.modify_game(id, title, copies, time, status, platform, games_store, subscription, box, paid, publisher, developer,  series)
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
        for database_platform in base.show_platform():
            platform_field.options.append(ft.dropdown.Option(database_platform[1]))
        platform_field.value = base.get_platform_name(game[5])


        games_store_field = ft.Dropdown(label="Games store")
        for database_games_stores in base.show_games_store():
            games_store_field.options.append(ft.dropdown.Option(database_games_stores[1]))
        games_store_field.value = base.get_games_store_name(game[6])

        subscription_field = ft.Dropdown(label="Subscription")
        for database_subscriptions in base.show_subscription():
            subscription_field.options.append(ft.dropdown.Option(database_subscriptions[1]))
        subscription_field.value = base.get_subscription_name(game[7])

        box_field = ft.Dropdown(label="Box", options=[ft.dropdown.Option("Yes"), ft.dropdown.Option("No")])
        box_field.value = box_status(game[8])
        
        paid_field = ft.Dropdown(label="Paid", options=[ft.dropdown.Option("Yes"), ft.dropdown.Option("No")])
        paid_field.value = paid_status(game[9])

        publisher_field = ft.Dropdown(label="Publisher")
        for database_publishers in base.show_publisher():
            publisher_field.options.append(ft.dropdown.Option(database_publishers[1]))
        publisher_field.value = base.get_publisher_name(game[10])


        developer_field = ft.Dropdown(label="Developer")
        for database_developer in base.show_developer():
            developer_field.options.append(ft.dropdown.Option(database_developer[1]))
        developer_field.value = base.get_developer_name(game[11])

        series_field = ft.Dropdown(label="Series")
        for database_series in base.show_series():
            series_field.options.append(ft.dropdown.Option(database_series[1]))
        series_field.value = base.get_series_name(game[12])
        
        add_platform = ft.ElevatedButton("Edit platform", on_click=lambda e:edit_platform(e, platform_field))
        add_games_store = ft.ElevatedButton("Edit games stores", on_click=lambda e:edit_games_stores(e, games_store_field))
        add_subscription = ft.ElevatedButton("Edit subscriptions", on_click=lambda e:edit_subscriptions(e, subscription_field))
        add_series = ft.ElevatedButton("Edit series", on_click=lambda e:edit_series(e, series_field))
        add_publisher = ft.ElevatedButton("Edit publishers", on_click=lambda e:edit_publisher(e, publisher_field))
        add_developer = ft.ElevatedButton("Edit developers", on_click=lambda e:edit_developer(e, developer_field))

        delete_platform_btn = ft.ElevatedButton("Delete platform", on_click=lambda e:delete_platform(e, platform_field)) 
        delete_games_store_btn = ft.ElevatedButton("Delete games store", on_click=lambda e:delete_games_store(e, games_store_field)) 
        delete_series_btn = ft.ElevatedButton("Delete serie", on_click=lambda e:delete_series(e, series_field)) 
        delete_developer_btn = ft.ElevatedButton("Delete developer", on_click=lambda e:delete_developer(e, developer_field))
        delete_subscription_btn = ft.ElevatedButton("Delete subscription", on_click=lambda e:delete_subscription(e, subscription_field))
        delete_publisher_btn = ft.ElevatedButton("Delete publisher", on_click=lambda e:delete_publisher(e, publisher_field)) 

        games_fields = ft.Column([title_field,
                            copies_field,
                            ft.Row(controls=[time_hours_field, ft.Text(":"), time_minutes_field, ft.Text(":"), time_seconds_field]),
                            status_field,
                            ft.Row(controls=[platform_field, add_platform, delete_platform_btn]),
                            ft.Row(controls=[games_store_field, add_games_store, delete_games_store_btn]),
                            ft.Row(controls=[subscription_field, add_subscription, delete_subscription_btn]),
                            box_field,
                            paid_field,
                            ft.Row(controls=[publisher_field, add_publisher, delete_publisher_btn]),
                            ft.Row(controls=[developer_field, add_developer, delete_developer_btn]),
                            ft.Row(controls=[series_field, add_series, delete_series_btn])], scroll=ft.ScrollMode.AUTO, expand=True)

        page.add(games_fields)
        
        modify_game_btn = ft.ElevatedButton("Modify", 
                                   on_click=lambda e:modify_game(e,
                                                     int(game[0]),
                                                     title_field.value, 
                                                     copies_field.value, 
                                                     f"{time_hours_field.value}:{time_minutes_field.value}:{time_seconds_field.value}", 
                                                     status_field.value, 
                                                     platform_field.value,
                                                     games_store_field.value, 
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

    def get_games_datatable(begin = 0, end = -1, find = None, filters = None):
        games_rows = []
        
        games_list = base.show_games(find, filters)


        if end == -1 and begin == 0:
            list_range = games_list
        else:
            list_range = games_list[begin:end]

        for game in list_range:
            cell_tab = []
            cell_tab.append(ft.DataCell(ft.Text(game[0])))
            cell_tab.append(ft.DataCell(ft.Text(game[1])))
            cell_tab.append(ft.DataCell(ft.Text(game[2])))
            cell_tab.append(ft.DataCell(ft.Text(game[3])))
            cell_tab.append(ft.DataCell(ft.Text(base.get_status_name(game[4]))))
            cell_tab.append(ft.DataCell(ft.Text(base.get_platform_name(game[5]))))
            cell_tab.append(ft.DataCell(ft.Text(base.get_games_store_name(game[6]))))
            cell_tab.append(ft.DataCell(ft.Text(base.get_subscription_name(game[7]))))
            cell_tab.append(ft.DataCell(ft.Text(box_status(game[8]))))
            cell_tab.append(ft.DataCell(ft.Text(paid_status(game[9]))))
            cell_tab.append(ft.DataCell(ft.Text(base.get_publisher_name(game[10]))))
            cell_tab.append(ft.DataCell(ft.Text(base.get_developer_name(game[11]))))
            cell_tab.append(ft.DataCell(ft.Text(base.get_series_name(game[12]))))
            games_rows.append(ft.DataRow(cells=cell_tab, color=set_color(game[4])))
        games_columns = []
        games_columns.append(ft.DataColumn(ft.Text("ID")))
        games_columns.append(ft.DataColumn(ft.Text("Title")))
        games_columns.append(ft.DataColumn(ft.Text("Copies")))
        games_columns.append(ft.DataColumn(ft.Text("Game time (H:M:S)")))
        games_columns.append(ft.DataColumn(ft.Text("Status")))
        games_columns.append(ft.DataColumn(ft.Text("Platform")))
        games_columns.append(ft.DataColumn(ft.Text("Games store")))
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

    def find_game(e, title, dlg_modal):
        page.close(dlg_modal)
        init_navbar(0, -1, title)


    def find_menu(e):
        search_field = ft.TextField(label="Enter game title")
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Find game"),
            content=ft.Column([search_field]),
            actions=[
                ft.Row(controls=[ft.TextButton("Find", on_click=lambda e:find_game(e, search_field.value, dlg_modal)), ft.TextButton("Back", on_click=lambda e:page.close(dlg_modal))]),
            ],
            actions_alignment=ft.MainAxisAlignment.START,
        )
        page.open(dlg_modal)

    def update_dropdown(e, filter_field, chosen_filter_field):
        options = []
        if filter_field.value == 'Status':
            options = ['Finished', 'Started', 'Not started']
        elif filter_field.value == 'Platform':
            for option in base.show_platform():
                options.append(option[1]) 
        elif filter_field.value == 'Games store':
            for option in base.show_games_store():
                options.append(option[1]) 
        elif filter_field.value == 'Subscription':
            for option in base.show_subscription():
                options.append(option[1]) 
        elif filter_field.value == 'Box':
            options = ['Yes', 'No']
        elif filter_field.value == 'Paid':
            options = ['Yes', 'No']
        elif filter_field.value == 'Publisher':
            for option in base.show_publisher():
                options.append(option[1]) 
        elif filter_field.value == 'Developer':
            for option in base.show_developer():
                options.append(option[1]) 
        elif filter_field.value == 'Series':
            for option in base.show_series():
                options.append(option[1]) 
        else:
            options = []

        chosen_filter_field.options.clear()
        for option in options:
            chosen_filter_field.options.append(ft.dropdown.Option(option))

        page.update(filter_field)
        page.update(chosen_filter_field)

    def set_sort(dlg_modal, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12):
        filters = ""
        if c1.value == True:
            if filters != "":
                filters += ","
            filters += "number_of_copies "
        if c2.value == True:
            if filters != "":
                filters += ","
            filters += "game_time "
        if c3.value == True:
            if filters != "":
                filters += ","
            filters += "status_id "
        if c4.value == True:
            if filters != "":
                filters += ","
            filters += "platform_id "
        if c5.value == True:
            if filters != "":
                filters += ","
            filters += "games_store_id "
        if c6.value == True:
            if filters != "":
                filters += ","
            filters += "subscription_id "
        if c7.value == True:
            if filters != "":
                filters += ","
            filters += "box "
        if c8.value == True:
            if filters != "":
                filters += ","
            filters += "paid "
        if c9.value == True:
            if filters != "":
                filters += ","
            filters += "publisher_id "
        if c10.value == True:
            if filters != "":
                filters += ","
            filters += "developer_id "
        if c11.value == True:
            if filters != "":
                filters += ","
            filters += "series_id "
        if c12.value == True:
            if filters != "":
                filters += ","
            filters += "title "

        page.close(dlg_modal)
        init_navbar(0, -1, None, filters)

    def set_show(dlg_modal, filter, chosen_filter):
        if filter == "Status":
            filters = f"status_id = {base.get_status_id(chosen_filter)}"
        elif filter == "Platform":
            filters = f"platform_id = {base.get_platform_id(chosen_filter)}"
        elif filter == "Games store":
            filters = f"games_store_id = {base.get_games_store_id(chosen_filter)}"
        elif filter == "Subscription":
            filters = f"subscription_id = {base.get_subscription_id(chosen_filter)}"
        elif filter == "Box":
            filters = f"box = {base.convert_yes_no(chosen_filter)}"
        elif filter == "Paid":
            filters = f"paid = {base.convert_yes_no(chosen_filter)}"
        elif filter == "Publisher":
            filters = f"publisher_id = {base.get_publisher_id(chosen_filter)}"
        elif filter == "Developer":
            filters = f"developer_id = {base.get_developer_id(chosen_filter)}"
        elif filter == "Series":
            filters = f"series_id = {base.get_series_id(chosen_filter)}"
        page.close(dlg_modal)
        init_navbar(0, -1, None, filters)

    def filter_menu(e):
        c12 = ft.Checkbox(label="Title", value=False)
        c1 = ft.Checkbox(label="Number of copies", value=False)
        c2 = ft.Checkbox(label="Game time", value=False)
        c3 = ft.Checkbox(label="Status", value=False)
        c4 = ft.Checkbox(label="Platform", value=False)
        c5 = ft.Checkbox(label="Games store", value=False)
        c6 = ft.Checkbox(label="Subscription", value=False)
        c7 = ft.Checkbox(label="Box", value=False)
        c8 = ft.Checkbox(label="Paid", value=False)
        c9 = ft.Checkbox(label="Publisher", value=False)
        c10 = ft.Checkbox(label="Developer", value=False)
        c11 = ft.Checkbox(label="Series", value=False)

        chosen_filter_field = ft.Dropdown(label="Choose:")
        filter_field = ft.Dropdown(label="Choose atribute:", on_change=lambda e:update_dropdown(e, filter_field, chosen_filter_field))
        for filter in ['Status', 'Platform', 'Games store', 'Subscription', 'Box', 'Paid', 'Publisher', 'Developer', 'Series']:
            filter_field.options.append(ft.dropdown.Option(filter))
        

        check = ft.Column([])
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("List filters"),
            content=ft.Tabs(
                    selected_index=0,
                    animation_duration=300,
                    tabs=[
                        ft.Tab(
                            text="Sort by",
                            content=ft.Column([c12, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11,
                                               ft.Row(controls=[ft.TextButton("Set filters", on_click=lambda e:set_sort(dlg_modal, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12)), 
                                                                ft.TextButton("Back", on_click=lambda e:page.close(dlg_modal))])])),

                        ft.Tab(
                            text="Show only",
                            content=ft.Column([filter_field, 
                                               chosen_filter_field,
                                               ft.Row(controls=[ft.TextButton("Set filters", on_click=lambda e:set_show(dlg_modal, filter_field.value, chosen_filter_field.value)), 
                                                                ft.TextButton("Back", on_click=lambda e:page.close(dlg_modal))])])),
                    ],
                    expand=True,
                    scrollable=True,
                ),
            scrollable=True,
            actions_alignment=ft.MainAxisAlignment.START,
        )
        page.open(dlg_modal)

    def set_wishlist_sort(dlg_modal, c4, c9, c10, c12):
        filters = ""
        if c4.value == True:
            if filters != "":
                filters += ","
            filters += "platform_id "
        if c9.value == True:
            if filters != "":
                filters += ","
            filters += "publisher_id "
        if c10.value == True:
            if filters != "":
                filters += ","
            filters += "developer_id "
        if c12.value == True:
            if filters != "":
                filters += ","
            filters += "title "

        page.close(dlg_modal)
        init_navbar(0, -1, None, filters)

    def set_wishlist_show(dlg_modal, filter, chosen_filter):
        if filter == "Platform":
            filters = f"platform_id = {base.get_platform_id(chosen_filter)}"
        elif filter == "Publisher":
            filters = f"publisher_id = {base.get_publisher_id(chosen_filter)}"
        elif filter == "Developer":
            filters = f"developer_id = {base.get_developer_id(chosen_filter)}"
        page.close(dlg_modal)
        init_navbar(0, -1, None, filters)

    def filter_wishlist_menu(e):
        c12 = ft.Checkbox(label="Title", value=False)
        c4 = ft.Checkbox(label="Platform", value=False)
        c9 = ft.Checkbox(label="Publisher", value=False)
        c10 = ft.Checkbox(label="Developer", value=False)

        chosen_filter_field = ft.Dropdown(label="Choose:")
        filter_field = ft.Dropdown(label="Choose atribute:", on_change=lambda e:update_dropdown(e, filter_field, chosen_filter_field))
        for filter in ['Platform', 'Publisher', 'Developer']:
            filter_field.options.append(ft.dropdown.Option(filter))
        

        check = ft.Column([])
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("List filters"),
            content=ft.Tabs(
                    selected_index=0,
                    animation_duration=300,
                    tabs=[
                        ft.Tab(
                            text="Sort by",
                            content=ft.Column([c12, c4, c9, c10,
                                               ft.Row(controls=[ft.TextButton("Set filters", on_click=lambda e:set_wishlist_sort(dlg_modal, c4, c9, c10, c12)), 
                                                                ft.TextButton("Back", on_click=lambda e:page.close(dlg_modal))])])),

                        ft.Tab(
                            text="Show only",
                            content=ft.Column([filter_field, 
                                               chosen_filter_field,
                                               ft.Row(controls=[ft.TextButton("Set filters", on_click=lambda e:set_wishlist_show(dlg_modal, filter_field.value, chosen_filter_field.value)), 
                                                                ft.TextButton("Back", on_click=lambda e:page.close(dlg_modal))])])),
                    ],
                    expand=True,
                    scrollable=True,
                ),
            scrollable=True,
            actions_alignment=ft.MainAxisAlignment.START,
        )
        page.open(dlg_modal)


    ### NAVIGATION MENU

    def manage_database_view(list_begin, list_end, find, filters):
        if base.exist():
            if base.show_games() != []:
                if find==None:
                    search_btn = ft.ElevatedButton("Search", on_click=find_menu, data=0)
                else:
                    search_btn = ft.OutlinedButton(f"Searched - '{find}'", on_click=lambda e:init_navbar(0, -1, None, filters), data=0)
                if filters == None:
                    filters_btn = ft.ElevatedButton("Filters", on_click=filter_menu, data=0)
                else:
                    filters_btn = ft.OutlinedButton(f"Filtered - '{filters}'", on_click=lambda e:init_navbar(0, -1, find, None), data=0)

                if list_begin == 0 and list_end == len(base.show_games()):
                    show_all = ft.OutlinedButton("Show less", on_click=lambda e:init_navbar(0, 50), data=0)
                else:
                    show_all = ft.ElevatedButton("Show all", on_click=lambda e:init_navbar(0, len(base.show_games())), data=0)
                return ft.Column([
                    ft.Text("Game list", style="headlineMedium"),
                    ft.Row(controls=[ft.ElevatedButton("Add game", on_click=add_game_menu, data=0),
                                     ft.ElevatedButton("Edit game list", on_click=edit_game_menu, data=0)]),
                    ft.Row(controls=[search_btn,
                                     filters_btn]),
                    ft.Row(controls=[ft.ElevatedButton("<", on_click=lambda e:move_left_game_list(list_begin, list_end), data=0),
                                     ft.Text(f"{list_begin} - {list_end}"),
                                     ft.ElevatedButton(">", on_click=lambda e:move_right_game_list(list_begin, list_end), data=0),
                                     show_all]),
                    ft.Divider(),
                    get_games_datatable(list_begin, list_end, find, filters),
                    ft.Divider()
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
                        ft.DataCell(ft.Text("Total")),
                        ft.DataCell(ft.Text(str(len(base.show_games()))))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Owned")),
                        ft.DataCell(ft.Text(str(len(base.show_owned_games()))))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Subscripted")),
                        ft.DataCell(ft.Text(str(len(base.show_subscription_games()))))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Purchased")),
                        ft.DataCell(ft.Text(str(len(base.show_purchased_games()))))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Free")),
                        ft.DataCell(ft.Text(str(len(base.show_free_games()))))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Box")),
                        ft.DataCell(ft.Text(str(len(base.show_box_games()))))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Digital")),
                        ft.DataCell(ft.Text(str(len(base.show_digital_games()))))
                    ]
                ),
            ]

            )

    def sort_games_stores(games_by_games_store):
        games_stores = base.show_games_store()
        games_store_dict = {}
        for games_store in games_stores:
            if len(games_store[1])>1 and games_store[1] != "Other" and games_store[1] != "None":
                if games_store[1] not in games_store_dict and "/" not in games_store[1]:
                    games_store_dict[games_store[1]] = len(games_by_games_store(games_store[1]))
                else:
                    games_store_list = games_store[1].split("/")
                    for splited_games_store in games_store_list:
                        if splited_games_store not in games_store_dict:
                            games_store_dict[splited_games_store] = len(games_by_games_store(games_store[1]))
                        else:
                            games_store_dict[splited_games_store] += len(games_by_games_store(games_store[1]))

        return games_store_dict

    def games_store_plot():
        bar_groups = []
        labels = []

        purchased_games = sort_games_stores(base.show_purchased_games_by_games_store)
        free_games = sort_games_stores(base.show_free_games_by_games_store)

        i = 0
        for games_store in purchased_games:
            bar_groups.append(ft.BarChartGroup(x=i, bar_rods=[ft.BarChartRod(from_y=0,to_y=purchased_games[games_store],color="blue"),
                                                                          ft.BarChartRod(from_y=0,to_y=free_games[games_store],color="red")]))
            store = games_store.split(" ")
            label_store = ""
            for word in store:
                label_store+= word + "\n" 
            labels.append(ft.ChartAxisLabel(value=i, label=ft.Container(ft.Text(label_store, text_align=ft.TextAlign.CENTER), padding=1)))
            i+=1

        return ft.BarChart(
            bar_groups= bar_groups,
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels_size=40, title=ft.Text("Value"), title_size=40
            ),
            bottom_axis=ft.ChartAxis(labels = labels, labels_size=80, title=ft.Text("Games stores")),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
            max_y=110,
            min_y=0,
            interactive=True,
            expand=False,
        )
       

    def total_game_time_table():
        years, days, hours, minutes, seconds = stats.total_playing_time()
        return ft.DataTable(columns=[
                ft.DataColumn(ft.Text("Total playing time:")),
                ft.DataColumn(ft.Text("Value:"))
            ],
            rows =[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Years:")),
                        ft.DataCell(ft.Text(f"{int(years)}"))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Days:")),
                        ft.DataCell(ft.Text(f"{int(days)}"))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Hours:")),
                        ft.DataCell(ft.Text(f"{int(hours)}"))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Minutes:")),
                        ft.DataCell(ft.Text(f"{int(minutes)}"))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Seconds:")),
                        ft.DataCell(ft.Text(f"{int(seconds)}"))
                    ]
                ),
            ]
            )    

    def number_of_started_games_table():
        return ft.DataTable(columns=[
                ft.DataColumn(ft.Text("Numer of games:")),
                ft.DataColumn(ft.Text("Value:"))
            ],
            rows =[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Started:")),
                        ft.DataCell(ft.Text(""))
                    ], 
                    color="orange"
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Not Started:")),
                        ft.DataCell(ft.Text(""))
                    ],
                    color="red"
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Finished:")),
                        ft.DataCell(ft.Text(""))
                    ],
                    color="green"
                ),
            ]
            )  

    def the_longest_game_time_table():
        time, index = stats.the_longest_playing_time()
        games = base.show_games()
        return ft.DataTable(columns=[
                ft.DataColumn(ft.Text("The longest playing time:")),
                ft.DataColumn(ft.Text("Value:"))
            ],
            rows =[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Playing time:")),
                        ft.DataCell(ft.Text(time))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Title:")),
                        ft.DataCell(ft.Text(games[index][1]))
                    ]
                )
            ]
            )          

    def the_shortest_game_time_table():
        time, index = stats.the_shortest_playing_time()
        games = base.show_games()
        return ft.DataTable(columns=[
                ft.DataColumn(ft.Text("The shortest playing time:")),
                ft.DataColumn(ft.Text("Value:"))
            ],
            rows =[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Playing time:")),
                        ft.DataCell(ft.Text(time))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Title:")),
                        ft.DataCell(ft.Text(games[index][1]))
                    ]
                )
            ]
            )     

    def statistics_tabs():          
            return ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
            ft.Tab(
                text="Summaries",
                content=ft.Column([
                        ft.Text(""),
                        ft.Text("Summaries of games database."),
                        ft.Row(controls=[number_of_games_table(), ft.VerticalDivider(), number_of_started_games_table()]),
                        ft.Divider(),
                        games_store_plot(),
                        ft.Divider()
            ])),
            ft.Tab(
                text="Playing time",
                content=ft.Column([
                        ft.Text("Playing time."),
                        ft.Divider(),
                        total_game_time_table(),
                        ft.Divider(),
                        the_longest_game_time_table(),
                        ft.Divider(),
                        the_shortest_game_time_table(),
                        ft.Divider()
            ])),
            ft.Tab(
                text="Percentage of games",
                content=ft.Column([
                        ft.Text("Playing time."),
                        total_game_time_table()])
            ),
        ],
        expand=True,
    )
            
            
    def statistics_view():
        if base.exist():
            return ft.Column([
                ft.Text("Statistics View", style="headlineMedium"),
                statistics_tabs(),
            ], scroll=ft.ScrollMode.AUTO, expand=True)
        else:
            return ft.Column([
                ft.Text("No database found!")
                ])
        
    # ***************
    # WISHLIST VIEW
    # ***************

    def check_wish_fields(e, title, platform, publisher, developer):
        if not (title and platform and publisher and developer):
            page.add(ft.Text("Please fill out all fields!", color="red"))
            return False   
        else:
            return True

    def add_game_to_wishlist(e, title, platform, publisher, developer):
        if check_wish_fields(e, title, platform, publisher, developer):
            base.add_game_to_wishlist(title, platform, publisher, developer)
            page.clean()
            main(page)
        page.add(ft.Text("Please fill out all fields!", color="red"))   

    def add_game_to_wishlist_menu(e):
        page.clean()
        page.add(ft.Text("Add game"))
        title_field = ft.TextField(label="Title")
        developer_field = ft.Dropdown(label="Developer")
        for database_developer in base.show_developer():
            developer_field.options.append(ft.dropdown.Option(database_developer[1]))
        publisher_field = ft.Dropdown(label="Publisher")
        for database_publishers in base.show_publisher():
            publisher_field.options.append(ft.dropdown.Option(database_publishers[1]))
        platform_field = ft.Dropdown(label="Platform")
        for database_platform in base.show_platform():
            platform_field.options.append(ft.dropdown.Option(database_platform[1]))
        
        add_platform = ft.ElevatedButton("Edit platform", on_click=lambda e:edit_platform(e, platform_field))
        add_publisher = ft.ElevatedButton("Edit publishers", on_click=lambda e:edit_publisher(e, publisher_field))
        add_developer = ft.ElevatedButton("Edit developers", on_click=lambda e:edit_developer(e, developer_field))

        delete_platform_btn = ft.ElevatedButton("Delete platform", on_click=lambda e:delete_platform(e, platform_field)) 
        delete_developer_btn = ft.ElevatedButton("Delete developer", on_click=lambda e:delete_developer(e, developer_field))
        delete_publisher_btn = ft.ElevatedButton("Delete publisher", on_click=lambda e:delete_publisher(e, publisher_field)) 

        games_fields = ft.Column([title_field,
                            ft.Row(controls=[platform_field, add_platform, delete_platform_btn]),
                            ft.Row(controls=[publisher_field, add_publisher, delete_publisher_btn]),
                            ft.Row(controls=[developer_field, add_developer, delete_developer_btn])], scroll=ft.ScrollMode.AUTO, expand=True)

        page.add(games_fields)
        add_game_btn = ft.ElevatedButton("Add", 
                                   on_click=lambda e:add_game_to_wishlist(e,
                                                     title_field.value, 
                                                     platform_field.value, 
                                                     publisher_field.value, 
                                                     developer_field.value), 
                                   data=0)
        back_btn = ft.OutlinedButton("Back", on_click=lambda e:main(page))
        page.add(ft.Row(controls=[add_game_btn, back_btn]))

    def modify_wishlist_game(e, id, title, platform, publisher, developer):
        if check_fields(e, title, platform, publisher, developer):
            base.modify_game(id, title, platform, publisher, developer)
            page.clean()
            main(page)
        page.add(ft.Text("Please fill out all fields!", color="red"))   

    def modify_wishlist(e, title):
        game = base.show_wishlist_game(title)[0]
        page.clean()
        page.add(ft.Text("Modify game"))
        title_field = ft.TextField(label="Title", value = game[1])

        platform_field = ft.Dropdown(label="Platform")
        for database_platform in base.show_platform():
            platform_field.options.append(ft.dropdown.Option(database_platform[1]))
        platform_field.value = base.get_platform_name(game[2])

        publisher_field = ft.Dropdown(label="Publisher")
        for database_publishers in base.show_publisher():
            publisher_field.options.append(ft.dropdown.Option(database_publishers[1]))
        publisher_field.value = base.get_publisher_name(game[3])

        developer_field = ft.Dropdown(label="Developer")
        for database_developer in base.show_developer():
            developer_field.options.append(ft.dropdown.Option(database_developer[1]))
        developer_field.value = base.get_developer_name(game[4])
        
        add_platform = ft.ElevatedButton("Edit platform", on_click=lambda e:edit_platform(e, modify_wishlist(e, title)))
        add_publisher = ft.ElevatedButton("Edit publishers", on_click=lambda e:edit_publisher(e, modify_wishlist(e, title)))
        add_developer = ft.ElevatedButton("Edit developers", on_click=edit_developer)

        delete_platform_btn = ft.ElevatedButton("Delete platform", on_click=lambda e:delete_platform(e, platform_field)) 
        delete_developer_btn = ft.ElevatedButton("Delete developer", on_click=lambda e:delete_developer(e, developer_field))
        delete_publisher_btn = ft.ElevatedButton("Delete publisher", on_click=lambda e:delete_publisher(e, publisher_field)) 

        games_fields = ft.Column([title_field,
                            ft.Row(controls=[platform_field, add_platform, delete_platform_btn]),
                            ft.Row(controls=[publisher_field, add_publisher, delete_publisher_btn]),
                            ft.Row(controls=[developer_field, add_developer, delete_developer_btn])], scroll=ft.ScrollMode.AUTO, expand=True)

        page.add(games_fields)
        
        modify_game_btn = ft.ElevatedButton("Modify", 
                                   on_click=lambda e:modify_wishlist_game(e,
                                                     int(game[0]),
                                                     title_field.value, 
                                                     platform_field.value, 
                                                     publisher_field.value, 
                                                     developer_field.value), 
                                   data=0)
        back_btn = ft.OutlinedButton("Back", on_click=lambda e:main(page))
        page.add(ft.Row(controls=[modify_game_btn, back_btn]))

    def move_game(e, title, copies, time, status, platform, games_store, subscription, box, paid, publisher, developer, series):
        if check_fields(e, title, copies, time, status, platform, games_store, subscription, box, paid, publisher, developer, series):
            if paid == "No":
                paid = 0
            else:
                paid = 1
            if box == "No":
                box = 0
            else:
                box = 1
            base.add_game(title, copies, time, status, platform, games_store, subscription, box, paid, publisher, developer, series)
            delete_wishlist_game(e, title)
            page.clean()
            main(page)
        page.add(ft.Text("Please fill out all fields!", color="red"))

    def move_game_menu(e, title):
        game = base.show_wishlist_game(title)[0]
        page.clean()
        page.add(ft.Text("Move game from wishlist to game list"))
        title_field = ft.TextField(label="Title", value=game[1])
        copies_field = ft.TextField(label="Number of copies", value="1")
        time_hours_field = ft.TextField(label="Game time: Hours", value="0")
        time_minutes_field = ft.TextField(label="Game time: Minutes", value="0")
        time_seconds_field = ft.TextField(label="Game time: Seconds", value="0")
        status_field = ft.Dropdown(label="Status", options=[ft.dropdown.Option("Finished"), ft.dropdown.Option("Started"), ft.dropdown.Option("Not started")])
        status_field.value = status_field.options[2].key

        platform_field = ft.Dropdown(label="Platform")
        for database_platform in base.show_platform():
            platform_field.options.append(ft.dropdown.Option(database_platform[1]))
        platform_field.value = base.get_platform_name(game[2])

        games_store_field = ft.Dropdown(label="Games store")
        for database_games_stores in base.show_games_store():
            games_store_field.options.append(ft.dropdown.Option(database_games_stores[1]))
        games_store_field.value = games_store_field.options[0].key

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
        publisher_field.value = base.get_publisher_name(game[3])

        developer_field = ft.Dropdown(label="Developer")
        for database_developer in base.show_developer():
            developer_field.options.append(ft.dropdown.Option(database_developer[1]))
        developer_field.value = base.get_developer_name(game[4])

        series_field = ft.Dropdown(label="Series")
        for database_series in base.show_series():
            series_field.options.append(ft.dropdown.Option(database_series[1]))
        
        add_platform = ft.ElevatedButton("Edit platform", on_click=lambda e:edit_platform(e, platform_field))
        add_games_store = ft.ElevatedButton("Edit games stores", on_click=lambda e:edit_games_stores(e, games_store_field))
        add_subscription = ft.ElevatedButton("Edit subscriptions", on_click=lambda e:edit_subscriptions(e, subscription_field))
        add_series = ft.ElevatedButton("Edit series", on_click=lambda e:edit_series(e, series_field))
        add_publisher = ft.ElevatedButton("Edit publishers", on_click=lambda e:edit_publisher(e, publisher_field))
        add_developer = ft.ElevatedButton("Edit developers", on_click=lambda e:edit_developer(e, developer_field))

        delete_platform_btn = ft.ElevatedButton("Delete platform", on_click=lambda e:delete_platform(e, platform_field)) 
        delete_games_store_btn = ft.ElevatedButton("Delete games store", on_click=lambda e:delete_games_store(e, games_store_field)) 
        delete_series_btn = ft.ElevatedButton("Delete serie", on_click=lambda e:delete_series(e, series_field)) 
        delete_developer_btn = ft.ElevatedButton("Delete developer", on_click=lambda e:delete_developer(e, developer_field))
        delete_subscription_btn = ft.ElevatedButton("Delete subscription", on_click=lambda e:delete_subscription(e, subscription_field))
        delete_publisher_btn = ft.ElevatedButton("Delete publisher", on_click=lambda e:delete_publisher(e, publisher_field)) 

        games_fields = ft.Column([title_field,
                            copies_field,
                            ft.Row(controls=[time_hours_field, ft.Text(":"), time_minutes_field, ft.Text(":"), time_seconds_field]),
                            status_field,
                            ft.Row(controls=[platform_field, add_platform, delete_platform_btn]),
                            ft.Row(controls=[games_store_field, add_games_store, delete_games_store_btn]),
                            ft.Row(controls=[subscription_field, add_subscription, delete_subscription_btn]),
                            box_field,
                            paid_field,
                            ft.Row(controls=[publisher_field, add_publisher, delete_publisher_btn]),
                            ft.Row(controls=[developer_field, add_developer, delete_developer_btn]),
                            ft.Row(controls=[series_field, add_series, delete_series_btn])], scroll=ft.ScrollMode.AUTO, expand=True)

        page.add(games_fields)
        
        add_game_btn = ft.ElevatedButton("Add", 
                                   on_click=lambda e:move_game(e,
                                                     title_field.value, 
                                                     copies_field.value, 
                                                     f"{time_hours_field.value}:{time_minutes_field.value}:{time_seconds_field.value}", 
                                                     status_field.value, 
                                                     platform_field.value,
                                                     games_store_field.value, 
                                                     subscription_field.value,
                                                     box_field.value, 
                                                     paid_field.value, 
                                                     publisher_field.value, 
                                                     developer_field.value, 
                                                     series_field.value), 
                                   data=0)
        back_btn = ft.OutlinedButton("Back", on_click=lambda e:main(page))
        page.add(ft.Row(controls=[add_game_btn, back_btn]))


    def delete_wishlist_game(e, title):
        base.delete_wishlist_game(title)
        main(page)

    def edit_wishlist_game_menu(e):
        page.clean()
        games = ft.Dropdown(label="Wishlist")
        for game in base.show_wishlist_games():
            games.options.append(ft.dropdown.Option(game[1]))
        page.add(games)
        page.add(ft.Row(controls=[ft.ElevatedButton("Delete game", on_click=lambda e:delete_wishlist_game(e, games.value), data=0), 
                                  ft.ElevatedButton("Modify", on_click=lambda e:modify_wishlist(e, games.value)),
                                  ft.ElevatedButton("Move to game list", on_click=lambda e:move_game_menu(e, games.value)), 
                                  ft.ElevatedButton("Back", on_click=lambda e:main(page))]))

    def get_wishlist_games_datatable(begin = 0, end = -1, find=None, filters=None):
        games_rows = []
        games_list = base.show_wishlist_games(find, filters)

        if end == -1 and begin == 0:
            list_range = games_list
        else:
            list_range = games_list[begin:end]

        for game in list_range:
            cell_tab = []
            cell_tab.append(ft.DataCell(ft.Text(game[0])))
            cell_tab.append(ft.DataCell(ft.Text(game[1])))
            cell_tab.append(ft.DataCell(ft.Text(base.get_platform_name(game[2]))))
            cell_tab.append(ft.DataCell(ft.Text(base.get_publisher_name(game[3]))))
            cell_tab.append(ft.DataCell(ft.Text(base.get_developer_name(game[4]))))
            games_rows.append(ft.DataRow(cells=cell_tab))
        games_columns = []
        games_columns.append(ft.DataColumn(ft.Text("ID")))
        games_columns.append(ft.DataColumn(ft.Text("Title")))
        games_columns.append(ft.DataColumn(ft.Text("Platform")))
        games_columns.append(ft.DataColumn(ft.Text("Publisher")))
        games_columns.append(ft.DataColumn(ft.Text("Developer")))         

        table = ft.DataTable(
            sort_column_index=0,
            sort_ascending=True,
            show_checkbox_column=True,
            columns= games_columns,
            rows = games_rows
        )
    
        return ft.Column([table], scroll=ft.ScrollMode.AUTO, expand=True)

    def wishlist_view(list_begin, list_end, find, filters):
        if base.exist():
            if base.show_games() != []:
                if find==None:
                    search_btn = ft.ElevatedButton("Search", on_click=find_menu, data=0)
                else:
                    search_btn = ft.OutlinedButton(f"Searched - '{find}'", on_click=lambda e:init_navbar(0, -1, None), data=0)
                if filters == None:
                    filters_btn = ft.ElevatedButton("Filters", on_click=filter_wishlist_menu, data=0)
                else:
                    filters_btn = ft.OutlinedButton(f"Filtered - '{filters}'", on_click=lambda e:init_navbar(0, -1, find, None), data=0)

                if list_begin == 0 and list_end == len(base.show_games()):
                    show_all = ft.OutlinedButton("Show less", on_click=lambda e:init_navbar(0, 50), data=0)
                else:
                    show_all = ft.ElevatedButton("Show all", on_click=lambda e:init_navbar(0, len(base.show_games())), data=0)

                return ft.Column([
                    ft.Text("Wishlist", style="headlineMedium"),
                    ft.Row(controls=[ft.ElevatedButton("Add game", on_click=add_game_to_wishlist_menu, data=0),
                                     ft.ElevatedButton("Edit wishlist", on_click=edit_wishlist_game_menu, data=0)]),
                    ft.Row(controls=[search_btn,
                                     filters_btn]),
                    ft.Row(controls=[ft.ElevatedButton("<", on_click=lambda e:move_left_game_list(list_begin, list_end), data=0),
                                     ft.Text(f"{list_begin} - {list_end}"),
                                     ft.ElevatedButton(">", on_click=lambda e:move_right_game_list(list_begin, list_end), data=0),
                                     show_all]),
                    ft.Divider(),
                    get_wishlist_games_datatable(list_begin, list_end, find, filters),
                    ft.Divider()
                    ], scroll=ft.ScrollMode.AUTO, expand=True)
            else:
                return ft.Column([
                    ft.Text("Wishlist", style="headlineMedium"),
                    ft.ElevatedButton("Add game", on_click=add_game_to_wishlist_menu, data=0)
                    ])
        else:
            return ft.Column([
                ft.Text("No database found!"),
                ft.ElevatedButton("Create a new database", on_click=create_database, data=0),
                ft.ElevatedButton("Load database from Google Drive", on_click=add_game_menu, data=0)
                ])
        
    # ***************
    # SETTINGS VIEW
    # ***************

    def settings_view():
        return ft.Column([
            ft.Text("Settings View", style="headlineMedium"),
            ft.Text("Explore different options available."),
            ft.ListView([
                ft.Text("Option 1"),
                ft.Text("Option 2"),
                ft.Text("Option 3"),
            ]),

        ])

    def on_tab_change(event, list_begin, list_end, find, filters):
        if event.control.selected_index == 0:
            page.controls[1].content = manage_database_view(list_begin, list_end, find, filters)
        elif event.control.selected_index == 1:
            page.controls[1].content = wishlist_view(list_begin, list_end, find, filters)
        elif event.control.selected_index == 2:
            page.controls[1].content = statistics_view()
        elif event.control.selected_index == 3:
            page.controls[1].content = settings_view()
        page.update()

    def init_navbar(list_begin, list_end, find=None, filters=None):
        page.clean()
        nav_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Game list"),
                ft.NavigationBarDestination(icon=ft.icons.BOOKMARK_BORDER, label="Wishlist"),
                ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Statistics"),
                ft.NavigationBarDestination(icon=ft.icons.SETTINGS, label="Settings"),
            ],
            on_change=lambda e:on_tab_change(e, list_begin, list_end, find, filters),
        )

        page.add(nav_bar, ft.Container(content=manage_database_view(list_begin, list_end, find, filters), expand=True))
        
    init_navbar(list_begin=0, list_end=50)

ft.app(target=main)
