// Extensões de tipos para os comandos
declare global {
  namespace Cypress {
    interface Chainable {
      /**
       * Faz login via API e guarda token no localStorage.
       * @param email email do usuário
       * @param password senha do usuário
       */
      login(email: string, password: string): Chainable<void>;
      /** Reseta o banco usando task definida no config. */
      resetDb(): Chainable<void>;
    }
  }
}

Cypress.Commands.add('resetDb', () => {
  return cy.task('resetDb')
})

Cypress.Commands.add('login', (email: string, password: string) => {
  const apiUrl = Cypress.env('API_URL')
  return cy
    .request('POST', `${apiUrl}/api/v1/auth/login`, {
      username: email,
      password
    })
    .then((resp) => {
      expect(resp.status).to.eq(200)
      const token = resp.body.access_token
      // Grava no localStorage do app
      window.localStorage.setItem('token', token)
    })
})