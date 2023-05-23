def getFeedbackFromCodeExecutionPrompt(command, output):
    # max length of output is 1000 characters
    output = output[-1000:]

    prompt = f"""You executed the command `{command}`.
this is the output 

```{output}
```

What is the next command you would like to execute?
Answer with the command only and nothing else.
"""

    return output
