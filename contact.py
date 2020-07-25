import os
import csv
import re


def csv_processing(file_name):
    pattern = "(\+7\s|8\s|8|\+7)(\(|\s\(|)(\d{3})(|\)|\d{3}|\s\d{3})(\s|\-|)(\d{3}|\d{3}|\d{3})(\-|)(\d{2}|)(\-|)" \
              "(\d{2}|\d{2})(\d{2}|\s\(|\s|)((доб.\s\d{4}|))(\)|)"
    with open(os.path.abspath(file_name), encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        column_lastname = contacts_list[0][0]
        column_firstname = contacts_list[0][1]
        column_middlename = contacts_list[0][2]
        column_organization = contacts_list[0][3]
        column_position = contacts_list[0][4]
        column_phone = contacts_list[0][5]
        column_email = contacts_list[0][6]
        contacts_list.pop(0)
        phone_dict_list = []
        phone_dict = {}
        for data in contacts_list:
            lastname = data[0]
            firstname = data[1]
            middlename = data[2]
            organization = data[3]
            position = data[4]
            phone = data[5]
            email = data[6]
            fio = lastname.split(' ')
            fio_firstname = firstname.split(" ")
            if len(fio) == 3:
                lastname = fio[0]
                firstname = fio[1]
                middlename = fio[2]
            elif len(fio) == 1 and len(fio_firstname) == 2:
                firstname = fio_firstname[0]
                middlename = fio_firstname[1]
            elif len(fio) == 2:
                lastname = fio[0]
                name_middlename = fio[1].split(" ")
                if len(name_middlename) == 2:
                    firstname = name_middlename[0]
                    middlename = name_middlename[1]
                else:
                    firstname = fio[1]
            if lastname + " " + firstname not in phone_dict.keys():
                phone_dict_user = {}
                phone_dict_user['lastname'] = lastname
                phone_dict_user['firstname'] = firstname
                phone_dict_user['middlename'] = middlename
                phone_dict_user['organization'] = organization
                phone_dict_user['position'] = position
                sub_for_phone = re.sub(pattern, r"+7(\3)\6-\8-\10 \13", str(phone))
                phone_dict_user['phone'] = sub_for_phone
                phone_dict_user['email'] = email
                phone_dict[lastname + " " + firstname] = phone_dict_user
            else:
                if not phone_dict[lastname + " " + firstname]['middlename']:
                    phone_dict[lastname + " " + firstname]['middlename'] = middlename
                if not phone_dict[lastname + " " + firstname]['organization']:
                    phone_dict[lastname + " " + firstname]['organization'] == organization
                if not phone_dict[lastname + " " + firstname]['position']:
                    phone_dict[lastname + " " + firstname]['position'] = position
                if not phone_dict[lastname + " " + firstname]['phone']:
                    sub_for_phone = re.sub(pattern, r"+7 \3 \6 \8 \10 \13", str(phone))
                    phone_dict[lastname + " " + firstname]['phone'] = sub_for_phone
                if not phone_dict[lastname + " " + firstname]['email']:
                    phone_dict[lastname + " " + firstname]['email'] = email
        return phone_dict


def csv_writer(file_name, parsed_data):
    with open(file_name, "w", encoding="utf-8") as f:
        fieldnames = ["lastname", "firstname", "middlename", "organization", "position", "phone", "email"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for val in parsed_data:
            writer.writerow(parsed_data[val])
