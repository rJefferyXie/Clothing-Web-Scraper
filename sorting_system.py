# 370 Fall 2020: Scraper Software

# This file takes the information returned by the search engine and
# filters it according to specified parameters


import csv
import operator


sample_input = [
    ["Aloha Long Sleeve T-Shirt", "Men", 35.95, "N/A", "WHITE (wht)", "https://www.billabong.com/en-ca/aloha-long-sleeve-t-shirt-194843166303.html", "https://images.boardriders.com/global/billabong-products/all/default/small/m4053bao_billabong,f_wht_frt1.jpg", "mens_tshirts", "Billabong"],
    ["Geo Hawaii T-Shirt", "Men", 29.95, "N/A", "BLACK (blk) || DARK GREY HEATH (dgr)", "https://www.billabong.com/en-ca/geo-hawaii-t-shirt-194843057380.html", "https://images.boardriders.com/global/billabong-products/all/default/small/m4043bgh_billabong,f_blk_frt1.jpg", "mens_tshirts", "Billabong"],
    ["Walled Long Sleeve T-Shirt", "Men", 37.95, "N/A", "COASTAL BLUE (cbu)", "https://www.billabong.com/en-ca/walled-long-sleeve-t-shirt-194843061080.html", "https://images.boardriders.com/global/billabong-products/all/default/small/m4053bwa_billabong,f_cbu_frt1.jpg", "mens_tshirts", "Billabong"],
    ["Flamingo Palm T-Shirt", "Men", 29.95, "N/A", "LIGHT AQUA (laq) || OFF WHITE (ofw)", "https://www.billabong.com/en-ca/flamingo-palm-t-shirt-194843057182.html", "https://images.boardriders.com/global/billabong-products/all/default/small/m4043bfp_billabong,f_laq_frt1.jpg", "mens_tshirts", "Billabong"],
    ["Lines Short Sleeve T-Shirt", "Men", 31.95, "N/A", "CHARCOAL (chr) || SILVER (sil)", "https://www.billabong.com/en-ca/lines-short-sleeve-t-shirt-194843174599.html", "https://images.boardriders.com/global/billabong-products/all/default/small/m4603bvh_billabong,f_chr_frt1.jpg", "mens_tshirts", "Billabong"],
    ["Palm Grinch Short Sleeve T-Shirt", "Men", 39.95, "N/A", "OFF WHITE (ofw)", "https://www.billabong.com/en-ca/palm-grinch-short-sleeve-t-shirt-194843454288.html", "https://images.boardriders.com/global/billabong-products/all/default/small/abyzt00637_billabong,m_ofw_frt1.jpg", "mens_tshirts", "Billabong"]
]


def retrieve_data_as_csv(results_list):
    """
    Converts list generated by search_engine into a csv file
    :return: filename: string attributed to new file
    """
    filename = "results.csv"
    f = csv.writer(open(filename, "w", newline=''))
    for item_data in results_list:
        f.writerow(item_data)
    return filename


# function to sort generated csv file
def sort_results(filename, sorting_key, reversed):
    """

    :return:
    """

    reader = csv.reader(open(filename))

    # Record index associated with each key in original data
    key_indices = {
                    "Name": 0,
                    "Gender": 1,
                    "Price": 2,
                    "Sale Price": 3,
                    "Store": 8
                   }

    initial_list = list(reader)

    # Remove dollar signs  and convert to allow for numerical sorting
    for i in range(len(initial_list)):
        # Covert prices to floats
        if initial_list[i][2][0] == "$":
            initial_list[i][2] = initial_list[i][2].lstrip("$")
        initial_list[i][2] = float(initial_list[i][2])
        try:
            initial_list[i][3] = float(initial_list[i][3])
        except:
            pass

    # sorted created list of lists
    sale_list = [result for result in initial_list if result[3] != "N/A"]
    no_sale_list = [result for result in initial_list if result[3] == "N/A"]
    if sorting_key == "Sale Price":
        sortedlist = sorted(sale_list, key=operator.itemgetter(key_indices[sorting_key]), reverse=reversed)
        sortedlist.extend(no_sale_list)
    else:
        sortedlist = sorted(initial_list, key=operator.itemgetter(key_indices[sorting_key]), reverse=reversed)

    # Divide

    return sortedlist

    # convert back into csv
    # with open("results.csv", "w") as file:
    #     for item in range(0, len(sortedlist)):
    #         for i in sortedlist[item]:
    #             file.write(i)
    #             file.write(", ")
    #         file.write("\n")


# main
def main():
    # data coming from
    file = retrieve_data_as_csv(sample_input)
    sort_results(file, "Price", True)


if __name__ == "__main__":
    main()
