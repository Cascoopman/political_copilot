### Debugging with Visual Studio Code

Visual studio code makes use of a configuration file called ```launch.json``` 
to create a customized debugging scenario and save it for reuse later.
Out of the box, VSCode comes with a few premade debugging configurations such 
as a normal Python file, Flask and Django. Connexion is not an option, so you 
can find a custom launch config for it here.

```
{
    "name": "Microservice <MICROSERVICE_NAME>",
    "type": "python",
    "request": "launch",
    "program": "run.py",
    "cwd": "${workspaceFolder}/<MICROSERVICE_FOLDER>"
}
``` 
More info about VSCode debugging can be found 
[here](https://code.visualstudio.com/docs/editor/debugging).

To use the config and debug a Connexion app follow these steps:

#### Step 1
Click the debug icon in the left bar of VSCode ( or use ```crtl+shift+D```) 
and press the cog icon a the top, next to the terminal icon to open your 
```launch.json``` configfile.

#### Step 2
Copy and paste the json config from this folder into the `configurations` list 
in the ```launch.json``` and save the file. **Make sure** the ```cwd``` 
argument works for your project structure. By default, the port is not specified 
and the ```cwd``` assumes debugging is run from within the microservice. 

#### Step 3
In `run.py` of your microservice, disable the reloader as this will not work
together with the VS Code Debugger:
```
APP.run(host='0.0.0.0', port=os.environ.get('PORT', 8080), debug=True,
        use_reloader=False)
```

#### Step 4
Go back to the debug tab, select `Microservice <MICROSERVICE_NAME>` from the 
dropdown next to the cog icon and press the start (green triangle) button. You 
should now be debugging.

#### Bonus
If you want one configuration for all your microservices, you can replace 
`<MICROSERVICE_FOLDER>` with `${input:microservice_name}` and add the following 
to the root of `launch.json`:

```
"inputs": [
    {
        "id": "microservice_name",
        "type": "pickString",
        "default": "ingestion",
        "options": [
            "<MICROSERVICE_1>",
            "<MICROSERVICE_2>",
        ],
        "description": "The name of the microservice to debug"
    }
]
```
Now, when you start debugging, you will be prompted with a dropdown list with 
the options you specified.

More info can be found 
[here](https://code.visualstudio.com/docs/editor/variables-reference#_input-variables).
