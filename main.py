import pandas as pd
import datetime
from matplotlib import pyplot as plt


def read_data(filepath):
    pd.options.display.max_rows = 999999
    DataFrame = pd.read_csv(filepath)
    #print(DataFrame[['baujahr_bw', 'km_bis']])

    return DataFrame

def preprocess_data(DataFrame, year):
    DataFrame['km_von'].replace(0,  inplace=True)
    DataFrame['km_bis'].replace(0,  inplace=True)

    DataFrame['baujahr_bw'] = DataFrame['baujahr_bw'].fillna(year)
    DataFrame['km_von'] = DataFrame['km_von'].astype('int')

    DataFrame["laenge_bw"] = ((DataFrame['km_von']-DataFrame['km_bis'])*1000)
    DataFrame['laenge_bw'] = DataFrame['laenge_bw'].round(decimals=0)
    DataFrame['laenge_bw'] = DataFrame['laenge_bw'].abs()

    DataFrame['alter_bw'] = current_year - DataFrame['baujahr_bw']

    DataFrame['wandflaeche_bw'] = DataFrame['laenge_bw'] * DataFrame['hoehe_bw']
    DataFrame['wandflaeche_bw'] = DataFrame['wandflaeche_bw'].fillna('')

    DataFrame['old_bw'] = DataFrame['baujahr_bw'] < 2000

    DataFrame.to_csv("/home/babwchi/Desktop/ali_A4/bw_vbg_preprocessed.csv", index=False)
    #print(DataFrame[['km_von', 'km_bis','laenge_bw','baujahr_bw','old_bw']])

    return DataFrame


def explore_building_lengths(DataFrame):
    DataFrame_stats = {}
    DataFrame_stats["shortest"] = DataFrame['laenge_bw'].min()
    DataFrame_stats["longest"] = DataFrame['laenge_bw'].max()
    DataFrame_stats["median"] = DataFrame['laenge_bw'].median()
    DataFrame_stats["mean"] = DataFrame['laenge_bw'].mean().round(decimals=2)
    #print(DataFrame_stats)
    return DataFrame_stats


def plot_type_distribution(DataFrame):
    plt.clf()
    DataFrame.typ_bw.value_counts().plot(kind='pie', autopct='%1.2f%%')
    plt.ylabel('')
    plt.show()
    return plt

def plot_age_distribution(DataFrame):
    plt.clf()
    DataFrame['old_bw'].value_counts().plot(kind="bar",figsize = (7, 7))
    plt.xlabel("Wurde das Bauwerk vor 2000 errichtet?")
    plt.ylabel("Anzahl")
    plt.show()
    return plt

def from_twentieth_century(DataFrame):
    old_bridges = len(DataFrame[(DataFrame['typ_bw'] == 'bruecke') & (DataFrame['old_bw'] == True)])
    percentage_bridges = (old_bridges/len(DataFrame[(DataFrame['typ_bw'] == 'bruecke')]))*100
    percentage_bridges = round(percentage_bridges,2)
    bridges_tupple = (old_bridges,percentage_bridges)

    old_galerie = len(DataFrame[(DataFrame['typ_bw'] == 'galerie') & (DataFrame['old_bw'] == True)])
    percentage_galerie = (old_galerie/len(DataFrame[(DataFrame['typ_bw'] == 'galerie')]))*100
    percentage_galerie = round(percentage_galerie,2)
    galerie_tupple = (old_galerie,percentage_galerie)


    old_tunnel = len(DataFrame[(DataFrame['typ_bw'] == 'tunnel') & (DataFrame['old_bw'] == True)])
    percentage_tunnel = (old_tunnel/len(DataFrame[(DataFrame['typ_bw'] == 'tunnel')]))*100
    percentage_tunnel = round(percentage_tunnel,2)
    tunnel_tupple = (old_tunnel,percentage_tunnel)

    old_unterfuehrung = len(DataFrame[(DataFrame['typ_bw'] == 'unterfuehrung') & (DataFrame['old_bw'] == True)])
    percentage_unterfuehrung = (old_unterfuehrung/len(DataFrame[(DataFrame['typ_bw'] == 'unterfuehrung')]))*100
    percentage_unterfuehrung = round(percentage_unterfuehrung,2)
    unterfuehrung_tupple = (old_unterfuehrung,percentage_unterfuehrung)

    while 1:
        chosen_input = str(input())
        if chosen_input == "bruecke":
            return bridges_tupple
        elif chosen_input == "galerie":
            return galerie_tupple
        elif chosen_input == "tunnel":
            return tunnel_tupple
        elif chosen_input == "unterfuehrung":
            return unterfuehrung_tupple




def mello_ge_schoppernou(DataFrame):
    temp_DataFrame = DataFrame[(DataFrame['bez_str'] == 'Bregenzerwaldstraße') & (DataFrame['km_von'] < 44) & (DataFrame['km_von'] > 31)]
    road_list = temp_DataFrame['bez_bw'].tolist()
    #print(road_list)
    #print(temp_DataFrame)
    road_list = sorted(road_list)
    return road_list

