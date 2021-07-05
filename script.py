import requests, urllib, json

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

def get_colleges(state, program=1, method="fetchdata", year="2020-2021", level=1, institutiontype=1, Women=1, Minority=1, course=1):
    state = urllib.parse.quote_plus(state)
    url = f"https://facilities.aicte-india.org/dashboard/pages/php/approvedinstituteserver.php?method={method}&year={year}&program={program}&level={level}&institutiontype={institutiontype}&Women={Women}&Minority={Minority}&state={state}&course={course}"
    resp = requests.get(url).json()
    return resp

def get_college_details(aicteid):
    url = f"https://facilities.aicte-india.org/dashboard/pages/php/approvedcourse.php?method=fetchdata&aicteid=/{aicteid}/&course=/1/&year=/2020-2021/"
    resp = requests.get(url).json()
    return resp

for state in states:
    records = get_colleges(state=states[state])
    filename = f"{state}.json"
    data = {states[state]: []}
    if records:
        for record in records:
            aicte_id = record[0]
            college_details = get_college_details(aicteid=aicte_id)
            college = {
                record[1]: {
                    "address": record[2],
                    "district": record[3],
                    "institution_type": record[4],
                    "course_details": []
                }
            }
            for course in college_details:
                course_details = {}
                course_details['programme'] = course[3]
                course_details['level'] = course[5]
                course_details['course'] = course[6]
                college[record[1]]['course_details'].append(course_details)
            print(college)
            data[states[state]].append(college)
        
    with open(filename, "w") as f:
        f.write(json.dumps(data))
