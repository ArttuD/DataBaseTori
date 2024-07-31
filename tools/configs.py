
import numpy as np
import matplotlib.pyplot as plt


class properties_items:
    
    class info_items():
        TYPE_ = ["Sell", "Buy", "Give"]
        header = None
        section = ["antique_and_art", "car_boat_and_motocycle equipment", "Electronics_and_appliance",
                   "funiture_and_decor", "home_garden_and_building", "children_and_parrents",
                   "business_and_services", "sports_and_outdoor", "clothes_cosmetics_and_accesory",
                   "entertaiment_and_hobby"]
        description = None
        picture = ["png", "jpg", "jpeg"]
        price = [0, 10000]
        len_postal_code = 5
        condition = ["new", "as new", "good", "moderate", "repair required"]

    class user():

        len_password = 10
        len_postal_code = 5
        

