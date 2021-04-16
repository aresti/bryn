describe("The Login Page", () => {
  const username = "prestigious.prof@bham.ac.uk";
  const password = "1nt3grAT10nTesting";

  before(() => {
    cy.resetDB();
  });

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
      cy.get("#id_password").type(password, { delay: 0 });
      cy.getBySel("login-form").submit();
      cy.url().should("eq", Cypress.config().baseUrl + "/user/login/");

      cy.getBySel("login-field-username")
        .find(".help")
        .first()
        .should("contain", "required");
    });

    it("requires a password", () => {
      cy.get("#id_username").type(username, { delay: 0 });
      cy.getBySel("login-form").submit();
      cy.url().should("eq", Cypress.config().baseUrl + "/user/login/");

      cy.getBySel("login-field-password")
        .find(".help")
        .first()
        .should("contain", "required");
    });

    it("requires valid credentials", () => {
      cy.get("#id_username").type("some");
      cy.get("#id_password").type("nonsense");
      cy.getBySel("login-form").submit();

      cy.url().should("eq", Cypress.config().baseUrl + "/user/login/");
      cy.get(".message.is-danger").should("contain", "username and password");
    });

    it("navigates to dashboard on valid login", () => {
      cy.get("#id_username").type(username, { delay: 0 });
      cy.get("#id_password").type(password + "{enter}", { delay: 0 });
      cy.location().should((loc) => {
        expect(loc.pathname).to.not.contain("/user/login");
        expect(loc.pathname).to.contain("/dashboard");
      });
    });

    it("won't authenticate inactive users", () => {
      cy.get("#id_username").type("inactiveUser", { delay: 0 });
      cy.get("#id_password").type(password + "{enter}", { delay: 0 });

      cy.url().should("eq", Cypress.config().baseUrl + "/user/login/");
      cy.get(".message.is-danger").should("contain", "disabled");
    });

    it("won't authenticate users with no team memberships", () => {
      cy.get("#id_username").type("legacyUserNoTeams", { delay: 0 });
      cy.get("#id_password").type(password + "{enter}", { delay: 0 });

      cy.url().should("eq", Cypress.config().baseUrl + "/user/login/");
      cy.get(".message.is-danger").should(
        "contain",
        "no current team memberships"
      );
    });

    it("won't authenticate users who have not verified their email", () => {
      cy.get("#id_username").type("user.pending.email@bham.uk", { delay: 0 });
      cy.get("#id_password").type(password + "{enter}", { delay: 0 });

      cy.url().should("eq", Cypress.config().baseUrl + "/user/login/");
      cy.get(".message.is-danger").should("contain", "account activation");
    });

    it("won't authenticate users who's only team is not verified'", () => {
      cy.get("#id_username").type("userPendingTeamVerification", { delay: 0 });
      cy.get("#id_password").type(password + "{enter}", { delay: 0 });

      cy.url().should("eq", Cypress.config().baseUrl + "/user/login/");
      cy.get(".message.is-danger").should("contain", "pending approval");
    });
  });
});
