# ASH - AutoShell

## Philosophy
ASH is a lightweight CLI tool built by a developer, for developers. It aims to stay minimal  
by default, yet powerful when you need it — making complexity a choice, not a burden.

## Development
### MVP 1:
- [X] Add parameter substitution
- [X] Add plugin infrastructure

### MVP 2:
- [X] Add basic configs
- [>] Autocomplete / Suggestions
- [X] Find a way to ensure all paramters have been filled in
- [ ] Add the `ash ash-source` feature 
    - Sources/dot-sources every function into the current shell to act as native functions

### MVP 3:
- [ ] Add the `ash ash-repl` feature
    - A custom loop where custom functions can be called without needing the `ash` command prefix 
- [ ] Add the `ash ash-info <command>` feature
    - Displays the metadata of a given function, described as `$data: "..."` in the YAML file