

class properties_items:
    
    class info_items():
        TYPE_ = ["sell", "buy", "give"]
        header = None
        section = ["antique_and_art", "car_boat_and_motocycle equipment", "Electronics_and_appliance",
                   "funiture_and_decor", "home_garden_and_building", "children_and_parrents",
                   "business_and_services", "sports_and_outdoor", "clothes_cosmetics_and_accesory",
                   "entertaiment_and_hobby"]
        description = None
        picture = None
        price = [0, 10000]
        len_postal_code = 5
        condition = ["new", "as new", "good", "moderate", "repair required"]

    class user():
        len_name = 2
        len_password = 8
        len_postal_code = 5
        len_phone_number = 10
        gender = ["male", "female", "other"]
