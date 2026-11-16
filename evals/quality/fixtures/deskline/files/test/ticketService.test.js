import test from "node:test";
import assert from "node:assert/strict";

import { loadStore } from "../src/store.js";
import { setNow } from "../src/clock.js";
import { assignTicket, closeTicket, listTickets } from "../src/services/ticketService.js";

loadStore("data/desk.json");
setNow("2026-10-05T09:00:00.000Z");

test("assigning an open ticket moves it to pending", () => {
  const ticket = assignTicket(1, "u-ben");
  assert.equal(ticket.assignee, "u-ben");
  assert.equal(ticket.status, "pending");
});

test("an inactive user cannot be assigned", () => {
  assert.throws(() => assignTicket(1, "u-cas"), /inactive/);
});

test("an unassigned open ticket cannot be closed", () => {
  assert.throws(() => closeTicket(1), /unassigned/);
});

test("listing works", () => {
  assert.ok(listTickets());
});
