# Flight search engine tool

**This task was created as solution of [Kiwi.com s.r.o.](https://www.kiwi.com/en/pages/content/about) task (task description can be seen in `task` folder):  
https://github.com/kiwicom/python-weekend-entry-task.**

For more information about tool, such as usage or input/output, check `task/README.md`.

### Usage

This tool can work as imported python package, but is mainly aimed to run from terminal. If imported as module, csv file checks are omitted, and it is expected, to be already well-formed. To run tool from `src` directory:
```
python3 -m solution ../input_example/example_from_task.csv BTW REJ --b=1
```

#### Arguments

| Argument name | Type           | Description              | Notes      |
|---------------|----------------|--------------------------|------------|
| file          | str            | path to file             | positional |
| origin        | str            | origin airport code      | positional |
| destination   | str            | destination airport code | positional |
| -b, --bags    | int (argument) | number of requested bags | optional   |
| -h, --help    | -              | help                     | optional   |