def getFeedbackFromCodeExecutionPrompt(command, output: str):
    # max length of output is 1000 characters
    output = output[-1000:]

    prompt = f"""your ran the command:{command} and it returned: 
    ```
    {output} 
    ```
    If you find the step to have been successfully executed based on the output, remove it from your list of steps and re-write the next steps that still need to be done. 
    If the step was not successful, create a new list of steps that also includes the steps needed to find a solution and fix it"""

    return prompt
