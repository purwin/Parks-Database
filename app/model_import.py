import pandas as pd

from add_models import (
    add_artist,
    add_artwork,
    add_exhibition,
    add_org,
    add_park
)

# import add_models


def object_table(arg):
    set_obj = {
        'exhibition': add_exhibition.add_exhibition,
        'artwork': add_artwork.add_artwork,
        'park': add_park.add_park,
        'artist': add_artist.add_artist,
        'org': add_org.add_org
    }
    return set_obj[arg.lower()]


def import_csv(csv_data, obj, cols, vals, match=False):
    # Remove empty rows
    csv_data = csv_data.replace('', pd.np.nan).dropna(how='all')

    # Replace nan values with empty string
    csv_data = csv_data.replace(pd.np.nan, "")

    # Get Object type, store function value
    model_object = object_table(obj)

    # Define result log
    results = []

    # Loop through file rows, create object to add to database
    for index, row in csv_data.iterrows():
        kwargs = {}
        for col, val in zip(cols, vals):
            # Store val item as key, value of row item as value
            kwargs[val] = row[col].strip()
        # print kwargs
        # Call relevant function with key/value items
        result = model_object(match=match, **kwargs)
        # Add result to results array
        results.append(result['result'])

    print results
    return results


def main(csv_file):
    temp_obj = 'park'
    cols = ['Location', 'Borough']
    vals = ['park_name', 'borough']

    import_csv(csv_file=csv_file, obj=temp_obj, cols=cols, vals=vals)

    # file = pd.read_csv(csv_file)
    # file.drop(file.columns[file.columns.str.contains('unnamed', case=False)],
    #   axis=1, inplace=True)
    # file_headers = file.columns.values
    # print file_headers

    # row_1 = file[1:5]
    # for index, row in row_1.iterrows():
    #   d = {}
    #   for col in file_headers:
    #     d[col] = row[col]
    #   print d


if __name__ == '__main__':
    main('/Users/michaelpurwin/Documents/workings/parks database/data/'
         'CURRENT_Public-Art-Chronology_1.30.2017.csv')