def print_shorter_bridge_distance(DataFrame, route_1, route_2):

    route_1_length = 0
    route_1_str = 0
    for element in route_1:
        print(element)
        route_1_str = route_1_str + 1
        temp_DataFrame = DataFrame.loc[DataFrame['bez_bw'] == element,'laenge_bw'].tolist()
        print(temp_DataFrame)
        for element_1 in temp_DataFrame:
            route_1_length += element_1

    #print(route_1)
    #print(route_1_length)

    route_2_length = 0
    route_2_str = 0
    for element in route_2:
        route_2_str = route_2_str + 1
        #print(element)
        temp_DataFrame = DataFrame.loc[DataFrame['bez_bw'] == element,'laenge_bw'].tolist()
        print(temp_DataFrame)
        for element_1 in temp_DataFrame:
            route_2_length += element_1
    #print(route_2_length)
    if route_2_length > route_1_length:
        print("The first route (",route_1_length,"m over" ,route_1_str,"roads) has a shorter bridge distance than the second route (",route_2_length,"m over ",route_2_str,"roads).")
        return route_1_length
    elif route_1_length > route_2_length:
        print("The second route (",route_2_length,"m over" ,route_2_str,"roads) has a shorter bridge distance than the first route (",route_1_length,"m over ",route_1_str,"roads).")
        return route_2_length
    elif route_1_length == route_2_length:
        print("The first route (",route_1_length,"m  over ",route_1_str,"roads) and the second route (",route_2_length,"m over" ,route_2_str,"roads) have equal bridge distance.")
        return route_2_length


def illuminate_underpasses(DataFrame):

    temp_DataFrame = DataFrame[DataFrame['typ_bw'] == 'unterfuehrung']
    index_list = temp_DataFrame.index.tolist()
    index_array = 0 * [0]
    underpass_list = temp_DataFrame['bez_bw'].tolist()
    splited_element = []
    counter = 0
    for element in underpass_list:
        splited_element = element.split()
        for word in splited_element:
            if word == "gehwegunterführung" or word == "Fußgängersteg" or word == "Radweg":
                index_array.append(index_list[counter])
        counter = counter + 1

    length = temp_DataFrame.loc[index_array,'laenge_bw'].tolist()
    lamp_counter = 0
    for element in length:
        lamp_counter += round(int(element/3),0)

    return lamp_counter

def renovate_galeries(DataFrame, current_year):

    temp_DataFrame = DataFrame[(DataFrame['typ_bw'] == 'galerie') & (DataFrame['alter_bw'] >= 45) & (DataFrame['alter_bw'] < 50)]
    area_to_renovate = temp_DataFrame['wandflaeche_bw'].tolist()
    price_to_pay = 0.00
    for element in area_to_renovate:
        price_to_pay += float(element * 10000.00)

    price_to_pay = format(price_to_pay,'.2f')
    print(price_to_pay)


    return price_to_pay

def renovate_bridges(DataFrame, street):

    total_cost = 0.0
    temp_DataFrame_1 = DataFrame[(DataFrame['typ_bw'] == 'bruecke') & (DataFrame['bez_str'] == street) & (DataFrame['alter_bw'] >= 15) & (DataFrame['alter_bw'] < 30)]
    temp_DataFrame_2 = DataFrame[(DataFrame['typ_bw'] == 'bruecke') & (DataFrame['alter_bw'] >= 30) & (DataFrame['alter_bw'] < 45)]
    temp_DataFrame_3 = DataFrame[(DataFrame['typ_bw'] == 'bruecke') & (DataFrame['alter_bw'] >= 45) & (DataFrame['alter_bw'] < 60)]
    temp_DataFrame_4 = DataFrame[(DataFrame['typ_bw'] == 'bruecke') & (DataFrame['alter_bw'] >= 60)]

    bridges_length = temp_DataFrame_1['laenge_bw'].tolist()
    bridges_width = temp_DataFrame_1['breite_bw'].tolist()
    total_length = 0
    total_width = 0
    total_area = 0
    for element in bridges_length:
        total_length += element
    for element in bridges_width:
        total_width += element
    total_area = total_length * total_width
    total_cost = total_length * 300

    bridges_length = temp_DataFrame_2['laenge_bw'].tolist()
    bridges_width = temp_DataFrame_2['breite_bw'].tolist()
    total_length = 0
    total_width = 0
    total_area = 0
    for element in bridges_length:
        total_length += element
    for element in bridges_width:
        total_width += element
    total_area = total_length * total_width
    total_cost = total_length * 750

    bridges_length = temp_DataFrame_3['laenge_bw'].tolist()
    bridges_width = temp_DataFrame_3['breite_bw'].tolist()
    total_length = 0
    total_width = 0
    total_area = 0
    for element in bridges_length:
        total_length += element
    for element in bridges_width:
        total_width += element
    total_area = total_length * total_width
    total_cost = total_length * 300

    bridges_length = temp_DataFrame_4['laenge_bw'].tolist()
    bridges_width = temp_DataFrame_4['breite_bw'].tolist()
    total_length = 0
    total_width = 0
    total_area = 0
    for element in bridges_length:
        total_length += element
    for element in bridges_width:
        total_width += element
    total_area = total_length * total_width
    total_cost = total_length * 3500


    total_cost = format(total_cost,'.2f')

    return total_cost

if __name__ == "__main__":
    datafile = "/home/babwchi/Desktop/ali_A4/bw_vbg.csv"
    DataFrame = read_data(datafile)
    current_year = datetime.datetime.now().year
    DataFrame = preprocess_data(DataFrame, current_year)
    DataFrame_stats = explore_building_lengths(DataFrame)
    pie_plot_object = plot_type_distribution(DataFrame)
    #pie_plot_object.show()
    bar_plot_object = plot_age_distribution(DataFrame)
    #bar_plot_object.show()
    general_tupple = from_twentieth_century(DataFrame)
    print(general_tupple)
    mello_ge_schoppernou(DataFrame)
    route_1 = ["Kugelbeerbrücke,Riedbachbrücke"]
    route_2 = ["Bergerbachbrücke"]
    shortest_distance = print_shorter_bridge_distance(DataFrame, route_1, route_2)
    lamp_counter = illuminate_underpasses(DataFrame)
    price_to_pay = renovate_galeries(DataFrame,current_year)
    street = str(input())
    renovate_bridges(DataFrame,street)




