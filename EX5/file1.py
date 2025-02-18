import pandas as pd
import os


def write_txt(filename, content):
    with open(filename, "w") as f:
        f.writelines(content)


if __name__ == "__main__":
    df = pd.read_excel("data/tshekid_office2003.xls")

    carts = []
    last_customer = 0
    current_cart = ""
    for index, row in df.iterrows():
        customer = row["ostja"]
        product = row["kaup"].lower().replace(", ", "/").replace(" ", "_")

        if customer != last_customer:
            if last_customer != 0:
                current_cart += "\n"
                carts.append(current_cart)
            last_customer = customer
            current_cart = product
        else:
            current_cart += f" {product}"

    write_txt("input1.txt", carts)

    os.system("./apriori input1.txt output1.txt ")
