import test from "node:test";
import assert from "node:assert/strict";

import { validateCreate, validateFilter } from "../src/validators/ticketValidator.js";

test("create needs a title", () => {
  assert.throws(() => validateCreate({ title: "", priority: "normal", requester: "u-ana" }), /title is required/);
});

test("create rejects an unknown priority", () => {
  assert.throws(() => validateCreate({ title: "x", priority: "asap", requester: "u-ana" }), /priority must be one of/);
});

test("filter rejects an unknown status", () => {
  assert.throws(() => validateFilter({ status: "done" }), /status must be one of/);
});
