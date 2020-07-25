from contact import csv_writer, csv_processing


if __name__ == "__main__":
    csv_writer("phonebook_parsed.csv", csv_processing("phonebook.csv"))
    print("Контакты записной книги унифицированы и записаны в файл!")