describe('E2E | Gateway', () => {
  beforeEach(() => {
    cy.login('user@test.com', 'Test1234!')
  })

  it('should forward payload through gateway', () => {
    // Mock do LLM_PROVIDER via intercept
    cy.intercept('POST', Cypress.env('LLM_URL') || '*', {
      statusCode: 200,
      body: { result: 'pong' }
    }).as('llmReq')

    cy.request({
      method: 'POST',
      url: `${Cypress.env('API_URL')}/api/v1/gateway/`,
      body: { ping: 'pong' },
      headers: { Authorization: `Bearer ${window.localStorage.getItem('token')}` }
    }).then((resp) => {
      expect(resp.status).to.eq(200)
      expect(resp.body).to.deep.equal({ result: 'pong' })
    })

    cy.wait('@llmReq').its('response.statusCode').should('eq', 200)
  })
})