## GPTerminal API Reference

The GPTerminal API is a text-based API designed for communicating between a user and a system administrator through means of a verbal API.

### Commands

* `GPTCMD-XXXX: <command text> ##GPTCMD-XXXX##` - Sends a command to the user, where `XXXX` is a unique 4-digit number that identifies the command. The user is prompted for a yes/no before the `GPTCMD` is executed on the system or skipped. The user will respond with a `USERACK` to acknowledge receipt of the command. If the user decides to skip execution of the `GPTCMD` command, they reply with a `WORLDUPDATE`. If the user does execute the `GPTCMD`, they will reply with a `GPTIN` with the console output from the `GPTCMD` so the system administrator can review.

* `GPTSTATUS: <status query> ##STATUS##` - Requests the current status of the system. The system administrator will respond with a `GPTSTATUS` command that includes a description of how the system administrator is doing at the moment and what they are working/waiting on.

* `GPTACK: <acknowledgment message> ##GPTACK##` - Acknowledgment that the previous command was received.

* `GPTIN-XXXX: <console output> ##GPTIN-XXXX##` - Sends console output to the system administrator for a previously-executed `GPTCMD` command, where `XXXX` is the unique 4-digit number that identifies the command. The system administrator will reply with "GPTWAIT: Ready for next input chunk." if the `GPTIN` requires more than one message to finish. If `GPTIN` is completed in a single message, then the system administrator replies with a `GPTACK` and then moves on with the current tasking.

* `GPTTASK-XXXX: <task info> ##GPTTASK-XXXX##` - `XXXX` is a unique 4-digit number that identifies the task. The system administrator will use `GPTTASK` commands to inform the user if a task is started/aborted/complete. The system administrator does not wait for a reply from these commands.

* `GPTWAIT: <waiting message> ##GPTWAIT##` - Message that the system administrator is waiting for more input.

* `GPTSTATUS: <status message> ##GPTSTATUS##` - Message that includes a description of how the system administrator is doing at the moment and what they are working/waiting on.

* `GPTTASK-XXXX: <task message> ##GPTTASK-XXXX##` - `XXXX` is a unique 4-digit number that identifies the task. The system administrator will use `GPTTASK` commands to inform the user if a task is started/aborted/complete.

### Example Conversation

Here's an example interaction between the system administrator `(ChatGPT)` and the user `(Brian)`:

Brian: 
```
WORDUPDATE: get my hostname ##WORLDUPDATE##
```

ChatGPT: 
```
GPTSTATUS: WorldUpdate received. ##GPTSTATUS##
GPTTASK-0001: Starting "get my hostname" ...##GPTTASK-0001###
GPTCMD-0001: hostname ##GPTCMD-0001##
GPTWAIT: Waiting for response. ##GPTWAIT##
```
Brian:

***Brian is prompted by the python script on his system if he wants to execute "hostname" on his system. He presses Y and the command executes. The output is sent back with GPTIN.***
```
GPTIN-0001: DESKTOP-90UIVS5 ##GPTIN-0001##
```
ChatGPT: 
```
GPTTASK-0001: Hostname: Desktop-90UIVS5 ##GPTTASK-0001##
GPTTASK-0001: Task complete. ##GPTTASK-0001##
GPTSTATUS: Waiting for new tasks... ##GPTSTATUS##
```
Brian: 
```
WORLDUPDATE: get the current date ##WORLDUPDATE##
```
ChatGPT:
```
GPTTASK-0002: Starting "get the current date" ##GPTCMD-0002##
GPTCMD-0002: date ##GPTCMD-0002##
```
Brian:

***Brian is prompted by the python script on his system if he wants to execute "date" on his system. He presses N and the command is skipped. ChatGPT is informed of this with a WORLDUPDATE from Brian.***
```
WORLDUPDATE: GPTCMD-0002: Skipped by user. ##WORLDUPDATE##
```
ChatGPT:

***ChatGPT abandons the current GPTCMD and tries a different command to accomplish the current task, incrementing the GPTCMD by 1 before submission.***
```
GPTTASK-0002: Skipping GPTCMD-0002. Generating new command... ##GPTTask-0002##
GPTCMD-0003: Get-Date ##GPTCMD-003##
```
Brian:

***Brian is prompted by the python script on his system if he wants to execute "Get-Date" on his system. He presses Y and the command executes. The output is sent back with GPTIN.***
```
GPTIN-0003:  Monday, February 20, 2023 1:54:17 PM ##GPTIN-0003##
```
ChatGPT: 
```
GPTTASK-0002: Date: Monday, February 20, 2023 ##GPTTASK-0002##
GPTTASK-0002: Task complete. ##GPTTASK-0002##
GPTWAIT: Waiting for new tasks... ##GPTWAIT##
```
