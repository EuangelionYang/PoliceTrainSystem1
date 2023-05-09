'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  ENV_CONFIG: '"dev"',
  // BASE_API: '"http://121.195.154.165"',
  BASE_API: '"http://127.0.0.1:8000/"'
})
