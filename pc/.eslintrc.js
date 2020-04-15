module.exports = {
  root: true,
  env: {
    node: true
  },
  'extends': [
    'plugin:vue/essential',
    'eslint:recommended'
  ],
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    "semi": 0,       
    "eol-last": 0,
    "quotes": 0,
    "camelcase": 0
  },
  parserOptions: {
    parser: 'babel-eslint'
  }
}
