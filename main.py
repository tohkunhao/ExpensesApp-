from kivy.app import App
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color, Line
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.clock import Clock
import pandas as pd
import numpy as np
import pickle
import os


class Month:
    def __init__(self):
        self.month_dict = {}

    def addItem(self, category, item_name, item_price):
        data = {'Item Name': item_name, 'Item Price': int(item_price)}
        if category in self.month_dict:
            # add to existing dictionary
            self.month_dict[category] = self.month_dict[category].append(data, ignore_index=True)
        else:
            # add dataframe to dictionary
            self.month_dict[category] = pd.DataFrame([data], columns=['Item Name', 'Item Price'])

    def getCategories(self):
        return [i for i in self.month_dict]

    def getSubtotal(self):
        subtotal = []
        for category in self.month_dict:
            subtotal.append(self.month_dict[category]['Item Price'].sum())
        return subtotal


class ExpenseApp(App):
    def build(self):
        return kv


class BodyVerticalStack(StackLayout):
    pass


class MainWindow(Screen):
    def __init__(self, **kwargs):
        self.dropdown_month = []
        self.dropdown_year = []
        self.main_dict = {}
        self.StartUpProcedure()
        self.year_string = None
        self.month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.month_to_numeral = self.MonthToNumGen(self.month_list)
        self.monthly_cat = []  # for pie chart labels
        self.cat_subtotal = []
        super().__init__(**kwargs)

    def StartUpProcedure(self):
        dir_list = os.listdir()
        if 'data.pkl' in dir_list:
            self.LoadData()
            self.YearExtract()
            # TODO: check if current date has entry in db, if so display automatically change the year/month selector
            # TODO: populate sub pie chart data lists (lists of lists)

    def LoadData(self):
        with open('data.pkl', 'rb') as f:
            keys = pickle.load(f)
            for key in keys:
                self.main_dict[key] = Month()
                self.main_dict[key].month_dict = pickle.load(f)

    def SaveData(self):
        with open('data.pkl', 'wb') as f:
            pickle.dump([key for key in self.main_dict], f)
            for key in self.main_dict:
                pickle.dump(self.main_dict[key].month_dict, f)

    def ObtainCategoryList(self, all_entry_dict):
        """
        登録されているカテゴリをリストにする関数。Extract all categories that exist in whole database.
        :param all_entry_dict:
        :return: 全カテゴリのリスト。list of all categories that exist
        """
        cat_list = []
        for key in all_entry_dict:
            for category in all_entry_dict[key].getCategories:
                if category not in cat_list:
                    cat_list.append(category)
        return cat_list

    def UpdateMonth(self):
        self.dropdown_month = []
        num_list = []
        for key in self.main_dict:
            if self.ids.year_spinner.text in key:
                month_num = int(key[4:])-1
                if month_num not in num_list:
                    num_list.append(month_num)
        num_list.sort()
        self.dropdown_month=[self.month_list[i] for i in num_list]
        self.ids.month_spinner.values = self.dropdown_month

    def YearExtract(self):
        self.dropdown_year = []
        for key in self.main_dict:
            key_cleaned = key[:4]
            if key_cleaned not in self.dropdown_year:
                self.dropdown_year.append(key_cleaned)

    def MonthToNumGen(self, month_list):
        num_dict = {}
        for index, month in enumerate(month_list):
            index_str = str(index+1)
            if len(index_str) == 1:
                index_str = "0"+index_str
            num_dict[month] = index_str
        return num_dict

    def AddEntry(self, item_txt, price, category, year, month):
        dict_key = str(year)+self.month_to_numeral[month]
        if dict_key not in self.main_dict:
            self.main_dict[dict_key] = Month()
        self.main_dict[dict_key].addItem(category, item_txt, price)
        if self.ids.year_spinner.text == year and self.ids.month_spinner.text == month:
            self.UpdateMonthSubtotal()

    def UpdateMonthSubtotal(self):
        main_key = self.ids.year_spinner.text + self.month_to_numeral[self.ids.month_spinner.text]
        if main_key in self.main_dict:
            self.cat_subtotal = self.main_dict[main_key].getSubtotal()
            self.ids.main_pie.values = self.cat_subtotal


