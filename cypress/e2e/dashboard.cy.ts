describe('E2E | Dashboard', () => {
  beforeEach(() => {
    cy.login('user@test.com', 'Test1234!')
  })

  it('should display metrics chart', () => {
    cy.visit('/dashboard')
    // Recharts monta um svg
    cy.get('svg.recharts-surface').should('exist')
    cy.get('path.recharts-line').should('have.length.at.least', 1)
  })
})