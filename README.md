# GPTerminal

GPTerminal is a software that interfaces between chatGPT and a live system terminal, enabling AI control of a target system.
*This does not use the API

![Demo](https://github.com/0xdreadnaught/GPTerminal/blob/main/GPTerminal-demo.png)

## Installation

To install GPTerminal, follow these steps:

1. Clone the repository to your local machine.
2. Install the dependencies using `pip install -r requirements.txt`.
3. Run `python GPTerminal.py` to start the application.
4. Authenticate with chatGPT.
5. Press Enter at the prompt to start the runtime loop.

## Usage

GPTerminal can be used to remotely control a system using natural language commands or raw commands. Simply enter your command in the chat interface, and GPTerminal will execute the corresponding action on the target system.

### Example commands

- `ls` - list the files in the current directory.
- `cd /path/to/directory` - change the current directory to the specified path.
- `identify basic system information` - GPT will try as many command variations as possible until it gets the desired response.
- `get the current date using curl and google` - GPT will try as many command variations as possible until it gets the desired response.

## To-do list

- Improve error handling and error messages.
- Add support for different terminals: bash, csh, cmd, etc.
- Identify if GPT is currently talking to a jailed shell.

## Work in progress

- Troubleshooting random sequence tracking failures. This only appears to effect the debug output in the terminal, not what is processed by GPT.

## Known issues

- GPTerminal may freeze or crash if an invalid command is entered.
- GPTerminal currently supports Windows Powershell only.

## License

This software is the property of Brian Peters(aka 0xdreadnaught) and is protected by intellectual property laws. No part of the software may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the owner.

Note that this software is not open source, and the license does not grant any permissions to users. Only those with written consent from the owner may use this software. Any unauthorized use, reproduction, or distribution of this software is strictly prohibited and may result in legal action.

