const { getYear } = require("date-fns/esm");

describe("The Login Page", () => {
  const username = "lisa";
  const password = "rAnd0mPa22w0rD";

  context("Unauthorized", () => {
    it("is redirected on visit to / when no session", () => {
      cy.request({
        url: "/",
        followRedirect: false,
      }).then(($response) => {
        expect($response.status).to.eq(302);
        expect($response.redirectedToUrl).to.eq(
          new URL("/user/login/?next=/", Cypress.config().baseUrl).toString()
        );
      });
    });
  });

  context("/user/login", () => {
    beforeEach(() => {
      cy.visit("/user/login");
      cy.get("#id_username").type(username);
      cy.get("#id_password").type(password);
    });

    it("greets you with an obvious login form", () => {
      cy.get("#id_username")
        .invoke("attr", "placeholder")
        .should("eq", "Email or username");

      cy.get("#id_password")
        .invoke("attr", "placeholder")
        .should("eq", "Password");

      cy.getBySel("login-submit-btn").should("contain", "Login");
    });

    it("has labels for screen readers", () => {
      cy.getBySel("login-field-username")
        .find("label")
        .should("have.class", "is-sr-only")
        .should("have.text", "Username");

      cy.getBySel("login-field-password")
        .find("label")
        .should("have.class", "is-sr-only")
        .should("have.text", "Password");
    });

    it("has a link to reset your password", () => {
      cy.getBySel("password-reset-link").should("contain", "password");
    });

    it("requires a username (which may be an email)", () => {
      cy.get("#id_username").clear();
      cy.getBySel("login-form").submit();
      cy.url().should("eq", Cypress.config().baseUrl + "/user/login/");

      cy.getBySel("login-field-username")
        .find(".help")
        .first()
        .should("contain", "required");
    });

    it("requires a password", () => {
      cy.get("#id_password").clear();
      cy.getBySel("login-form").submit();
      cy.url().should("eq", Cypress.config().baseUrl + "/user/login/");

      cy.getBySel("login-field-password")
        .find(".help")
        .first()
        .should("contain", "required");
    });

    it.only("requires valid credentials", () => {
      cy.get("#id_password").type("nonsense");
      cy.getBySel("login-form").submit();

      cy.url().should("eq", Cypress.config().baseUrl + "/user/login/");
      cy.get(".message.is-danger").should("contain", "username and password");
    });
  });
});
