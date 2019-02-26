var path = require('path');
var webpack = require('webpack');

module.exports = {
  mode: 'production',
  watch: true,
  entry: {
    park: './app/static/js/src/park.js',
    exhibition: './app/static/js/src/exhibition.js',
    org: './app/static/js/src/org.js',
    artwork: './app/static/js/src/artwork.js',
    artist: './app/static/js/src/artist.js',
    create: './app/static/js/src/create.js',
    import: './app/static/js/src/import.js'
  },
  output: {
    path: path.resolve(__dirname, './app/static/js/dist'),
    filename: '[name].bundle.js'
  },
  module: {
    rules: [
      { test: /\.js$/, exclude: /node_modules/, loader: "babel-loader" }
    ]
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    })
  ],
  stats: {
    colors: true
  },
  devtool: 'source-map',
  optimization: {
      splitChunks: {
        cacheGroups: {
          commons: {
            name: 'commons',
            chunks: 'initial',
            minChunks: 2
          }
        }
      }
    }
};
