def getPlanMessage(plan: str):
    if plan == "":
        return None

    message = {
        "role": "system",
        "content": f"""This is your current plan:
```
{plan}
```
""",
    }

    return message
