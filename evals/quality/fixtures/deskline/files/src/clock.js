// The CLI sets the time once; services ask for it when they need it.
let current = null;

export function setNow(iso) {
  current = iso ? new Date(iso) : null;
}

export function getNow() {
  return current ?? new Date();
}
