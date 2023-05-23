from agents.agent import JuniorDev


def testJuniorDev():
    prompt = "build the application and fix any errors"
    agent = JuniorDev()
    answer = agent.startLoop(prompt)
    print("answer:", answer)


if __name__ == "__main__":
    testJuniorDev()
