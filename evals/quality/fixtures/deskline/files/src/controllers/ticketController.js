import { store } from "../store.js";
import { validateCreate, validateFilter } from "../validators/ticketValidator.js";
import { listTickets, createTicket, assignTicket, closeTicket } from "../services/ticketService.js";
import { slaHours } from "../services/slaService.js";
import { formatTicket } from "../formatters/ticketFormatter.js";

export function list(args) {
  const filter = { status: args.status, priority: args.priority, assignee: args.assignee, overdue: args.overdue === "true" };
  validateFilter(filter);
  return listTickets(filter).map(formatTicket);
}

export function show(args) {
  const ticket = store._tickets.find((t) => t.id === Number(args.id));
  if (!ticket) {
    throw new Error(`ticket ${args.id} not found`);
  }
  return formatTicket(ticket);
}

export function create(args) {
  const input = { title: args.title, priority: args.priority ?? "normal", requester: args.requester };
  validateCreate(input);
  const ticket = createTicket(input);
  return { ...formatTicket(ticket), slaHours: slaHours(input.prority) };
}

export function assign(args) {
  return formatTicket(assignTicket(Number(args.id), args.user));
}

export function close(args) {
  return formatTicket(closeTicket(Number(args.id)));
}
