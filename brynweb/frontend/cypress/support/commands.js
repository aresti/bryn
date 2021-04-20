import { resetDB } from "./utils";
import "@testing-library/cypress/add-commands";

Cypress.Commands.add("resetDB", { prevSubject: false }, () => {
  resetDB();
});

Cypress.Commands.add("loginByCSRF", (csrfToken) => {
  const username = "prestigious.prof@bham.ac.uk";
  const password = "1nt3grAT10nTesting";
  cy.request({
    method: "POST",
    url: "/user/login/",
    failOnStatusCode: false, // dont fail so we can make assertions
    form: true, // we are submitting a regular form body
    body: {
      username,
      password,
      csrfmiddlewaretoken: csrfToken,
    },
  });
});

Cypress.Commands.add("login", () => {
  cy.request("user/login/")
    .its("body")
    .then((body) => {
      const $html = Cypress.$(body);
      const csrf = $html.find("input[name=csrfmiddlewaretoken]").val();

      cy.loginByCSRF(csrf).then((resp) => {
        expect(resp.status).to.eq(200);
        expect(resp);
      });
    });
});
