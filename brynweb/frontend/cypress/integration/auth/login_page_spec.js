describe("The Login Page", () => {
  const password = Cypress.env("dummy_password");
  const usernames = {
    ACTIVE_NO_TEAMS: "activeNoTeams",
    ACTIVE_PENDING_TEAM_VERIFICATION: "activePendingTeamVerification",
    ACTIVE_TEAM_ADMIN: "activeTeamAdmin",
    ACTIVE_TEAM_MEMBER: "activeTeamMember",
    DUPLICATE_EMAIL_USER_1: "duplicateEmailUser1",
    DUPLICATE_EMAIL_USER_2: "duplicateEmailUser2",
    INACTIVE: "inactive",
    NO_TEAMS_INVITE_ONLY: "noTeamsInviteOnly",
    PENDING_EMAIL_VERIFICATION: "pendingEmailVerification",
  };

  const beAtLogin = (loc) => {
    expect(loc.pathname).to.contain(Cypress.env("login_url"));
  };

  const beAtDashboard = (loc) => {
    expect(loc.pathname).to.not.contain(Cypress.env("login_url"));
    expect(loc.pathname).to.contain("/dashboard");
  };

  before(function() {
    // "this" points at the test context object
    cy.resetDB();

    cy.fixture("default_seed.json").then((json) => {
      // Seeded usernames for specific scenarious:
      this.users = json
        .filter((obj) => {
          return obj.model === "auth.user";
        })
        .map((obj) => {
          return obj.fields;
        })
        .reduce((acc, obj) => {
          acc[obj.username] = obj;
          return acc;
        }, {});
    });
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
      cy.findByRole("form", { name: /login form/i }).as("loginForm");
      cy.findByLabelText(/username/i).as("usernameInput");
      cy.findByLabelText(/password/i).as("passwordInput");
    });

    it("greets you with an obvious login form", () => {
      cy.get("@usernameInput")
        .should("be.visible")
        .invoke("attr", "placeholder")
        .should("match", /email or username/i);

      cy.get("@passwordInput")
        .should("be.visible")
        .invoke("attr", "placeholder")
        .should("match", /password/i);

      cy.findByRole("button", { name: /login/i })
        .should("be.visible")
        .and("have.attr", "type", "submit");
    });

    it("has a link to reset your password", () => {
      cy.findByRole("link", { name: /password/i })
        .should("be.visible")
        .and("have.attr", "href", "/user/password_reset/");
    });

    it("requires a username (which may be an email)", () => {
      cy.get("@passwordInput").type(password, { delay: 0 });
      cy.get("@loginForm").submit();
      cy.location().should(beAtLogin);

      cy.findByText(/is required/i)
        .should("be.visible")
        .and("have.class", "is-danger");
    });

    it("requires a password", function() {
      cy.get("@usernameInput").type(usernames.ACTIVE_TEAM_MEMBER, {
        delay: 0,
      });
      cy.get("@loginForm").submit();
      cy.location().should(beAtLogin);

      cy.findByText(/is required/i)
        .should("be.visible")
        .and("have.class", "is-danger");
    });

    it("won't authenticate invalid credentials", () => {
      cy.get("@usernameInput").type("some");
      cy.get("@passwordInput").type("nonsense");
      cy.get("@loginForm").submit();

      cy.location().should(beAtLogin);
      cy.findByRole("alert").should("contain", "username and password");
    });

    it("will authenticate valid credentials", function() {
      cy.get("@usernameInput").type(usernames.ACTIVE_TEAM_MEMBER, {
        delay: 0,
      });
      cy.get("@passwordInput").type(password + "{enter}", { delay: 0 });

      cy.getCookie("sessionid").should("exist");
      cy.location().should(beAtDashboard);
    });

    it("won't authenticate inactive users", function() {
      cy.get("@usernameInput").type(usernames.INACTIVE, {
        delay: 0,
      });
      cy.get("@passwordInput").type(password + "{enter}", { delay: 0 });

      cy.location().should(beAtLogin);
      cy.findByRole("alert")
        .should("contain", "disabled")
        .and("have.class", "is-danger");
    });

    it("won't authenticate users with no team memberships", function() {
      cy.get("@usernameInput").type(usernames.ACTIVE_NO_TEAMS, {
        delay: 0,
      });
      cy.get("@passwordInput").type(password + "{enter}", { delay: 0 });

      cy.location().should(beAtLogin);
      cy.findByRole("alert")
        .should("contain", "no current team memberships")
        .and("have.class", "is-danger");
    });

    it("won't authenticate users who have not verified their email", function() {
      cy.get("@usernameInput").type(usernames.PENDING_EMAIL_VERIFICATION, {
        delay: 0,
      });
      cy.get("@passwordInput").type(password + "{enter}", { delay: 0 });

      cy.location().should(beAtLogin);
      cy.findByRole("alert")
        .should("contain", "account activation")
        .and("have.class", "is-danger");
    });

    it("won't authenticate users who's only team is not verified'", () => {
      cy.get("@usernameInput").type(
        usernames.ACTIVE_PENDING_TEAM_VERIFICATION,
        {
          delay: 0,
        }
      );
      cy.get("@passwordInput").type(password + "{enter}", { delay: 0 });

      cy.location().should(beAtLogin);
      cy.findByRole("alert")
        .should("contain", "pending approval")
        .and("have.class", "is-danger");
    });

    it("won't authenticate an existing user with no teams, but with a pending invitation, navigating to dashboard", () => {
      cy.get("@usernameInput").type(usernames.NO_TEAMS_INVITE_ONLY);
      cy.get("@passwordInput").type(password);
      cy.get("@loginForm").submit();

      cy.location().should(beAtLogin);
      cy.findByRole("alert")
        .should("contain", "no current team")
        .and("contain", "invitation");
    });

    it("will allow login with email instead of username", function() {
      // use function so "this" points at test context obj
      cy.get("@usernameInput").type(
        this.users[usernames.ACTIVE_TEAM_MEMBER].email
      );
      cy.get("@passwordInput").type(password);
      cy.get("@loginForm").submit();

      cy.location().should(beAtDashboard);
    });

    it("won't allow legacy users to use email for login, where it is not unique", function() {
      // use function so "this" points at test context obj
      cy.get("@usernameInput").type(
        this.users[usernames.DUPLICATE_EMAIL_USER_1].email
      );
      cy.get("@passwordInput").type(password);
      cy.get("@loginForm").submit();

      cy.location().should(beAtLogin);
      cy.findAllByRole("alert")
        .first()
        .should("contain", "login using your username");
    });

    it("will allow users with duplicate emails to login using their username", function() {
      // use function so "this" points at test context obj
      cy.get("@usernameInput").type(usernames.DUPLICATE_EMAIL_USER_1);
      cy.get("@passwordInput").type(password);
      cy.get("@loginForm").submit();

      cy.location().should(beAtDashboard);
    });
  });
});