class InputWindow(Screen):
    def LimitSpinner(self, *args):
        max_open = 2
        self.ids.input_month_spinner.dropdown_cls.max_height = max_open * dp(48)

    def ClearFormFields(self):
        self.ids.item_input.text = ""
        self.ids.price_input.text = ""
        self.ids.category_input.text = ""
        self.ids.year_input.text = ""
        self.ids.input_month_spinner.text = "Select"

    def CheckFormFields(self):
        id_list = [self.ids.item_input.text, self.ids.price_input.text, self.ids.category_input.text,
                   self.ids.year_input.text, self.ids.input_month_spinner.text]
        missing_field = False
        price_numerical = False
        year_numerical = False
        year_len = False
        for index, field in enumerate(id_list):
            if field == "":
                missing_field = True
            elif index == 4 and field == "Select":
                missing_field = True
            if index == 1:
                price_numerical = field.isnumeric()
            elif index == 3:
                year_numerical = field.isnumeric()
                if len(field) == 4:
                    year_len = True
        if not missing_field and price_numerical and year_numerical and year_len:
            main_screen = self.manager.get_screen("main")
            main_screen.AddEntry(*id_list)
            main_screen.YearExtract()
            main_screen.UpdateMonth()
            main_screen.SaveData()
            main_screen.ids.year_spinner.values = main_screen.dropdown_year
            self.ClearFormFields()
            self.parent.current = "main"
            self.manager.transition.direction = "right"
        else:
            ErrorNotice().open()


class WindowManager(ScreenManager):
    pass


class ErrorNotice(Popup):
    pass


class PieChart(Widget):
    values = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.angles = []
        self.percentage = None
        self.pie = {}  # チャートオブジェクトを保存する辞書, dictionary to save each pie chart component

    def CalculateAngle(self):
        if self.values:
            total = sum(self.values)
            self.angles = []
            for i in self.values:
                self.angles.append(i/total*360)

    def CalculateComponentWeightage(self):
        self.percentage = [i/sum(self.angles)*100 for i in self.angles]

    def on_size(self, *args):
        self.CalculateAngle()
        self.canvas.clear()
        with self.canvas:
            for j in range(len(self.values)):
                np.random.seed(j)
                rgb = np.random.uniform(0.5,0.9,3).tolist()
                Color(*rgb)
                self.pie[str(j)] = Ellipse(pos=(self.center_x-0.3 * min(self.width, self.height),
                                                self.center_y-0.3 * min(self.width, self.height)),
                                           size=(0.6 * min(self.width, self.height),
                                                 0.6 * min(self.width, self.height)),
                                           angle_start=0 if j == 0 else sum(self.angles[0:j]),
                                           angle_end=360 if j == len(self.values)-1 else sum(self.angles[0:j+1]))

    # TODO: Add labels to the pie chart
    # TODO: Add outline to pie chart
    # TODO: integrate title into pie chart

    #def value_change(self):  # might not be needed
    #    self.CalculateAngle()
    #    for j in range(len(self.values)):
    #        if j == 0:
    #            self.pie[str(j)].angle_end = self.angles[j]
    #        elif j == len(self.values)-1:
    #            self.pie[str(j)].angle_start = sum(self.angles[0:j])
    #        else:
    #            self.pie[str(j)].angle_start = sum(self.angles[0:j])
    #            self.pie[str(j)].angle_end = sum(self.angles[0:j+1])

# screen manager kivy
# month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
kv = Builder.load_file("Main.kv")
Window.size = (1200, 675)
Window.minimum_height = 675
Window.minimum_width = 1200
ExpenseApp().run()
