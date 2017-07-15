const path = require('path');
const webpack = require('webpack');

const config = {
  entry: './static/js/src/app.js',
  output: {
    path: path.resolve(__dirname, 'static/js/dist'),
    filename: 'app.bundle.js'
  },
  devtool: 'inline-source-map',
  module: {
    rules: [
        { test: /\.js$/, exclude: /node_modules/, loader: "babel-loader" }
    ]
  },
  plugins: [
    new webpack.DefinePlugin({
        'process.env': {
            NODE_ENV: JSON.stringify('production')
        }
    }),
    new webpack.optimize.UglifyJsPlugin()
  ]
};

module.exports = config;
