import pandas as pd;

file_path = 'IMDB_Netflix_Original_Movies_Data.xlsx';
data = pd.read_excel(file_path, sheet_name = 'Edited_Data', engine='openpyxl');

column_data = data['Genres'];

# Create a blank list of unique genres
unique_genres = []

# Iterate through every genre in every cell to add unique ones
# not already in the 'unique_genres' list
for item in column_data:
    if isinstance(item, str):
        split_data = item.split(",")
        for genre in split_data:
            if genre.strip() in unique_genres:
                pass;
            else:
                unique_genres.append(genre.strip());

# Add new columns that say whether or not it has a genre
for genre in unique_genres:
    data[f'is_{genre}'] = 'Default Value'

for index, row in data.iterrows():
    if isinstance(row['Genres'], str):
        genres_in_row = [genre.strip() for genre in row['Genres'].split(',')]
        for genre in unique_genres:
            if genre in genres_in_row:
                data.at[index, f'is_{genre}'] = 'True'
            else:
                data.at[index, f'is_{genre}'] = 'False'
        

data.to_excel("updated_excel_file.xlsx", index=False)