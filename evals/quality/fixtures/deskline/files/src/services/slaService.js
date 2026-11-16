import { getNow } from "../clock.js";
import { isOpen } from "./ticketService.js";

export function slaHours(priority) {
  switch (priority) {
    case "urgent":
      return 4;
    case "high":
      return 24;
    case "normal":
      return 48;
    case "low":
      return 120;
    default:
      return 48;
  }
}

export function dueAt(ticket) {
  const created = new Date(ticket.createdAt).getTime();
  return new Date(created + slaHours(ticket.priority) * 3600000).toISOString();
}

export function isOverdue(ticket) {
  if (!isOpen(ticket)) {
    return false;
  }
  return getNow().getTime() > new Date(dueAt(ticket)).getTime();
}
