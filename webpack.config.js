var webpack = require('webpack');
var path = require('path');

var BUILD_DIR = path.resolve(__dirname, 'static/scripts/js');
var APP_DIR = path.resolve(__dirname, 'static/scripts/');

var config = {
    entry: {
        index: APP_DIR + '/index.jsx'
    },
    output: {
        path: BUILD_DIR,
        filename: '[name].bundle.js'
    },
    module: {
        loaders: [
            {
                test: /.jsx?/,
                include: APP_DIR,
                loader: 'babel'
            }
        ]
    }
};

module.exports = config;
