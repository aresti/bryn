import { resetDB } from "./utils";

Cypress.Commands.add("getBySel", (selector, ...args) => {
  return cy.get(`[data-testid=${selector}]`, ...args);
});

Cypress.Commands.add("getBySelLike", (selector, ...args) => {
  return cy.get(`[data-testid*=${selector}]`, ...args);
});

Cypress.Commands.add("resetDB", { prevSubject: false }, () => {
  resetDB();
});