import pandas as pd

demo_seed = pd.read_excel('../DATA/Day05_PlanningSeed.xlsx', sheet_name="seeds")
demo_seed_to_soil = pd.read_excel('../DATA/Day05_PlanningSeed.xlsx', sheet_name="seed_to_soil")
demo_soil_to_fertilizer = pd.read_excel('../DATA/Day05_PlanningSeed.xlsx', sheet_name="soil_to_fertilizer")
demo_fertilizer_to_water = pd.read_excel('../DATA/Day05_PlanningSeed.xlsx', sheet_name="fertilizer_to_water")
demo_water_to_light = pd.read_excel('../DATA/Day05_PlanningSeed.xlsx', sheet_name="water_to_light")
demo_light_to_temperature = pd.read_excel('../DATA/Day05_PlanningSeed.xlsx', sheet_name="light_to_temperature")
demo_temperature_to_humidity = pd.read_excel('../DATA/Day05_PlanningSeed.xlsx', sheet_name="temperature_to_humidity")
demo_humidity_to_location = pd.read_excel('../DATA/Day05_PlanningSeed.xlsx', sheet_name="humidity_to_location")

string_seed = demo_seed.seeds[0]
string_seed = string_seed.split(" ")
seed_to_create = {
    'seed': []
}
for i in range(len(string_seed)):

    if i % 2 == 0:

        value = string_seed[i:i+2]
        start = int(value[0])
        length = int(value[1])
        seed_to_create['seed'].append(list(range(start, start + length)))


seed_df = pd.DataFrame(seed_to_create)
seed_df['seed'] = seed_df['seed'].astype(int)

def ConvertStringToMatchingTable(input_df,
                                 need_to_add_df,
                                 name_source,
                                 name_destination,
                                 column_name):

    matching_dict = {
        'source': [],
        'destination': []
    }

    for i in need_to_add_df[name_source].to_list():

        for index, row in input_df.iterrows():

            string_to_expand = row[column_name]
            string_to_expand = string_to_expand.split(" ")

            start_destination = int(string_to_expand[0])
            start_source = int(string_to_expand[1])
            length = int(string_to_expand[2])
            # list_source = list(range(start_source, start_source + length))

            if (i >= start_source) & (i < start_source + length):

                position = i - start_source
                value_source = start_destination + position
                matching_dict['source'].append(i)
                matching_dict['destination'].append(value_source)
    
    output_df = pd.DataFrame(matching_dict).rename(columns={
        'source': name_source,
        'destination': name_destination
    })

    need_to_add_df = need_to_add_df[~need_to_add_df[name_source].isin(output_df[name_source])]
    need_to_add_df[name_destination] = need_to_add_df[name_source]
    need_to_add_df = need_to_add_df[[name_source, name_destination]]
    
    output_df = pd.concat([output_df, need_to_add_df])

    return output_df

seed_to_soil_df = ConvertStringToMatchingTable(input_df=demo_seed_to_soil,
                                               need_to_add_df=seed_df,
                                               name_source="seed",
                                               name_destination='soil',
                                               column_name='seed_to_soil')

output_seed = seed_df.merge(seed_to_soil_df, on='seed')

print("Successfully join soil")

soil_to_fertilizer_df = ConvertStringToMatchingTable(input_df=demo_soil_to_fertilizer,
                                                need_to_add_df=output_seed,
                                               name_source="soil",
                                               name_destination='fertilizer',
                                               column_name='soil_to_fertilizer')

output_seed = output_seed.merge(soil_to_fertilizer_df, on='soil')

print("Successfully join fertilizer")


fertilizer_to_water_df = ConvertStringToMatchingTable(input_df=demo_fertilizer_to_water,
                                                     need_to_add_df=output_seed,
                                               name_source="fertilizer",
                                               name_destination='water',
                                               column_name='fertilizer_to_water')

output_seed = output_seed.merge(fertilizer_to_water_df, on='fertilizer')

print("Successfully join water")

water_to_light_df = ConvertStringToMatchingTable(input_df=demo_water_to_light,
                                                 need_to_add_df=output_seed,
                                               name_source="water",
                                               name_destination='light',
                                               column_name='water_to_light')

output_seed = output_seed.merge(water_to_light_df, on='water')

print("Successfully join light")

light_to_temperature_df = ConvertStringToMatchingTable(input_df=demo_light_to_temperature,
                                                       need_to_add_df=output_seed,
                                               name_source="light",
                                               name_destination='temperature',
                                               column_name='light_to_temperature')

output_seed = output_seed.merge(light_to_temperature_df, on='light')

print("Successfully join temperature")

temperature_to_humidity_df = ConvertStringToMatchingTable(input_df=demo_temperature_to_humidity,
                                                          need_to_add_df=output_seed,
                                               name_source="temperature",
                                               name_destination='humidity',
                                               column_name='temperature_to_humidity')

output_seed = output_seed.merge(temperature_to_humidity_df, on='temperature')

print("Successfully join humidity")

humidity_to_location_df = ConvertStringToMatchingTable(input_df=demo_humidity_to_location,
                                               need_to_add_df=output_seed,
                                               name_source="humidity",
                                               name_destination='location',
                                               column_name='humidity_to_location')

output_seed = output_seed.merge(humidity_to_location_df, on='humidity')

print("Successfully join location")


print(output_seed.location.min())