describe('E2E | Webhooks', () => {
  it('should accept valid webhook and reject invalid signature', () => {
    const secret = Cypress.env('JWT_SECRET')!
    const payload = { event: 'test_event', data: { foo: 'bar' } }
    const body = JSON.stringify(payload)
    const signature = `sha256=${Cypress.Buffer.from(require('crypto')
      .createHmac('sha256', secret)
      .update(body)
      .digest('hex')).toString()}`

    // Caso válido
    cy.request({
      method: 'POST',
      url: `${Cypress.env('API_URL')}/webhooks/receive`,
      headers: { 'X-Hub-Signature-256': signature, 'Content-Type': 'application/json' },
      body: payload
    }).then((resp) => {
      expect(resp.status).to.eq(200)
      expect(resp.body).to.have.property('status', 'received')
    })

    // Caso inválido
    cy.request({
      method: 'POST',
      url: `${Cypress.env('API_URL')}/webhooks/receive`,
      headers: { 'X-Hub-Signature-256': 'sha256=wrongsignature', 'Content-Type': 'application/json' },
      body: payload,
      failOnStatusCode: false
    }).then((resp) => {
      expect(resp.status).to.be.oneOf([400,401])
    })
  })
})