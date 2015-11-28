# Commands/tasks

|Task|Description|
|----------|:-------------:|
|setup|Initializes you application by creating the necessary directories/files. Must run first|
|deploy|Performs the actual deployment|
|rollback|Removes the current release and reactivates the previous|

```
>>> fabrik stage setup
>>> fabrik stage deploy
```


## Debugging
Simple, just import `debug` from fabrik.api, then run it with your command.
Debug will then generate a log file called `fabrik-debug.log`.

Example: `fabrik debug demo deploy`

