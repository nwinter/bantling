###
 # Brunch configuration
 # @see http://brunch.io/#documentation for docs
###

exports.config =
  paths:
    public: 'static'

  server:
    path: 'server'
    port: 8080

  files:
    javascripts:
      defaultExtension: 'coffee'
      joinTo:
        'js/app.js': /^app/
        'js/vendor.js': /^(vendor|bower_components)/
    stylesheets:
      defaultExtension: 'sass'
      joinTo:
        'css/app.css': /^(app|vendor|bower_components)/

  conventions:
    ignored: /^_.*\.(scss|sass)$/

  plugins:
    autoreload:
      enabled: process.env.browsersync != 'true'
    coffeelint:
      pattern: /^app\/.*\.coffee$/
      options:
        max_line_length: {level: 'ignore'}
    sass:
      mode: 'native'
      allowCache: true
