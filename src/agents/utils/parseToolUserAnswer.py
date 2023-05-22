def parseToolUserAnswer(answer):
    # writeFile(components/LandingPage.tsx, ```import React from "react";
    # import s from "./LandingPage.module.scss";

    # const LandingPage = () => {
    # return (
    #     <div className={s.container}>
    #         <span>hello</span>
    #     </div>
    # );
    # };

    # export default LandingPage;
    # ```)
    functionName, arguments = answer.split("(", 1)
    arguments = arguments[:-1]
    arguments = arguments.split(",", 1)

    for i in range(len(arguments)):
        arguments[i] = arguments[i].strip()

    return functionName, arguments
