import pandas as pd

# books = pd.read_csv('Books.csv')
# ratings = pd.read_csv('Ratings.csv')
# users = pd.read_csv('Users.csv')

# print(books.head(10))

# users = pd.read_csv('Users.csv', nrows=10, error_bad_lines=False, warn_bad_lines=True, sep=';')
# # print(users)

# books = pd.read_csv('Books.csv', nrows=10, error_bad_lines=False, warn_bad_lines=True, sep=';')


ratings = pd.read_csv('Ratings.csv', nrows=10, error_bad_lines=False, warn_bad_lines=True, sep=';')
print(ratings.columns)    
# ik wil op basis van leeftijd, geslacht, opleidingsniveau, regio, eerder gelezen boeken, interesses in boeken/genres aanbevelingen maken hoe doe ik dat
