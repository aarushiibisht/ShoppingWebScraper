from collections import Counter
from Database import add_purchased_items, get_uncategorized_items, create_new_category, update_item_category, \
    get_all_categories, update_category, get_all_keywords


def _categorize_items(purchased_items):
    categories = get_all_categories()
    for item in purchased_items:
        _categorize_item(item, categories)


def _categorize_item(item, categories):
    name = item[1]
    name_keywords = name.lower().split(" ")
    selected_category_id = -1
    max_match = 0
    for (category_id, _) in categories:
        keywords = get_all_keywords(category_id)
        match = _get_match(keywords, name_keywords)
        if match > max_match:
            max_match = match
            selected_category_id = category_id
    item.append(selected_category_id)


def _get_match(keywords, name_keywords):
    c = Counter(name_keywords)
    match = 0
    for (_, k) in keywords:
        if k in c:
            match += c[k]
    return match


def process_data(purchased_items=None):
    if purchased_items:
        _categorize_items(purchased_items)
        add_purchased_items(purchased_items)
    uncategorized_items = get_uncategorized_items()
    for item in uncategorized_items:
        done = False
        while not done:
            user_selection = input(
                "Item " + item[1] + " is uncategorized. To select from existing category, press 1 otherwise press 0: ")
            if user_selection == '1':
                categories = get_all_categories()
                for category in categories:
                    print(str(category[0]) + ":" + category[1])
                category_id = input("Choose the category id:")
                internal_done = False
                while not internal_done:
                    edit = input("Do you want to edit the category? Press y or n: ")
                    if edit == 'y':
                        name = input("Name of the category. Press enter if do not want to update")
                        keywords = input("Enter keywords to add comma seperated: ")
                        update_category(category_id, name, keywords)
                        update_item_category(item, category_id)
                        done = True
                        internal_done = True
                    elif edit == 'n':
                        update_item_category(item, category_id)
                        done = True
                        internal_done = True
                    else:
                        print("Choose either y or n")

            elif user_selection == '0':
                new_category = input("Name of the new category:")
                keywords = input("Enter keywords comma separated: ")
                category_id = create_new_category(new_category, keywords)
                update_item_category(item, category_id)
                done = True
            else:
                print("Incorrect entry")