import requests, urllib, json, os, time

duration = 0.1
freq = 500

states = {
    "AN":"Andaman and Nicobar Islands",
    "AP":"Andhra Pradesh",
    "AR":"Arunachal Pradesh",
    "AS":"Assam",
    "BR":"Bihar",
    "CH":"Chandigarh",
    "CG":"Chhattisgarh",
    "DN":"Dadra and Nagar Haveli",
    "DD":"Daman and Diu",
    "DL":"Delhi",
    "GA":"Goa",
    "GJ":"Gujarat",
    "HR":"Haryana",
    "HP":"Himachal Pradesh",
    "JK":"Jammu and Kashmir",
    "JH":"Jharkhand",
    "KA":"Karnataka",
    "KL":"Kerala",
    "LA":"Ladakh",
    "LD":"Lakshadweep",
    "MP":"Madhya Pradesh",
    "MH":"Maharashtra",
    "MN":"Manipur",
    "ML":"Meghalaya",
    "MZ":"Mizoram",
    "NL":"Nagaland",
    "OD":"Odisha",
    "PY":"Puducherry",
    "PB":"Punjab",
    "RJ":"Rajasthan",
    "SK":"Sikkim",
    "TN":"Tamil Nadu",
    "TS":"Telangana",
    "TR":"Tripura",
    "UP":"Uttar Pradesh",
    "UK":"Uttarakhand",
    "WB":"West Bengal"
}

years = [
    "2014-2015",
    "2015-2016",
    "2016-2017",
    "2017-2018",
    "2018-2019",
    "2019-2020",
    "2020-2021"
]

def get_colleges(state, program=1, method="fetchdata", year="2020-2021", level=1, institutiontype=1, Women=1, Minority=1, course=1):
    state = urllib.parse.quote_plus(state)
    url = f"https://facilities.aicte-india.org/dashboard/pages/php/approvedinstituteserver.php?method={method}&year={year}&program={program}&level={level}&institutiontype={institutiontype}&Women={Women}&Minority={Minority}&state={state}&course={course}"
    # print(url)
    resp = requests.get(url).json()
    return resp

def get_college_details(aicteid, year):
    url = f"https://facilities.aicte-india.org/dashboard/pages/php/approvedcourse.php?method=fetchdata&aicteid=/{aicteid}/&course=/1/&year=/{year}/"
    # print(url)
    resp = requests.get(url).json()
    return resp

count = 1
for state in states:
    filename = f"{state}.json"
    print("--------------------------------------------------\n", states[state])
    data = {states[state]: {"id": {}}}
    for year in years:
        records = get_colleges(state=states[state], year=year)
        # time.sleep(1)
        if records is not None:
            print(len(records))
            i = 1
            for record in records:
                try:
                    aicte_id = record[0]
                    college_details = get_college_details(aicteid=aicte_id, year=year)
                    # time.sleep(1)
                    if college_details is None:
                        continue
                    _name = record[1]
                    if _name not in data[states[state]]:
                        data[states[state]][_name] = {
                            "address": record[2],
                            "district": record[3],
                            "institution_type": record[4],
                            "course_details": []
                        }
                    for course in college_details:
                        try:
                            # print(course)
                            _id = f"{record[1]}`{course[3]}`{course[5]}`{course[6]}"
                            if _id in data[states[state]]["id"].keys():
                                continue
                            data[states[state]]["id"][_id] = 1
                            course_details = {
                                "programme": course[3],
                                "level": course[5],
                                "course": course[6]
                            }
                            data[states[state]][_name]['course_details'].append(course_details)
                        except:
                            continue
                except:
                    continue
                print(count, "\t", i, "\t", year, "\t", state, "\t", _name)
                os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
                # print("\a")
                i += 1
                count += 1
            print()

    with open(filename, "w") as f:
        f.write(json.dumps(data))
