const PRIORITIES = ["low", "normal", "high", "urgent"];
const STATUSES = ["open", "pending", "closed"];

export function validateCreate(input) {
  const errors = [];
  if (!input.title || input.title.trim() === "") {
    errors.push("title is required");
  } else if (input.title.length > 120) {
    errors.push("title is longer than 120 characters");
  }
  if (!PRIORITIES.includes(input.priority)) {
    errors.push(`priority must be one of ${PRIORITIES.join(", ")}`);
  }
  if (!input.requester) {
    errors.push("requester is required");
  }
  if (errors.length > 0) {
    throw new Error(errors.join("; "));
  }
}

export function validateFilter(filter) {
  if (filter.status && !STATUSES.includes(filter.status)) {
    throw new Error(`status must be one of ${STATUSES.join(", ")}`);
  }
  if (filter.priority && !PRIORITIES.includes(filter.priority)) {
    throw new Error(`priority must be one of ${PRIORITIES.join(", ")}`);
  }
}
