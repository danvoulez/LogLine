describe('E2E | Admin', () => {
  const admin = { email: 'admin@admin.com', password: 'AdminPass123!' }

  beforeEach(() => {
    // Registrar e autenticar admin
    cy.request('POST', `${Cypress.env('API_URL')}/api/v1/auth/register`, {
      email: admin.email,
      password: admin.password
    })
    cy.login(admin.email, admin.password)
  })

  it('should access admin status and stats', () => {
    cy.visit('/admin/status')
    cy.contains('admin OK').should('exist')

    cy.visit('/admin/stats?days=1')
    cy.contains('total_users').should('exist')
    cy.contains('recent_logs').should('exist')
  })
})