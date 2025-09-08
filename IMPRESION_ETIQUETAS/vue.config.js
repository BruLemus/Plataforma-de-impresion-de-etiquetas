/**
 * vue.config.js
 * Configuración personalizada para Vue CLI 5 / Webpack 5.
 */

module.exports = {
  // Configuración del servidor de desarrollo
  devServer: {
    port: 8080,   // Cambia el puerto si quieres
    open: true,   // Abre el navegador automáticamente
  },

  // Directorio de salida de la compilación
  outputDir: 'dist',

  // Rutas públicas si tu app no está en la raíz
  publicPath: '/',

  // Transpilar dependencias específicas
  transpileDependencies: [
    // Ejemplo: 'vuetify', 'some-es6-package'
  ],

  // Configuración opcional de Webpack
  configureWebpack: {
    // Plugins adicionales (sin progress-webpack-plugin)
    plugins: [
      // Aquí puedes agregar plugins compatibles con Webpack 5 si los necesitas
    ],
  },

  // Configuración opcional de proxy para API
  // devServer: {
  //   proxy: {
  //     '/api': {
  //       target: 'http://localhost:3000',
  //       changeOrigin: true,
  //     },
  //   },
  // },
};
