import pandas as pd

#prepare data
def get_data():
    #read data
    df= pd.read_csv("https://gitlab.com/kuziomkin/public-data/-/raw/main/basic-fit-feedback.csv")
    #convert date to datetype
    df["Date"] = pd.to_datetime(df["Date"])
    df["Stars"] = pd.to_numeric(df["Stars"], downcast="float")
    return df


#create address dict function
def create_dic(dataframe):
    city_gp = dataframe.pivot_table(
        values=["Rating"],
        index=None,
        columns=["City", "Address"],
        aggfunc="count"
    )
    ad_dict = {}
    for city in dataframe["City"]:
        ad_list = []
        for n in city_gp[city].axes[1]:
            ad_list.append(n)
        city_dict = {
            city : ad_list
        }
        ad_dict.update(city_dict)
    return ad_dict


#filter data
def filter_data(df, city, address, period):
    if isinstance(city, str):
        city_list = []
        city_list.append(city)
    elif city is None:
        city_list = []
    else:
        city_list = city
    if isinstance(address, str):
        address_list = []
        address_list.append(address)
    elif address is None:
        address_list = []
    else:
        address_list = address

    #filter dataset
    df_filtered = df.loc[
        (df["City"].isin(city_list))
        & (df["Address"].isin(address_list))
        & (df["Date"].dt.year >= period[0] + 2000)
        & (df["Date"].dt.year <= period[1] + 2000)
        ]
    return df_filtered