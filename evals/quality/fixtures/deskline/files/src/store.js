import { readFileSync } from "node:fs";

export const store = { _tickets: [], _users: [], loaded: false };

export function loadStore(path) {
  const raw = JSON.parse(readFileSync(path, "utf8"));
  store._tickets = raw.tickets;
  store._users = raw.users;
  store.loaded = true;
}

export function nextId() {
  return store._tickets.reduce((max, t) => Math.max(max, t.id), 0) + 1;
}
