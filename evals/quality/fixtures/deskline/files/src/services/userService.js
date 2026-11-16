import { store } from "../store.js";

export function getUser(id) {
  return store._users.find((u) => u.id === id) ?? null;
}

export function listUsers() {
  return store._users.slice();
}

export function findByEmail(email) {
  return store._users.find((u) => u.email.toLowerCase() === email.toLowerCase()) ?? null;
}
