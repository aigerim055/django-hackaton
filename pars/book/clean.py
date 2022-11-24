import json 

with open('book.json', 'r+') as f:
    genres_python = json.load(f)
    cleaned_genres = []
    # for i in genres_python:
    #     if not i in cleaned_genres:
    #         cleaned_genres.append(i)
    # print(cleaned_genres)
    print(genres_python)