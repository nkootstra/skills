// CSV export for the old reporting tool.
export function toCsv(tickets) {
  const header = "id,title,priority,status";
  const rows = tickets.map((t) => [t.id, JSON.stringify(t.title), t.priority, t.status].join(","));
  return [header, ...rows].join("\n");
}
