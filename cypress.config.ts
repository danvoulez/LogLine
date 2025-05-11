import { defineConfig } from 'cypress'

export default defineConfig({
  e2e: {
    // URL do frontend (pode vir de ENV ou padrão)
    baseUrl: process.env.FRONTEND_URL || 'http://localhost:3000',
    // URL da API usada pelos comandos customizados
    env: {
      API_URL: process.env.API_URL || 'http://localhost:10000'
    },
    // Onde estão seus testes
    specPattern: 'cypress/e2e/**/*.cy.ts',
    supportFile: 'cypress/support/e2e.ts',
    // Gatilhos e tasks Node
    setupNodeEvents(on, config) {
      // Antes de tudo, reseta DB
      on('task', {
        async resetDb() {
          const { exec } = require('child_process')
          await new Promise<void>((resolve, reject) => {
            exec('bash scripts/reset_db.sh', (err: any) =>
              err ? reject(err) : resolve()
            )
          })
          return null
        }
      })
      return config
    },
    // Retries e tempo de espera generosos
    retries: { runMode: 2, openMode: 0 },
    defaultCommandTimeout: 10000,
    pageLoadTimeout: 60000,
    video: false,
    screenshots: { onRunFailure: true },
  }
})