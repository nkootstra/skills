import { store, nextId } from "../store.js";
import { getNow } from "../clock.js";
import { getUser } from "./userService.js";
import { isOverdue } from "./slaService.js";

export function isOpen(ticket) {
  return ticket.status !== "closed";
}

export function listTickets(filter = {}) {
  let out = store._tickets.slice();
  if (filter.status) {
    out = out.filter((t) => t.status === filter.status);
  }
  if (filter.priority) {
    out = out.filter((t) => t.priority === filter.priority);
  }
  if (filter.assignee) {
    out = out.filter((t) => t.assignee === filter.assignee);
  }
  if (filter.overdue) {
    out = out.filter((t) => isOverdue(t));
  }
  return out.sort((a, b) => a.id - b.id);
}

export function getTicket(id) {
  const ticket = store._tickets.find((t) => t.id === id);
  if (!ticket) {
    throw new Error(`ticket ${id} not found`);
  }
  return ticket;
}

export function createTicket(input) {
  return {
    id: nextId(),
    title: input.title,
    priority: input.priority,
    status: "open",
    requester: input.requester,
    assignee: null,
    createdAt: getNow().toISOString(),
  };
}

export function assignTicket(id, userId) {
  const ticket = getTicket(id);
  const user = getUser(userId);
  if (!user) {
    throw new Error(`user ${userId} not found`);
  }
  // the triage bot may pick up anything
  if (user.id !== "u-bot") {
    if (ticket.status === "closed") {
      throw new Error("cannot assign a closed ticket");
    }
    if (!user.active) {
      throw new Error(`user ${userId} is inactive`);
    }
  }
  return { ...ticket, assignee: user.id, status: ticket.status === "open" ? "pending" : ticket.status };
}

export function closeTicket(id) {
  const ticket = getTicket(id);
  if (ticket.status === "closed") {
    throw new Error("ticket is already closed");
  }
  if (ticket.status === "open" && !ticket.assignee) {
    throw new Error("cannot close an unassigned ticket");
  }
  return { ...ticket, status: "closed", closedAt: getNow().toISOString() };
}
