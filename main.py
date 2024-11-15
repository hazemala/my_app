from flet import *
import sqlite3

conn = sqlite3.connect("app.db",check_same_thread=False)
cursor = conn.cursor()

def fetch():
    cursor.execute("select * from products")
    data = cursor.fetchall()
    return data

def search(inp):
    cursor.execute("select * from products where Code"
        +" LIKE '%"+inp+"%'"
    )
    rows = cursor.fetchall()
    print(rows)
    return rows

def update(amount,my_id):
        cursor.execute("update products set Amount=? where ID=?",(
            amount,my_id
        ))
        conn.commit()

def insert(code,amount):
        cursor.execute("insert into products values(NULL,?,?)",(
            code,amount
        ))
        conn.commit()

def main(page:Page):
    page.title = "App"
    page.scroll = "auto"
    page.theme_mode = ThemeMode.LIGHT

    def on_change(e):
        # Check if the input is not a digit
        if not e.control.value.isdigit():
            e.control.error_text = "Please enter numbers only"
        else:
            e.control.error_text = None
        page.update()

    def insert_code(code,amount):
        if code == "" or amount == "":
            return False
        
        cursor.execute("select Code from products")
        s = cursor.fetchall()
        for i in s:
            if i.__contains__(code):
                for view in page.views:
                    if view.route == "/add":
                        view.controls.pop()
                        view.controls.append(
                            Text("This code is already exist!",width=390,color='red',size=25,text_align='center')
                        )
                        page.update()
                return False
            
        insert(code,amount)
        for view in page.views:
            if view.route == "/add":
                view.controls.pop()
                view.controls.append(
                    Text("Add success",width=390,color='green',size=25,text_align='center')
                )
                page.update()

    def search_code(inp):
        if inp == "":
            return False
        s = search(inp)
        if s == []:
            for view in page.views:
                if view.route == "/search":
                    view.controls.pop()
                    view.controls.append(
                        Text("Not Found",color='red',size=20,text_align='center')
                    )
                    page.update()
            return False
        
        for view in page.views:
            if view.route == "/search":
                input1 = TextField(str(s[0][0]),width=80,border='none')
                input2 = TextField(str(s[0][1]),width=80,border='none')
                input3 = TextField(str(s[0][2]),width=80,border='none',keyboard_type=KeyboardType.NUMBER,on_change=on_change,on_blur=lambda _:update(input3.value,input1.value))
                view.controls.pop()
                view.controls.append(
                    DataTable(
                        columns=[DataColumn(Text(col)) for col in ["ID","Code","Amount"]],
                        rows=[
                            DataRow(
                                cells=[
                                    DataCell(input1),
                                    DataCell(input2),
                                    DataCell(input3),
                                    ]
                            )
                        ],border=Border(top=BorderSide(1,'black'),right=BorderSide(1,'black'),left=BorderSide(1,'black'),bottom=BorderSide(1,'black')),
                        horizontal_lines=BorderSide(1,'black'),
                        vertical_lines=BorderSide(1,'black'),
                        clip_behavior=ClipBehavior.ANTI_ALIAS,
                        width=350, 
                    )
                )
                page.update()

    inp_search = TextField(label="Write The Code...",width=250,height=40,capitalization=TextCapitalization.CHARACTERS,border_color='blue')
    search_ = ElevatedButton(text="Search",width=100,bgcolor='blue',color='white',on_click=lambda _:search_code(inp_search.value))
    btn_search = ElevatedButton(text="Search Codes",width=200,bgcolor='blue',color='white',on_click=lambda _:page.go("/search"))
    btn_show = ElevatedButton(text="Show Codes",width=200,bgcolor='blue',color='white',on_click=lambda _:page.go("/show"))
    btn_add = ElevatedButton(text="Add Code",width=200,bgcolor='blue',color='white',on_click=lambda _:page.go("/add"))
    inp_add_code = TextField(label='Code',width=250,height=40,capitalization=TextCapitalization.CHARACTERS,border_color='blue')
    inp_add_amount = TextField(label='Amount',width=250,height=40,keyboard_type=KeyboardType.NUMBER,on_change=on_change,border_color='blue')
    add = ElevatedButton(text="Add",width=200,bgcolor='blue',color='white',on_click=lambda _:insert_code(inp_add_code.value,inp_add_amount.value))

    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("App"),center_title=True,leading=Icon(icons.HOME),bgcolor='blue',color='white'),
                    Text("Welcom",width=390,size=30,text_align="center",color='blue',weight=FontWeight.BOLD),
                    Row([btn_search],alignment=MainAxisAlignment.CENTER),
                    Row([btn_show],alignment=MainAxisAlignment.CENTER),
                    Row([btn_add],alignment=MainAxisAlignment.CENTER),
                ],vertical_alignment='center'
            )
        )
        if page.route == "/show":
            data = fetch()
            page.views.append(
                View(
                    "/show",
                    [
                        AppBar(title=Text("Show Codes"),center_title=True,bgcolor='blue',color='white'),
                        DataTable(
                            columns=[DataColumn(Text(col)) for col in ["ID","Code","Amount"]],
                            rows=[
                                DataRow(
                                    cells=[DataCell(Text(str(cell),selectable=True)) for cell in i]
                                )
                                for i in data
                            ],border=Border(top=BorderSide(1,'black'),right=BorderSide(1,'black'),left=BorderSide(1,'black'),bottom=BorderSide(1,'black')),
                            horizontal_lines=BorderSide(1,'black'),
                            vertical_lines=BorderSide(1,'black'),
                            clip_behavior=ClipBehavior.ANTI_ALIAS,
                            width=350
                        ),
                    ],scroll='auto'
                )
            )
        if page.route == "/search":
            page.views.append(
                View(
                    "/search",
                    [
                        AppBar(bgcolor='blue',color='white'),
                        Text('Search',width=390,size=30,text_align="center",color='blue',weight=FontWeight.BOLD),
                        Row([
                            inp_search,
                            search_,
                        ],alignment=MainAxisAlignment.CENTER),
                        Row([]),
                    ],vertical_alignment='center'
                )
            )
        if page.route == "/add":
            page.views.append(
                View(
                    "/add",
                    [
                        AppBar(bgcolor='blue',color='white'),
                        Text('Add Code',width=390,size=30,text_align="center",color='blue',weight=FontWeight.BOLD),
                        inp_add_code,
                        inp_add_amount,
                        add,
                        Row([]),
                    ],vertical_alignment='center',
                    horizontal_alignment='center',
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    
app(main)
