import pandas as pd
import StringIO

from add_models import (
  add_artist,
  add_artwork,
  add_exhibition,
  add_org,
  add_park
)


def object_table(arg):
  """
  Take in string argument and return relevant add_models function
  """

  set_obj = {
    'exhibition': add_exhibition.add_exhibition,
    'artwork': add_artwork.add_artwork,
    'park': add_park.add_park,
    'artist': add_artist.add_artist,
    'org': add_org.add_org
  }

  return set_obj[arg.lower()]


def read_csv_heads(file):
  """
  Read a CSV file and return a list of column head values

  Receive a CSV file as argument
  Read the file using Pandas, dropping empty columns
  Return CSV column head values as a list of strings
  """

  # Get form data (object type, classes, etc.)
  file_data = pd.read_csv(file, quoting=1)
  # Drop unnamed columns
  file_data.drop(
      file_data.columns[file_data.columns.str.contains('unnamed', case=False)],
      axis=1, inplace=True
  )
  # Return file column names
  return file_data.columns.values


def import_csv(file, obj, cols, vals, match=False):
  """
  Receive a file and column info, add rows to database, return results

  Read the file using Pandas, dropping empty columns
  Loop through file rows
  Create a dict from based on the supplied column mapping
  Add dict to database
  Create a list of dict responses
  Return results

  Keyword arguments:
  file -- CSV file
  obj -- string, determines which DB table to import data 
         (one of 'exhibition', 'artwork', 'park', 'artist', 'org')
  cols -- list of columns to be imported
  vals -- list of matching class attributes to apply col values
  match -- (default = False)
  """

  # Read passed file
  csv_data = pd.read_csv(file, skiprows = 0, na_values = [''], encoding='utf-8')

  # Remove empty rows
  csv_data = csv_data.replace('', pd.np.nan).dropna(how='all')

  # Replace nan values with empty string
  csv_data = csv_data.replace(pd.np.nan, "")

  # Get Object type, store function value
  model_object = object_table(obj)

  # Define result log
  results = []

  # Loop through file rows, create dict to add to database
  for index, row in csv_data.iterrows():
    kwargs = {}
    for col, val in zip(cols, vals):
      # Store val item as key, value of row item as value
      kwargs[val] = row[col].strip()
    # Call relevant function with key/value items
    result = model_object(match=match, **kwargs)
    # Add result dict to results list
    results.append({
      "success": result['success'],
      "result": result['result'],
      "warning": result['warning'],
      "data": result['data'],
    })

  return results


def export_csv(obj):
  """
  Read a JSON object and return a list of column head values
  """

  # Turn argument into dataframe
  df = pd.DataFrame(obj)
  # Store csv in StringIO
  buffer = StringIO.StringIO()
  # Turn dataframe into csv
  csv_file = df.to_csv(buffer,encoding='utf-8')
  buffer.seek(0)
  # Return CSV temp file
  return buffer
