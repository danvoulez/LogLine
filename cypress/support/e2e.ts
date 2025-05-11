import './commands'

// Para ignorar erros JS não relacionados
Cypress.on('uncaught:exception', (_err, _runnable) => {
  return false
})

// Antes de cada spec, reseta DB
beforeEach(() => {
  cy.resetDb()
})