from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config 
from kivy.uix.relativelayout import RelativeLayout 
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.core.text.markup import MarkupLabel

import pymysql
import pymysql.cursors

host = "127.0.0.1"
user = "root"
password = ""
db_name = "shoppingDB"

User_ID = "11335577"
sql_products = 0
sql_quantity = 0
sql_status = 0
try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            select_all_rows = f"SELECT * FROM ShoppingList WHERE USER_ID = '{User_ID}'"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            sql_products = rows[0]['Products'].split(';')
            sql_quantity = rows[0]['Quantity'].split(';')
            sql_status = rows[0]['Status'].split(';')
            for i in range(len(sql_status)):
                sql_status[i] = int(sql_status[i])
            print(sql_products)
    finally:
        connection.close()

except:
    print(1)
#Builder.load_file("shopping.kv")
connection = pymysql.connect(
    host=host,
    port=3306,
    user=user,
    password=password,
    database=db_name,
    cursorclass=pymysql.cursors.DictCursor
)
Config.set('graphics', 'resizable', True) 

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.products = []

    def build(self):
        for i in range(len(sql_products)):
            self.products.append((sql_products[i],sql_quantity[i],sql_status[i]))
        print(self.products)
        root = FloatLayout()

        top_panel = RelativeLayout()
        adding_products = RelativeLayout()
        product_list_layout = GridLayout(cols=2, spacing=4, size_hint_y=None)
        product_list_layout.bind(minimum_height = product_list_layout.setter("height"))
        clear = RelativeLayout()
        #top_panel
        setting_button = Button(text="Settings", pos_hint={'x':0,'y':0.9},size_hint=(.2,.1))
        list_id_label = Label(text=f"{User_ID}", pos_hint={'x':0.2,'y':0.9},size_hint=(.2,.1))
        delete_button = Button(text="Unconnect", pos_hint={'x':0.4,'y':0.9},size_hint=(.2,.1))
        list_id_inpurt = TextInput(hint_text='list ID', pos_hint={'x':0.6,'y':0.9},size_hint=(.2,.1))
        connect_button = Button(text="Connect", pos_hint={'x':0.8,'y':0.9},size_hint=(.2,.1))
        
        #adding products
        product_input = TextInput(pos_hint={'x':0,'y':0.8},size_hint=(.7,.1))
        quantity_input = TextInput(pos_hint={'x':0.7,'y':0.8},size_hint=(.2,.1))
        add_product_button = Button(pos_hint={'x':0.9,'y':0.8},size_hint=(.1,.1), text="Add")

        clear_button = Button(text="Clear", pos_hint={'x':0,'y':0},size_hint=(1,.1))
        def add_product(instance):
            product_name = product_input.text
            product_quantity = quantity_input.text
            number = len(self.products)
            print(number)
            self.products.insert(0,(product_name, product_quantity, 1))
            product_list_layout.clear_widgets()
            for i in range(len(self.products)):

                if(self.products[i][2]):
                    ilabel = Label(text=f"{self.products[i][0]} : {self.products[i][1]}", size_hint_y=None, size_hint_x=0.9, height=40)
                else:
                    ilabel = Label(
                            text=f"[s]{self.products[i][0]} : {self.products[i][1]}[/s]",
                            size_hint_y=None,
                            size_hint_x=0.9,
                            height=40,
                            markup=True
                        )
                ibutton = Button(text="+", size_hint_y=None, size_hint_x=0.1, height=40)
                product_list_layout.add_widget(ilabel)
                product_list_layout.add_widget(ibutton)
                print(self.products)
                products_list = ';'.join([item[0] for item in self.products])
                quantity_list = ';'.join([item[1] for item in self.products])
                status_list = ';'.join([str(item[2]) for item in self.products])


                with connection.cursor() as cursor:
                    update_query = f"UPDATE `ShoppingList` SET `Products`='{products_list}',`Quantity`='{quantity_list}',`Status`='{status_list}' WHERE USER_ID='{User_ID}'"
                    cursor.execute(update_query)
                    connection.commit()


                def gotten_item(instance, index=i):
                    product_list_layout.clear_widgets()
                    if(self.products[index][2]==1):
                        self.products[index]=(self.products[index][0],self.products[index][1],0)
                        self.products.append(self.products.pop(index))
                    else:
                        self.products[index]=(self.products[index][0],self.products[index][1],1)
                        self.products.insert(0, self.products.pop(index))
                    products_list = ';'.join([item[0] for item in self.products])
                    quantity_list = ';'.join([item[1] for item in self.products])
                    status_list = ';'.join([str(item[2]) for item in self.products])

                    with connection.cursor() as cursor:
                        update_query = f"UPDATE `ShoppingList` SET `Products`='{products_list}',`Quantity`='{quantity_list}',`Status`='{status_list}' WHERE USER_ID='{User_ID}'"
                        cursor.execute(update_query)
                        connection.commit()

                    print(self.products)
                    for i, item in enumerate(self.products):
                        if(item[2]==0):
                            ilabel = Label(
                            text=f"[s]{item[0]} : {item[1]}[/s]",
                            size_hint_y=None,
                            size_hint_x=0.9,
                            height=40,
                            markup=True
                        )
                        else:
                            ilabel = Label(text=f"{item[0]} : {item[1]}", size_hint_y=None, size_hint_x=0.9, height=40)
                        ibutton = Button(text="+", size_hint_y=None, size_hint_x=0.1, height=40)
                        product_list_layout.add_widget(ilabel)
                        product_list_layout.add_widget(ibutton)
                        ibutton.bind(on_press=lambda instance, idx=i: gotten_item(instance, idx))
                ibutton.bind(on_press=gotten_item)


        def delete_all(instance):
            self.products.clear()
            product_list_layout.clear_widgets()
            with connection.cursor() as cursor:
                update_query = f"UPDATE `ShoppingList` SET `Products`='',`Quantity`='',`Status`='' WHERE USER_ID='{User_ID}'"
                cursor.execute(update_query)
                connection.commit()
        
        add_product_button.bind(on_press=add_product)
        clear_button.bind(on_press=delete_all)
        
        #adding widg to lay
        top_panel.add_widget(setting_button)
        top_panel.add_widget(list_id_label)
        top_panel.add_widget(delete_button)
        top_panel.add_widget(list_id_inpurt)
        top_panel.add_widget(connect_button)

        adding_products.add_widget(product_input)
        adding_products.add_widget(add_product_button)
        adding_products.add_widget(quantity_input)

        clear.add_widget(clear_button)
        # for i in range(24):
        #     ilabel = Label(text=str(i), size_hint_y=None, size_hint_x=0.9, height=40)
        #     ibutton = Button(text=str(i), size_hint_y=None, size_hint_x=0.1, height=40)
        #     product_list_layout.add_widget(ilabel)
        #     product_list_layout.add_widget(ibutton)

        

        root.add_widget(top_panel)
        root.add_widget(adding_products)

        scroll_view = ScrollView(size_hint=(1,None), size=(200,400), pos_hint={'x': 0, 'y': 0.13})
        scroll_view.add_widget(product_list_layout)
        root.add_widget(scroll_view)

        root.add_widget(clear)
        
        product_list_layout.clear_widgets()
        for i in range(len(self.products)):
            if(self.products[i][2]):
                ilabel = Label(text=f"{self.products[i][0]} : {self.products[i][1]}", size_hint_y=None, size_hint_x=0.9, height=40)
            else:
                ilabel = Label(
                        text=f"[s]{self.products[i][0]} : {self.products[i][1]}[/s]",
                        size_hint_y=None,
                        size_hint_x=0.9,
                        height=40,
                        markup=True
                    )
            ibutton = Button(text="+", size_hint_y=None, size_hint_x=0.1, height=40)
            product_list_layout.add_widget(ilabel)
            product_list_layout.add_widget(ibutton)
            print(self.products)

            def gotten_item(instance, index=i):
                product_list_layout.clear_widgets()
                if(self.products[index][2]==1):
                    self.products[index]=(self.products[index][0],self.products[index][1],0)
                    self.products.append(self.products.pop(index))
                else:
                    self.products[index]=(self.products[index][0],self.products[index][1],1)
                    self.products.insert(0, self.products.pop(index))                
                    print(self.products)
                for i, item in enumerate(self.products):
                    if(item[2]==0):
                        ilabel = Label(
                        text=f"[s]{item[0]} : {item[1]}[/s]",
                        size_hint_y=None,
                        size_hint_x=0.9,
                        height=40,
                        markup=True
                    )
                    else:
                        ilabel = Label(text=f"{item[0]} : {item[1]}", size_hint_y=None, size_hint_x=0.9, height=40)
                    ibutton = Button(text="+", size_hint_y=None, size_hint_x=0.1, height=40)
                    product_list_layout.add_widget(ilabel)
                    product_list_layout.add_widget(ibutton)
                    ibutton.bind(on_press=lambda instance, idx=i: gotten_item(instance, idx))
            ibutton.bind(on_press=gotten_item)

        return(root)
        
if __name__ == '__main__':
    MainApp().run()
# layout = GridLayout(cols=4, rows=1, row_force_default=True, row_default_height=40)
# layout.add_widget(Button(text="Set", size_hint_x=None, width=100))
# layout.add_widget(Button(text="ID", size_hint_x=None, width=300))
# layout.add_widget(Button(text="Delet", size_hint_x=None, width=100))
# layout.add_widget(Button(text="Connect", size_hint_x=None, width=100))
# return layout

