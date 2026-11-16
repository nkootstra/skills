import { dueAt, isOverdue } from "../services/slaService.js";

export function priorityLabel(priority) {
  switch (priority) {
    case "urgent":
      return "Urgent (P1)";
    case "high":
      return "High (P2)";
    case "normal":
      return "Normal (P3)";
    case "low":
      return "Low (P4)";
    default:
      return priority;
  }
}

export function statusLabel(status) {
  if (status === "open") {
    return "Open";
  } else if (status === "pending") {
    return "Pending";
  } else if (status === "closed") {
    return "Closed";
  }
  return status;
}

export function formatTicket(ticket) {
  return {
    id: ticket.id,
    title: ticket.title,
    priority: priorityLabel(ticket.priority),
    status: statusLabel(ticket.status),
    assignee: ticket.assignee ?? "unassigned",
    dueAt: dueAt(ticket),
    overdue: isOverdue(ticket),
  };
}
