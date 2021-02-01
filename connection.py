import csv

def read_data(filename):
    with open (filename, "r") as file:
        data = csv.reader(file, delimiter=",")
        first_line = True
        header = []
        posts = []
        post = {}
        for row in data:
            if not first_line:
                for i in range(len(header)):
                    post[header[i]] = row[i]
                posts.append(post)
            else:
                for item in row:
                    header.append(item)
                first_line = False
        return posts, header


def write_data(filename, posts, header):
    with open (filename, "w") as file:
        data = csv.writer(file, delimiter=",")
        data.writerow(header)
        for post in posts:
            row = []
            for i in range(len(header)):
                row.append(post[header[i]])
            data.writerow(row)
