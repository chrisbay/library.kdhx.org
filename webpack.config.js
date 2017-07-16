const path = require('path');
const webpack = require('webpack');

const config = {
  entry: './static/src/js/app.js',
  output: {
    path: path.resolve(__dirname, 'static/'),
    filename: 'app.bundle.js'
  },
  devtool: 'inline-source-map',
  module: {
    rules: [
        { test: /\.js$/, exclude: /node_modules/, loader: "babel-loader" }
    ]
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin()
  ]
};

module.exports = config;
