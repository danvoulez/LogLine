describe('E2E | Actions', () => {
  beforeEach(() => {
    // Garante que está autenticado antes de cada teste
    cy.login('user@test.com', 'Test1234!')
  })

  it('should create a new log event via UI', () => {
    cy.visit('/actions')
    cy.get('input[name=action]')
      .should('be.visible')
      .type('test_action')
    cy.get('button[type=submit]').click()

    // Aguarda e verifica no histórico
    cy.contains('test_action', { timeout: 10000 }).should('exist')
  })
})