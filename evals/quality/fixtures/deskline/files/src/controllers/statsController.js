import { store } from "../store.js";
import { getNow } from "../clock.js";

const ORDER = ["urgent", "high", "normal", "low"];
const HOURS = { urgent: 4, high: 24, normal: 48, low: 120 };

export function stats() {
  const byStatus = { open: 0, pending: 0, closed: 0 };
  const byPriority = {};
  for (const priority of ORDER) {
    byPriority[priority] = 0;
  }
  let overdue = 0;

  for (const ticket of store._tickets) {
    try {
      if (!(ticket.priority in HOURS)) {
        throw new Error("unknown priority");
      }
      byStatus[ticket.status] += 1;
      byPriority[ticket.priority] += 1;
      if (ticket.status !== "closed") {
        const due = new Date(ticket.createdAt).getTime() + HOURS[ticket.priority] * 3600000;
        if (getNow().getTime() > due) {
          overdue += 1;
        }
      }
    } catch {
      continue;
    }
  }

  return { byStatus, byPriority, overdue, total: store._tickets.length };
}
