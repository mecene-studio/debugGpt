# DebugGpt

DebugGpt is a Python application that uses AI to automatically debug Next.js apps. Specifically, it is designed to debug the test-app.

![Example answer from debugGPT](https://lh3.googleusercontent.com/pw/AJFCJaW0mQLlluV-6hiHo7xnP-zETVKt62tZIrxNheR3AHB_VMKJ313d8nKplCyZigR_3Ti8MCJqCpiuDgqt6FjPRPiJDs3IY1Q9SDX4HHr34jk_co1e3_WlVF5ztk9hBwA9rV_U5w-0AK3WuM0NkJ4WOBmB=w567-h229-s-no?authuser=0)

## Demo

Watch this youtube video to understand how it works:

[![DebugGPT Youtube video](http://img.youtube.com/vi/nUVBSC6gTic/0.jpg)](http://www.youtube.com/watch?v=nUVBSC6gTic "I Built DebugGPT")

## Installation

To install DebugGpt, follow these steps:
1. Clone the repository to your local machine
2. Install the required dependencies by running `pip install -r requirements.txt`
3. Rename the .env.example to .env and add the variables
4. Install Node.js 18 for the test app

## Usage

To use DebugGpt, follow these steps:

1. Navigate to the root/src directory of the DebugGpt application.
2. Run the command `python main.py`.
3. DebugGpt will automatically analyze the test-app and provide and fix any errors or issues it finds.
4. More levels are available in levels/. Switch what's in the test-app/components/ folder.

## Contributing

If you would like to contribute to DebugGpt, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and commit them with clear and concise commit messages.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

## License

DebugGpt is licensed under the MIT License. See the LICENSE file for more information.