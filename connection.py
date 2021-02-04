import csv


def read_data(filename):
    with open(filename, "r") as file:
        data = csv.reader(file, delimiter=",")
        first_line = True
        header = []
        posts = []
        for row in data:
            if not first_line:
                posts.append(read_row_data(header, row))
            else:
                for item in row:
                    header.append(item)
                first_line = False
        return posts, header


def read_row_data(header, row):
    post = {}
    for i in range(len(header)):
        post[header[i]] = row[i]
    return post


def write_data(filename, posts, header):
    with open(filename, "w") as file:
        data = csv.writer(file, delimiter=",")
        data.writerow(header)
        for post in posts:
            row = []
            for i in range(len(header)):
                row.append(post[header[i]])
            data.writerow(row)
