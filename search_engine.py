import os.path
import retrieve_files as rf
import time


# CMPT 370 Group 6 - Search Engine
# This file takes in user input for gender, category, and subcategory from the GUI
# and returns all items that match all three of these filters in a list format.


def check_for_update():
    """
    Checks if updated data must be downloaded from GoogleDrive
    and if the destination directory is in order
    :return: N/A
    """
    # If the user does not have cache storage yet,
    # Create the directory and populate it with the csv files.
    if not os.path.exists("cache_storage/"):
        rf.main()

    # Check content in cache_storage/ is as expected
    files_present = os.listdir("cache_storage/")
    if len(files_present) != 10:
        rf.main()

    # Calculate the time since the files were last updated
    file_updated = os.path.getmtime("cache_storage/accessories_men_cache.csv")

    # Check if its been over a day (86,400s) since the files were last updated
    time_since_updated = time.time() - file_updated
    if time_since_updated > 86400:
        rf.main()


def search(gender, category, subcategory):
    """
    This function takes in user input for gender, category, and subcategory from the GUI
    and returns all items that match all three of these filters in a list format.
    :param gender: The user's gender input
    :param category: The user's category input
    :param subcategory: The user's subcategory input
    :return: A list of all items that matched the sort filters
    """
    check_for_update()

    database = ["cache_storage/accessories_men_cache.csv",
                "cache_storage/accessories_women_cache.csv",
                "cache_storage/bottoms_men_cache.csv",
                "cache_storage/bottoms_women_cache.csv",
                "cache_storage/footwear_men_cache.csv",
                "cache_storage/footwear_women_cache.csv",
                "cache_storage/overall_men_cache.csv",
                "cache_storage/overall_women_cache.csv",
                "cache_storage/tops_men_cache.csv",
                "cache_storage/tops_women_cache.csv"]

    result_list = []
    # Check if user wants all items from a particular selection parameter
    # Search for all items
    if gender == "All" and category == "All":
        for file in database:
            result_list.append(file)
    # Search for specific category from all genders
    elif gender == "All":
        for file in database:
            result_list.append(file)
            if category.lower() not in file:
                result_list.remove(file)
    # Search for all categories from a specific gender
    elif category == "All":
        for file in database:
            if "_" + gender.lower() in file:
                result_list.append(file)
    # Else, sort by given gender and category
    else:
        for file in database:
            if "_" + gender.lower() in file:
                result_list.append(file)
                if category.lower() not in file:
                    result_list.remove(file)

    # Check subcategories
    results = []
    for i in range(len(result_list)):
        f = open(result_list[i], "r")
        eof = False
        # Skip first line containing header data
        next(f)
        # Read remaining files
        while not eof:
            current_line = f.readline()
            if current_line == "":
                eof = True
            # Search for all subcategories of given category
            elif subcategory == "All":
                results.append(current_line)
            # Else, search for specified subcategory
            else:
                if subcategory.lower() in current_line.lower() or subcategory[0:-1].lower() in current_line.lower():
                    results.append(current_line)

    return results


def main():
    """
    Initialize the file database using the nike.csv files, and then call sort_results().
    For now, I put only the Nike .csv files in for the database, but
    once we have the .csv file merger part of our program done, that will
    become our new database.
    :return: All items that match the desired sort filters in a list format
    """
    results = search("men", "accessories", "socks")
    for i in results:
        print(i)


if __name__ == "__main__":
    main()
