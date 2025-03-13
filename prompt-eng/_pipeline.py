##
## Prompt Engineering Lab
## Platform for Education and Experimentation with Prompt NEngineering in Generative Intelligent Systems
## _pipeline.py :: Simulated GenAI Pipeline 
## 
#  
# Copyright (c) 2025 Dr. Fernando Koch, The Generative Intelligence Lab @ FAU
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# Documentation and Getting Started:
#    https://github.com/GenILab-FAU/prompt-eng
#
# Disclaimer: 
# Generative AI has been used extensively while developing this package.
# 


import requests
import json
import os
import time
import re

def load_config():
    """
    Load config file looking into multiple locations
    """
    config_locations = [
        "./_config",
        "prompt-eng/_config",
        "../_config"
    ]
    
    # Find CONFIG
    config_path = None
    for location in config_locations:
        if os.path.exists(location):
            config_path = location
            break
    
    if not config_path:
        raise FileNotFoundError("Configuration file not found in any of the expected locations.")
    
    # Load CONFIG
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()


def create_payload(model, prompt, target="ollama", **kwargs):
    """
    Create the Request Payload in the format required byt the Model Server
    @NOTE: 
    Need to adjust here to support multiple target formats
    target can be only ('ollama' or 'open-webui')

    @TODO it should be able to self_discover the target Model Server
    [Issue 1](https://github.com/genilab-fau/prompt-eng/issues/1)
    """

    payload = None
    if target == "ollama":
        payload = {
            "model": model,
            "prompt": prompt, 
            "stream": False,
        }
        if kwargs:
            payload["options"] = {key: value for key, value in kwargs.items()}

    elif target == "open-webui":
        '''
        @TODO need to verify the format for 'parameters' for 'open-webui' is correct.
        [Issue 2](https://github.com/genilab-fau/prompt-eng/issues/2)
        '''
        payload = {
            "model": model,
            "messages": [ {"role" : "user", "content": prompt } ]
        }

        # @NOTE: Taking not of the syntaxes we tested before; none seems to work so far 
        #payload.update({key: value for key, value in kwargs.items()})
        #if kwargs:
        #   payload["options"] = {key: value for key, value in kwargs.items()}
        
    else:
        print(f'!!ERROR!! Unknown target: {target}')
    return payload


def model_req(payload=None):
    """
    Issue request to the Model Server
    """
        
    # CUT-SHORT Condition
    try:
        load_config()
    except:
        return -1, f"!!ERROR!! Problem loading prompt-eng/_config"

    url = os.getenv('URL_GENERATE', None)
    api_key = os.getenv('API_KEY', None)
    delta = response = None

    headers = dict()
    headers["Content-Type"] = "application/json"
    if api_key: headers["Authorization"] = f"Bearer {api_key}"

    #print(url, headers)
    print(payload)

    # Send out request to Model Provider
    try:
        start_time = time.time()
        response = requests.post(url, data=json.dumps(payload) if payload else None, headers=headers)
        delta = time.time() - start_time
    except:
        return -1, f"!!ERROR!! Request failed! You need to adjust prompt-eng/config with URL({url})"

    # Checking the response and extracting the 'response' field
    if response is None:
        return -1, f"!!ERROR!! There was no response (?)"
    elif response.status_code == 200:

        ## @NOTE: Need to adjust here to support multiple response formats
        result = ""
        delta = round(delta, 3)

        response_json = response.json()
        if 'response' in response_json: ## ollama
            result = response_json['response']
        elif 'choices' in response_json: ## open-webui
            result = response_json['choices'][0]['message']['content']
        else:
            try:
                result = json.dumps(response_json, indent=2) # Try to pretty-print JSON response
            except:
                result = str(response_json) # If that fails, convert to string
            print("Warning: Unknown response format. Check the model server documentation.")
       
        return delta, result
    elif response.status_code == 401:
        return -1, f"!!ERROR!! Authentication issue. You need to adjust prompt-eng/config with API_KEY ({url})"
    else:
        return -1, f"!!ERROR!! HTTP Response={response.status_code}, {response.text}"
    return

