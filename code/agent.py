import sys
sys.path.append('../')

from py_expression_eval import Parser
import requests
import json
import re,time,os
import sys
from util.sys_prompt import system_prompt
from openai import OpenAI


client = OpenAI()

google_maps_api_key=os.environ['GOOGLE_MAPS_API_KEY']

def mapshelp(source, destination,mode,api_key=google_maps_api_key):
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={source}&destination={destination}&key={api_key}&mode={mode}'
    response = requests.get(url)
    data = response.json()
    #print(data['routes'][0])
    if data['status'] == 'OK':
        travel_time = data['routes'][0]['legs'][0]['duration']['text']
        print(f"Live travel time from {source} to {destination} is {travel_time}")
    else:
        print(response)
        print(response.text)
        print("Error in retrieving travel time information.")
    
    return travel_time

parser = Parser()
def calculator(str):
    return parser.parse(str).evaluate({})

def Stream_agent(prompt):
    
    def extract_action_and_input(text):
        action_pattern= r"Action: (.+?)\n"
        action= re.findall(action_pattern,text)

        if action[-1]=="Maps":
            input_pattern= r'Action Input: \{"source":"[^"]+","destination":"[^"]+","mode":"[^"]+"\}'
            action_input= re.findall(input_pattern,text)
            action_input=json.loads(action_input[0].split(": ")[-1])
        else:
            input_pattern = r"Action Input: .*"
            action_input = re.findall(input_pattern, text)
            #print(f"Action input is {action_input}")
                
        return action, action_input
    
    

    messages=[{"role":"system","content":system_prompt},{"role":"user","content":prompt}]
    last_response=""
    while True:
    
        response_text = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        seed=123,
        max_tokens=1000,  # Adjust the max tokens as needed
        temperature=0,
        top_p=1
        
    )
        response_text=response_text.choices[0].message.content
        print(response_text)
        print("\n")
        time.sleep(20)
        action,action_input=extract_action_and_input(response_text)
        #print(action,action_input)
        if action[-1]=="Maps":
            tool= mapshelp
            observation=tool(**action_input)
        elif action[-1]=="Calculator":
            tool= calculator
            observation = tool(action_input[-1].split(":")[-1])

        elif action[-1]=="Response To Human":
            print(f"Response: {action_input[-1]}")
            #sys.exit()
            break
        
        
        print("Observation: ", observation)
        messages.extend([{"role":"system","content":response_text},
                         {"role":"user","content":f"Observation: {observation}"},])

    


Stream_agent("I live in Sydney. Assuming the live travel time between Gordon and Wynyard right now is x, calculate 5 times x minus 10")
# Stream_agent("I live in Gordon, Sydney. I have a decision to make and I need your help.\
#  I can buy an iphone either from Chatswood,Penrith or Schofields. \
#  My objective is to minimize the total cost involved. \
#  The cost incurred to travel to a location is x*5 dollar where x is the travel time to the place in minutes. \
#  Cost of iphone in chatswood is $1230,cost of iphone in schofields is $1120 and cost of iphone in penirth is $1090.\
#   And I can only walk to schofields. Where should I buy the iphone?")



