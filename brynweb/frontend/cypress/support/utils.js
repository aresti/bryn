export const resetDB = () => {
  console.log("Reset database");
  cy.request({
    method: "POST",
    url: "/api/reset/",
  });
};