# Enhanced Prompt Templates with explicit JSON structure requests
PROMPTS = {
    "zero_shot": """You are an AI assistant for software requirement analyst. Extract functional and non-functional requirements from the following user story.  Provide the output in JSON format with "functional" and "non_functional" keys, each containing a list of strings.
    The JSON must be a valid JSON object with two keys: "functional" and "non_functional".  Each key should have a value that is a JSON array of strings.
    The JSON should have the following format:

    ```json
    {{
        Extract functional requirements", "Extract non-functional requirements", "Summarize key features"
    }}
    ```
    user story: {input}""",

    "few_shot": """
    You are a meticulous software requirements analyst. Extract highly specific and actionable functional and non-functional requirements from the following description and return them as valid JSON.  Do NOT include any other text in your response.  Just the JSON.

    The JSON must be a valid JSON object with two keys: "functional" and "non_functional".  Each key should have a value that is a JSON array of strings.

    Example 1:
    user story: A mobile banking app.
    {{
      "functional": ["Users can transfer money", "Users can check balance"],
      "non_functional": ["Security: Multi-factor authentication", "Performance: Fast processing"]
    }}

    Now analyze: {input}""",

    "cot": """Step-by-step requirement analysis:
    You are an AI assistant for software requirement analysis.  Your ONLY job is to extract functional and non-functional requirements from the following description and return them as valid JSON.  Do NOT include any other text in your response.  Just the JSON.

    The JSON must be a valid JSON object with two keys: "functional" and "non_functional".  Each key should have a value that is a JSON array of strings.

    1. Identify key features.
    2. Separate functional and non-functional needs.
    3. Format output in JSON with "functional" and "non_functional" keys, each containing a list of strings.

    Project Description: {input}""",

    "automated_prompt": """
    You are an AI assistant for software requirement analysis.  Your ONLY job is to generate three different prompts for requirement extraction from the following description.  Return the prompts as a valid JSON array of strings. Do NOT include any other text in your response.  Just the JSON.

    Example:
    ```json
    [
      "Prompt 1",
      "Prompt 2",
      "Prompt 3"
    ]
    ```

    Description: {input}
    """ 
}
def remove_trailing_commas(json_string):
    """Removes trailing commas from a JSON string."""
    json_string = re.sub(r',\s*([\]\}])', r'\1', json_string) # Remove trailing commas in objects and arrays
    return json_string

def clean_json_response(response):
    """Cleans the LLM's response to extract valid JSON (Improved)."""
    try:
        # Attempt direct parsing (unlikely to succeed, but worth a try)
        json.loads(response)
        return response

    except json.JSONDecodeError:
        # More Robust Regex Extraction (Handles more variations)
        match = re.search(r"\{.*\}", response, re.DOTALL)  # Find JSON object
        if match:
            json_string = match.group(0)

            # Remove backticks and "json" from code blocks (if present)
            json_string = json_string.replace("```json", "").replace("```", "")
            json_string = json_string.strip() # Remove leading/trailing whitespace

            # *** Trailing Comma Removal ***
            json_string = remove_trailing_commas(json_string)
            
            try:
                json.loads(json_string)  # Check if extracted part is valid
                return json_string

            except json.JSONDecodeError as e:
                print(f"Extracted JSON is still invalid: {json_string}")
                print(f"JSONDecodeError: {e}") # Print specific error
                return None

        else:
            print("No JSON found in response.")
            return None
        
# Call AI Model with error handling and JSON parsing
def call_model(model, prompt, temperature=0.7, max_tokens=500):
    try:
        payload = create_payload(
            target="open-webui",  
            model=model,  
            prompt=prompt,  
            temperature=temperature,  # Set temperature
            num_ctx=100,  # Set maximum context length
            num_predict=100  # Set number of tokens to generate
        )

        # Use the model_req function to send the request
        response_time, response = model_req(payload=payload) 
        cleaned_response = clean_json_response(response)
        if cleaned_response is None:  # Check if cleaning failed
            print(f"Error: Could not clean JSON response. Raw response: {response}")
            return None

        return json.loads(cleaned_response)
        #return json.loads(response)# Return raw string if JSON parsing fails
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Problematic Response: {response}") 
        return None 
    except requests.exceptions.RequestException as e:
        print(f"Error calling model: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# Experiment with Chained Prompting
def chain_prompting(model, input_text):
    initial_output = call_model(model, PROMPTS["zero_shot"].format(input=input_text))
    if isinstance(initial_output, dict): # Check if initial output is a dict
      refined_prompt = PROMPTS["cot"].format(input=input_text) + f"\n\nInitial Analysis: {json.dumps(initial_output)}" # Convert dict to JSON string
    else:
      refined_prompt = PROMPTS["cot"].format(input=input_text) + f"\n\nInitial Analysis: {initial_output}" # Use raw string if it's not a dict
    return call_model(model, refined_prompt)

# Experiment Runner
def run_experiment(model="Llama-3.2-3B-Instruct", technique="zero_shot", input_text="A CRM system for customer tracking.", temperature=0.7):
    prompt = PROMPTS[technique].format(input=input_text)
    start_time = time.time()
    result = call_model(model, prompt, temperature=temperature)
    elapsed_time = time.time() - start_time
    return {"technique": technique, "result": result, "time": elapsed_time}

###
### DEBUG
###

if __name__ == "__main__":
    #test_input = "As a user, I want to be able to control the living room lights with my voice. I also want the lights to automatically turn on when I enter the room and off when I leave. The system should be secure and prevent unauthorized access. It should also be reliable and work even if the internet connection is down.  The system should integrate with my existing smart thermostat.  I want to be able to set schedules for the lights and thermostat.  The system should be easy to use and configure. I'd like to receive notifications on my phone if there's a security alert (e.g., door opened).  The system should be energy efficient."
    test_input = "A system for managing library resources, including books, journals, and digital media."
    from _pipeline import create_payload, model_req
    
    experiments = []
    for technique in PROMPTS.keys():
        experiments.append(run_experiment(technique=technique, input_text=test_input))

    # Chained Experiment
    chain_result = chain_prompting("Llama-3.2-3B-Instruct", test_input)

    # Output Results with JSON formatting if possible
    for exp in experiments:
        print(f"\nTechnique: {exp['technique']}\nTime Taken: {exp['time']:.2f}s")


