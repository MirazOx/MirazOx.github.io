import json

with open('content/academic.json', 'r') as f:
    data = json.load(f)

for category in data['courseGroups']:
    for course in category['courses']:
        if course.get('code') == 'NSC4182':
            course['resources'] = [
                {
                    "type": "pdf",
                    "title": "The Architecture of Logic: Learning Outcomes",
                    "url": "/assets/showcase/Mathematics_Learning_Outcomes.pdf"
                }
            ]
            course['workTitle'] = "The Architecture of Logic: Learning Outcomes"
            course['type'] = "Curriculum Document"

with open('content/academic.json', 'w') as f:
    json.dump(data, f, indent=2)
