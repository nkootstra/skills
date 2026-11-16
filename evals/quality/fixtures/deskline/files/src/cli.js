import { setNow } from "./clock.js";
import { loadStore } from "./store.js";
import * as tickets from "./controllers/ticketController.js";
import { stats } from "./controllers/statsController.js";

function parse(argv) {
  const [command, ...rest] = argv;
  const args = {};
  for (let i = 0; i < rest.length; i += 2) {
    if (!rest[i].startsWith("--") || rest[i + 1] === undefined) {
      throw new Error(`bad argument: ${rest[i]}`);
    }
    args[rest[i].slice(2)] = rest[i + 1];
  }
  return { command, args };
}

function main(argv) {
  const { command, args } = parse(argv);
  loadStore(args.data ?? "data/desk.json");
  setNow(args.now);

  let result;
  if (command === "list") {
    result = tickets.list(args);
  } else if (command === "show") {
    result = tickets.show(args);
  } else if (command === "create") {
    result = tickets.create(args);
  } else if (command === "assign") {
    result = tickets.assign(args);
  } else if (command === "close") {
    result = tickets.close(args);
  } else if (command === "stats") {
    result = stats();
  } else {
    throw new Error(`unknown command: ${command}`);
  }
  console.log(JSON.stringify(result));
}

try {
  main(process.argv.slice(2));
} catch (err) {
  console.error(`error: ${err.message}`);
  process.exitCode = 2;
}
