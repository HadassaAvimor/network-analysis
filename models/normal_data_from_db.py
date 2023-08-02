def normal_communication(communications):
    organize_dict = {}
    for communication in communications:
        if communication["source"] in organize_dict:
            organize_dict[communication["source"]].append(communication["destination"])
        else:
            organize_dict[communication["source"]] = [communication["destination"]]
    return organize_dict


def normal_network_details(data_from_db):
    organize_data = {"Date": data_from_db[0][0], "Location": data_from_db[0][1], "client": data_from_db[0][2]}
    devices = []
    for i in data_from_db:
        devices.append((i[3], i[4]))
    organize_data["Devices"] = set(devices)
    communication = [(i[5], i[6]) for i in data_from_db]
    organize_data["communication"] = [sub for sub in communication if not all(ele is None for ele in sub)]
    return organize_data
