const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const TerserPlugin = require('terser-webpack-plugin');

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
    import: './app/static/js/src/import.js',
    main: './app/static/js/src/main.js'
  },
  output: {
    path: path.resolve(__dirname, './app/static/js/dist'),
    filename: '[name].bundle.js'
  },
  module: {
    rules: [
      { test: /\.js$/i, exclude: /node_modules/, loader: "babel-loader" },
      {
        test: /\.scss$/i,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'postcss-loader',
          'sass-loader',
        ],
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "../../style/dist/style.css"
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
      },
      minimizer: [
        new OptimizeCSSAssetsPlugin({
          test: /\.css$/i,
        }),
        new TerserPlugin({
          test: /\.js(\?.*)?$/i,
        })
      ]
    }
};
