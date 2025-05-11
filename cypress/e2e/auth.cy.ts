describe('E2E | Auth', () => {
  it('should register, login and redirect to dashboard', () => {
    const email = 'user@test.com'
    const password = 'Test1234!'

    cy.visit('/register')
    cy.get('input[name=email]').type(email)
    cy.get('input[name=password]').type(password)
    cy.get('button[type=submit]').click()

    // Após registro, deve ir para login
    cy.url().should('include', '/login')

    // Usa comando customizado
    cy.login(email, password)
    cy.visit('/dashboard')

    // Verifica dashboard carregado
    cy.contains('Dashboard Metrics').should('be.visible')
  })
})