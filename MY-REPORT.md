![GenI-Banner](https://github.com/genilab-fau/genial-fau.github.io/blob/8f1a2d3523f879e1082918c7bba19553cb6e7212/images/geni-lab-banner.png?raw=true)

# Simulated GenAI Pipeline for Prompt Engineering in Generative AI Models  or GenAI Experimentation Pipeline 

This research explores techniques to enhance prompt engineering and response generation in large language models (LLMs), specifically focusing on the creation, testing, and refinement of prompts in a simulated environment.



* Authors: [RojaMayuri](Rpottepalli2024@fau.edu)
* Academic Supervisor: [Dr. Fernando Koch](http://www.fernandokoch.me)

  
# Research Question 

How can different prompt engineering techniques be utilized to improve the performance and response quality of generative AI systems, especially in the context of software requirement analysis?

## Arguments

#### What is already known about this topic

*  Generative AI models like LLMs (e.g., OpenAI, Llama) can generate text-based outputs based on user-defined prompts.
* The challenges of creating highly specific prompts that align with the task at hand.
* The possibility of chaining multiple prompt engineering techniques to improve model outputs.

#### What this research is exploring


* We employ advanced techniques like zero-shot, few-shot, chain-of-thought, and automated prompt generation.
* We are building a robust pipeline to test and experiment with these techniques.
* We are exploring the potential for prompt engineering to automate requirement analysis in software development.

#### Implications for practice



* It will be easier to automate software requirement analysis using AI.
* It will optimize the generation of functional and non-functional requirements.
* We will better understand how different prompt structures influence the quality and relevance of model responses.


# Research Method

Describe how you are building this research process.

The research builds upon a pipeline for interacting with AI models using various prompt engineering techniques. Key stages in the process include:

1. Loading Configuration: Configuration files are dynamically loaded from various locations to set up the environment.
2. Creating Payloads: The create_payload function builds a request payload in the format required by the target AI model (e.g., Ollama or Open-WebUI).
3. Model Request Handling: The model_req function sends the generated payload to the model server, handles the request, and processes the response.
4. Response Handling and Cleanup: The clean_json_response function attempts to clean and extract valid JSON from the model's response. Any invalid JSON formats are addressed with robust error handling.
5. Experimentation: The pipeline supports various techniques (zero-shot, few-shot, chain-of-thought) to analyze their effectiveness in generating relevant software requirements.

# Results

The research process focused on automating the extraction of functional and non-functional requirements from user stories using AI models. The results achieved include:

1. Zero-Shot Responses: The model generally provided the expected output, but inconsistencies in format occasionally emerged. This was especially the case when the model added unnecessary explanation or failed to strictly follow the required JSON structure.

2. Few-Shot Responses: By providing example input-output pairs, the model often returned the correct output in JSON format. However, extraneous text could still be included, which led to minor formatting issues.

3. Chain-of-Thought (CoT) Responses: This technique showed promise in helping the model break down the requirement extraction process, but it sometimes resulted in additional steps that weren’t necessary for the direct extraction of requirements. This increased verbosity and reduced output efficiency.

4. Automated Prompting: The generated prompts for requirement extraction were appropriate, but they failed to consistently return the expected JSON structure. Instead, the model offered unrelated questions that didn’t align with the intended task.

In summary, the results indicate that while the model can generate useful prompts and responses, refinement is necessary to ensure that the output adheres strictly to the desired format. Post-processing or filtering may also be required to clean up the output.

# Further research

1. Formatting and Output Control: Enhance the model’s ability to follow output formatting guidelines by exploring prompt engineering or temperature adjustments.

2.Feedback Loops and Self-Correction: Introduce feedback mechanisms to allow the model to detect and fix formatting errors, improving consistency.

3.Error-Handling Integration: Develop systems that automatically detect errors (e.g., invalid JSON) and trigger corrections.

4.0Fine-tuning for Specific Tasks: Train the model on a dataset focused on software requirements to improve accuracy in requirement extraction.

5.UX Optimization: Adapt the model’s behavior to improve clarity and focus when extracting requirements, minimizing unnecessary details.
