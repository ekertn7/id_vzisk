from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import Progressbar
from tkinter import filedialog
import functools
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import collections
from PIL import Image, ImageTk
import os


def open_case(wut_is_num):
    print(excel_list[wut_is_num])


def show_an_image(wut_is_num):
    global image_list
    img = Image.open("analys/" + str(image_list[wut_is_num]))
    img = img.resize((900, 600), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    panel = Label(window, image=img)
    panel.image = img
    panel.grid(column=0, row=5, columnspan=6)

    label_poyasn_1.configure(text=str(image_list[wut_is_num]))
    label_poyasn_2.configure(text="П - подозрительно, Н - неподозрительно, Р - в работе, В - не выявлено.")


def show_another_image(delta):
    global wut_is_num, image_list
    try:
        if wut_is_num > 0:
            wut_is_num += delta
        elif wut_is_num == 0 and delta == +1:
            wut_is_num += delta
        elif wut_is_num == 0 and delta == -1:
            wut_is_num = 0
        else:
            wut_is_num = 0
        img = Image.open("analys/" + str(image_list[wut_is_num]))
        img = img.resize((900, 600), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        panel = Label(window, image=img)
        panel.image = img
        panel.grid(column=0, row=5, columnspan=6)
        label_poyasn_1.configure(text=str(image_list[wut_is_num]))
    except IndexError:
        wut_is_num -= delta
    # print(wut_is_num)
    return wut_is_num


def input_choice_clicked():
    name_of_file = filedialog.askopenfilename(filetypes = (("Excel files","*.xlsx"),("CSV files","*.csv"),("Text files","*.txt"),("all files","*.*")))
    if ".csv" in str(name_of_file.split('/')[-1]):
        df = pd.read_csv(name_of_file)
    elif ".xlsx" in str(name_of_file.split('/')[-1]):
        df = pd.read_excel(name_of_file)
    else:
        df = pd.read_csv(name_of_file)
    return df


def graph(df):
    df = df.rename(columns={
        str(node1_choice.get()): "d_inn"
        , str(node2_choice.get()): "k_num"
        , str(prizn1_choice.get()): "status_otp"
        , str(prizn2_choice.get()): "status_pol_fl"
        , str(prizn3_choice.get()): "status_pol_ul"
    })
    perem_save = 1
    dg_index = 0
    while dg_index <= max(df.index):
        try:
            dg_info = df.d_inn[dg_index]
            data_merge = df.where(df.d_inn == dg_info).dropna(how="all")
            const_len_data_merge = 0

            while len(data_merge) != const_len_data_merge:
                const_len_data_merge = len(data_merge)
                k_num_frame = pd.DataFrame(data=list(data_merge.k_num), columns=["val_key"]).drop_duplicates()
                data_merge = pd.merge(k_num_frame, df, how="inner", left_on="val_key", right_on="k_num").drop(columns=["val_key"])

                d_inn_frame = pd.DataFrame(data=list(data_merge.d_inn), columns=["val_key"]).drop_duplicates()
                data_merge = pd.merge(d_inn_frame, df, how="inner", left_on="val_key", right_on="d_inn").drop(columns=["val_key"])

            print("Index: " + str(dg_index) + ", len: " + str(len(data_merge)))

            dg = data_merge
            g = nx.Graph()

            d_map = []
            k_map = []
            nodes_map = []
            label_map = []
            label_dict = {}
            color_map = []
            size_map = []

            for i, row in dg.iterrows():
                g.add_edge(dg.d_inn[i], dg.k_num[i])
                d_map.append(dg.d_inn[i])
                k_map.append(dg.k_num[i])

            k_map = [item for item, count in collections.Counter(k_map).items() if count > 1]

            for node in nx.nodes(g):
                if node in dg["d_inn"].values:
                    node_indx = df[node == df.d_inn.values].index.values[0]
                    node_status = df.status_otp[node_indx]
                    if node_status == "Подозрительно":
                        label_map.append("П отп")
                        color_map.append("Purple")
                    elif node_status == "Неподозрительно":
                        label_map.append("Н отп")
                        color_map.append("Pink")
                    elif node_status == "Другое":
                        label_map.append("Р отп")
                        color_map.append("Orange")
                    else:
                        label_map.append("В отп")
                        color_map.append("Gray")
                    size_map.append(2000)
                    nodes_map.append(node)
                elif node in dg["k_num"].values:
                    node_indx = df[node == df.k_num.values].index.values[0]
                    node_status_1 = df.status_pol_fl[node_indx]
                    node_status_2 = df.status_pol_ul[node_indx]
                    if node_status_1 == "Подозрительно" or node_status_2 == "Подозрительно":
                        label_map.append("П пол")
                        color_map.append("Red")
                    elif node_status_1 == "Неподозрительно" or node_status_2 == "Неподозрительно":
                        label_map.append("Н пол")
                        color_map.append("Blue")
                    elif node_status_1 == "Другое" or node_status_2 == "Другое":
                        label_map.append("Р пол")
                        color_map.append("Yellow")
                    else:
                        label_map.append("В пол")
                        color_map.append("Gray")
                    size_map.append(900)
                    nodes_map.append(node)
            label_dict = dict(zip(nodes_map, label_map))
            plt.figure(figsize=(30,20))

            nx.draw(g
                    , node_color=color_map
                    , node_size=size_map
                    , with_labels=True
                    , labels=label_dict
                    , alpha=0.7
                    , font_color="black"
                    , node_shape="o"
                    , font_size = 40)

            labels = pd.DataFrame(data={"keys":list(label_dict.keys()), "values":list(label_dict.values())})
            # labels["values"] = labels["values"].str.replace("-","")
            # labels["values"] = labels["values"].str.replace(".","")
            labels["values"] = labels["values"].str.replace("отп", "")
            labels["values"] = labels["values"].str.replace("пол", "")
            labels["values"] = labels["values"].str.replace(" ","")

            if len(set(list(labels["values"]))) == 1:
                data_merge.to_excel("odinak/" + str(perem_save) + "_odinak.xlsx", index=False)
                plt.savefig("odinak/" + str(perem_save) + "_case.png")
            else:
                if "Н" in list(labels["values"]) and "П" in list(labels["values"]) and "Р" in list(labels["values"]):
                    data_merge.to_excel("nepod/" + str(perem_save) + "_nepod.xlsx", index=False)
                    plt.savefig("nepod/" + str(perem_save) + "_case.png")
                else:
                    data_merge.to_excel("analys/" + str(perem_save) + "_analys.xlsx", index=False)
                    plt.savefig("analys/" + str(perem_save) + "_case.png")
            df = pd.concat([df, data_merge]).drop_duplicates(keep=False)
            perem_save += 1
        except KeyError as ke:
            print("KeyError")
        except IndexError as ie:
            print("IndexError")
        finally:
            dg_index += 1
        final_text.configure(text="Построение выполнено")


def get_image_list():
    dirlist = list(os.listdir("analys"))
    dirlist_len_start = len(dirlist)
    dirlist_len_end = 0
    while dirlist_len_end != dirlist_len_start:
        dirlist_len_start = len(dirlist)
        for i in dirlist:
            if ".png" not in i:
                dirlist.remove(i)
            else:
                continue
        dirlist_len_end = len(dirlist)
    p_dirlist = list(range(1,len(dirlist)+1))
    i_dirlist=[]
    for e in p_dirlist:
        i_dirlist.append(str(e) + "_case.png")
    return i_dirlist


def get_excel_list():
    dirlist = list(os.listdir("analys"))
    dirlist_len_start = len(dirlist)
    dirlist_len_end = 0
    while dirlist_len_end != dirlist_len_start:
        dirlist_len_start = len(dirlist)
        for i in dirlist:
            if ".png" not in i:
                dirlist.remove(i)
            else:
                continue
        dirlist_len_end = len(dirlist)
    p_dirlist = list(range(1,len(dirlist)+1))
    i_dirlist=[]
    for e in p_dirlist:
        i_dirlist.append(str(e) + "_analys.xlsx")
    return i_dirlist


if __name__ == '__main__':
    window = Tk()
    window.title("ИД взыскания")
    window.geometry("1050x1000")

    # input_text = Label(window, text="Загрузите файл", font=("Arial", 18))
    # input_text.grid(column=0, row=0)
    # input_choice = Button(window, text="Выбрать файл", command=input_choice_clicked)
    # input_choice.grid(column=1, row=0)

    df = input_choice_clicked()

    choice_list = list(df.columns)
    print(choice_list)

    node1_text = Label(window, text="ИНН отправителя", justify=LEFT, font=("Arial", 14,))
    node1_text.grid(column=0, row=0)
    node1_choice = Combobox(window)
    node1_choice["values"] = choice_list
    node1_choice.current(0)
    node1_choice.grid(column=0, row=1)

    node2_text = Label(window, text="Счет получателя", justify=LEFT, font=("Arial", 14,))
    node2_text.grid(column=1, row=0)
    node2_choice = Combobox(window)
    node2_choice["values"] = choice_list
    node2_choice.current(0)
    node2_choice.grid(column=1, row=1)

    prizn1_text = Label(window, text="Признак отправителя", justify=LEFT, font=("Arial", 14,))
    prizn1_text.grid(column=2, row=0)
    prizn1_choice = Combobox(window)
    prizn1_choice["values"] = choice_list
    prizn1_choice.current(0)
    prizn1_choice.grid(column=2, row=1)

    prizn2_text = Label(window, text="Признак получателя ФЛ", justify=LEFT, font=("Arial", 14,))
    prizn2_text.grid(column=3, row=0)
    prizn2_choice = Combobox(window)
    prizn2_choice["values"] = choice_list
    prizn2_choice.current(0)
    prizn2_choice.grid(column=3, row=1)

    prizn3_text = Label(window, text="Признак получателя ЮЛ", justify=LEFT, font=("Arial", 14,))
    prizn3_text.grid(column=4, row=0)
    prizn3_choice = Combobox(window)
    prizn3_choice["values"] = choice_list
    prizn3_choice.current(0)
    prizn3_choice.grid(column=4, row=1)

    btn_graph = Button(window, text="Построить граф", command=functools.partial(graph, df))
    btn_graph.grid(column=0, row=2)

    final_text = Label(window, text="", justify=LEFT, font=("Arial", 14,))
    final_text.grid(column=0, row=3)

    label_poyasn_1 = Label(window, text="", justify=LEFT, font=("Arial", 14,))
    label_poyasn_1.grid(column=0, row=6)
    label_poyasn_2 = Label(window, text="", justify=LEFT, font=("Arial", 14,))
    label_poyasn_2.grid(column=1, row=6, columnspan=4)

    wut_is_num = 0

    btn_an_img = Button(window, text="Показать кейсы", command=functools.partial(show_an_image, wut_is_num))
    btn_an_img.grid(column=1, row=2)

    btn_next_img = Button(window, text="Следующий слайд", command=functools.partial(show_another_image, +1))
    btn_next_img.grid(column=4, row=2)

    btn_open_case = Button(window, text="Открыть кейс", command=functools.partial(open_case, wut_is_num))
    btn_open_case.grid(column=3, row=2)

    btn_prev_img = Button(window, text="Предыдущий слайд", command=functools.partial(show_another_image, -1))
    btn_prev_img.grid(column=2, row=2)

    image_list = get_image_list()
    excel_list = get_excel_list()

    window.mainloop()
