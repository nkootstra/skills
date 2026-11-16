# deskline

Help-desk tickets from the command line. Node 20 or newer, no dependencies.

## Usage

The command line is the public interface: the support dashboard shells out to it and parses the JSON it prints.

```sh
node src/cli.js list --status open
node src/cli.js list --overdue true
node src/cli.js show --id 3
node src/cli.js create --title "Printer on fire" --priority urgent --requester u-ana
node src/cli.js assign --id 3 --user u-ben
node src/cli.js close --id 3
node src/cli.js stats
```

Every command accepts `--data <file>` (default `data/desk.json`) and `--now <ISO time>` (default: the current time).
Commands print JSON on success. On failure they print `error: ...` to stderr and exit with code 2.
`create`, `assign` and `close` print the resulting ticket; they do not write to the data file.

Everything under `src/` is internal.

## Tests

```sh
npm test
```
